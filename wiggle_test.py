import time
from functools import partial

import numpy as np
import pandas as pd

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

from bluesky.utils import (Msg, short_uid)

from bluesky import RunEngine, callbacks
from bluesky.utils import install_kicker

from jet_tracking.sim import generate_simulation
from jet_tracking.plan_stubs import wiggle


def load_simulation_data_from_hdf5(fn):
    import h5py  # TODO
    with h5py.File(fn, 'r') as f:
        items = dict((key, value)
                     for key, value in f.items()
                     if key not in ('Sc3Inline', 'evr', 'event_time', 'ebeam',
                                    'fiducials', 'phase_cav', 'gas_detector', ))

        print(list(items.keys()), [(key, np.asarray(value).shape) for key, value in items.items()])
        df = pd.DataFrame(items)
        df = df.rename(columns={'FEEGasDetEnergy': 'gas_det',
                                'DsdCsPad': 'cspad_sum'},
                       index=int,
                       )
        print(list(df.keys()))
    return df


def load_simulation_data_from_csv(fn):
    df = pd.read_csv(fn)
    df = df.rename(columns={'FEEGasDetEnergy': 'gas_det',
                            'DsdCspad_diffraction_intensity': 'cspad_sum'},
                   index=int,
                   )
    return df


def averaged_step(average_counts, detectors, motor, step):
    group = short_uid('set')
    yield Msg('checkpoint')
    yield Msg('set', motor, step, group=group)
    yield Msg('wait', None, group=group)

    def strip_timestamp(reading):
        for name, det_reading in list(reading.items()):
            reading[name] = det_reading['value']
        return reading

    def single_reading():
        reading = (yield from bps.trigger_and_read(list(detectors) + [motor]))
        return strip_timestamp(reading)

    readings = []
    for i in range(average_counts):
        readings.append((yield from single_reading()))

    all_readings = pd.DataFrame.from_records(readings)
    return {key: {'value': all_readings[key].mean(),
                  'timestamp': time.time(),
                  }
            for key in all_readings}


def load_good_dataset():
    # df = load_simulation_data_from_csv('run271.csv')
    df = load_simulation_data_from_hdf5('cxip12516_good/mpi_data_cxip12516_271_FEEGasDetEnergy_DsdCsPad_pi3_x_pi3_fine_x_Sc3Inline.h5')
    print(list(df.keys()))
    df.pi3_x -= df.pi3_x[0]
    df.gas_det[np.abs(df.gas_det) < 1.0] = np.nan
    df = df.dropna()

    df.cspad_sum /= np.max(df.cspad_sum)
    norm_cspad = df.cspad_sum / df.gas_det
    norm_cspad /= np.max(norm_cspad)
    return df


def test():
    df = load_good_dataset()
    ns = generate_simulation('pi3_x', 'cspad_sum', df, motor_precision=0)

    dets = [ns.signal, ns.motor]

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={})
    def scan():
        iter_ = 0
        last_intensity = None
        min_wiggle = 0.001
        max_wiggle = 0.003
        step_size = min_wiggle
        while True:
            iter_ += 1
            if not (iter_ % 5):
                ns.offset.put(ns.offset.value + 0.005)  # 3um steps every 5 iterations works
                plt.vlines(-ns.offset.value, 0, 1)

            pos, intensity = yield from wiggle(
                dets, ns.signal.name, ns.motor, step_size=step_size,
                per_step=partial(averaged_step, 5))

            intensity = intensity['value']

            yield from bps.abs_set(ns.motor, pos, wait=True)
            print(f'Now at position {pos} with reading {intensity} '
                  f'(offset={ns.offset.value}; step={step_size})')

            if last_intensity is not None:
                step_size = (last_intensity / intensity) * max_wiggle
                step_size = max(min(max_wiggle, step_size), min_wiggle)

            last_intensity = intensity

            yield from bps.sleep(0.1)

    ns.scan = scan

    return ns


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Qt5Agg')
    import matplotlib.pyplot as plt

    install_kicker()

    plt.figure()
    plt.ion()
    plt.show()
    ns = test()
    plot = callbacks.LivePlot(x=ns.motor.name, y=ns.signal.name,
                              legend_keys=[ns.signal.name], lw=0.5)
    RE = RunEngine({})
    a = input('test')
    RE(ns.scan(), plot)
