from ophyd.device import Device, FormattedComponent as FCpt
from ophyd.signal import EpicsSignal
from ophyd.areadetector.plugins import ROIPlugin, StatsPlugin, ImagePlugin

from pcdsdevices.areadetector.detectors import PCDSDetector
from pcdsdevices.epics_motor import IMS

class Injector(Device):
    '''An Injector which consists of 3 coarse control motors and 3 fine control motors
        
       Parameters
       ----------
       pvs : str dict
           A dictionary containing the name of the device and
           the PVs of all the injector components
        
       Attributes
       ----------
       coarseX : EpicsSignal
           The coarse control motor in the X direction
       coarseY : EpicsSignal
           The coarse control motor in the Y direction
       coarseZ : EpicsSignal
           The coarse control motor in the Z direction
       fineX : EpicsSignal
           The fine control motor in the X direction
       fineY : EpicsSignal
           The fine control motor in the Y direction
       fineZ : EpicsSignal
           The fine control motor in the Z direction
       '''

    coarseX = FCpt(IMS, '{self._coarseX}')
    coarseY = FCpt(IMS, '{self._coarseY}')
    coarseZ = FCpt(IMS, '{self._coarseZ}')
                
    fineX = FCpt(IMS, '{self._fineX}')
    fineY = FCpt(IMS, '{self._fineY}')
    fineZ = FCpt(IMS, '{self._fineZ}')
                            
    def __init__(self, name,
                       coarseX, coarseY, coarseZ,
                       fineX, fineY, fineZ, **kwargs):
                                        
        self._coarseX = coarseX
        self._coarseY = coarseY
        self._coarseZ = coarseZ
                                                             
        self._fineX = fineX
        self._fineY = fineY
        self._fineZ = fineZ

        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal.prefix+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'velocity', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adict={'value': 'user_readback', 'units': 'motor_egu'}
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in self._signals.items():
            sget = signal.get()
            atable[name] = {'desc': adesc.get(name)}
            for attr in attrs:
                field = adict.get(attr, attr)
                try:
                    atable[name][attr] = getattr(sget, field)
                except:
                    pass

        return pd.DataFrame(atable).T[attrs]


class Selector(Device):
    '''A Selector for the sample delivery system
        
       Parameters
       ----------
       pvs : str dict
           A dictionary containing the name of the device and
           the PVs of all the selector components
       
       Attributes
       ----------
       remote_control : EpicsSignal
           Remote control enabled
       status : EpicsSignal
           Connection status for selector
       flow : EpicsSignal
           Flow
       flowstate : EpicsSignal
           State of the flow
       flowtype : EpicsSignal
           Type of the flow
       FM_rb : EpicsSignal
       
       FM_reset : EpicsSignal
       
       FM : EpicsSignal
       
       names_button : EpicsSignal
       
       couple_button : EpicsSignal
       
       names1 : EpicsSignal
       
       names2 : EpicsSignal
       
       shaker1 : EpicsSignal
           Shaker 1
       shaker2 : EpicsSignal
           Shaker 2
       shaker3 : EpicsSignal
           Shaker 3
       shaker4 : EpicsSignal
           Shaker 4
       '''
    
    remote_control = FCpt(EpicsSignal, '{self._remote_control}') # also appears on pressure controller screen?
    status = FCpt(EpicsSignal, '{self._status}')
    
    flow = FCpt(EpicsSignal, '{self._flow}')
    flowstate = FCpt(EpicsSignal, '{self._flowstate}')
    flowtype = FCpt(EpicsSignal, '{self._flowtype}')
    
    FM_rb = FCpt(EpicsSignal, '{self._FM_rb}')
    FM_reset = FCpt(EpicsSignal, '{self._FM_reset}')
    FM = FCpt(EpicsSignal, '{self._FM}')
    
    names_button = FCpt(EpicsSignal, '{self._names_button}')
    couple_button = FCpt(EpicsSignal, '{self._couple_button}')
    names1 = FCpt(EpicsSignal, '{self._names1}')
    names2 = FCpt(EpicsSignal, '{self._names2}')
    
    shaker1 = FCpt(EpicsSignal, '{self._shaker1}')
    shaker2 = FCpt(EpicsSignal, '{self._shaker2}')
    shaker3 = FCpt(EpicsSignal, '{self._shaker3}')
    shaker4 = FCpt(EpicsSignal, '{self._shaker4}')
    
    def __init__(self, name,
                       remote_control, status,
                       flow, flowstate, flowtype,
                       FM_rb, FM_reset, FM,
                       names_button, couple_button, names1, names2,
                       shaker1, shaker2, shaker3, shaker4, **kwargs):
        
        self._status = status
        self._remote_control = remote_control
        
        self._flow = flow
        self._flowstate = flowstate
        self._flowtype = flowtype
        
        self._FM_rb = FM_rb
        self._FM_reset = FM_reset
        self._FM = FM
        
        self._names_button = names_button
        self._couple_button = couple_button
        self._names1 = names1
        self._names2 = names2
    
        self._shaker1 = shaker1
        self._shaker2 = shaker2
        self._shaker3 = shaker3
        self._shaker4 = shaker4
        
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]


class CoolerShaker(Device):
    '''A Cooler/Shaker for the sample delivery system
        
       Parameters
       ----------
       pvs : str dict
           A dictionary containing the PVs of all the cooler/shaker components
       name : str
           The device name
        
       Attributes
       ----------
       temperature1 : EpicsSignal
           Temperature of 1
       SP1 : EpicsSignal
           Set point of 1
       set_SP1 : EpicsSignal
           Set the set point for 1
       current1 : EpicsSignal
           Current for 1
       temperature2 : EpicsSignal
           Temperature of 2
       SP2 : EpicsSignal
           Set point of 2
       set_SP2 : EpicsSignal
           Set the set point of 2
       current2 : EpicsSignal
           Current of 2
       reboot : EpicsSignal
           Reboot the cooler/shaker
       '''
    
    temperature1 = FCpt(EpicsSignal, '{self._temperature1}')
    SP1 = FCpt(EpicsSignal, '{self._SP1}')
    set_SP1 = FCpt(EpicsSignal, '{self._set_SP1}')
    current1 = FCpt(EpicsSignal, '{self._current1}')
    
    temperature2 = FCpt(EpicsSignal, '{self._temperature2}')
    SP2 = FCpt(EpicsSignal, '{self._SP2}')
    set_SP2 = FCpt(EpicsSignal, '{self._set_SP2}')
    current2 = FCpt(EpicsSignal, '{self._current2}')
    
    reboot = FCpt(EpicsSignal, '{self._reboot}')
    
    def __init__(self, name,
                       temperature1, SP1, set_SP1, current1,
                       temperature2, SP2, set_SP2, current2,
                       reboot, **kwargs):
        
        self._temperature1 = temperature1
        self._SP1 = SP1
        self._set_SP1 = set_SP1
        self._current1 = current1
        
        self._temperature2 = temperature2
        self._SP2 = SP2
        self._set_SP2 = set_SP2
        self._current2 = current2
        
        self._reboot = reboot
        
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]



class HPLC(Device):
    '''An HPLC for the sample delivery system
        
       Parameters
       ----------
       pvs : str dict
           A dictionary containing the PVs of all the HPLC components
       name : str
           The device name
        
       Attributes
       ----------
       status : EpicsSignal
           Status of the HPLC
       run : EpicsSignal
           Run the HPLC
       flowrate : EpicsSignal
           Flow rate of the HPLC
       set_flowrate : EpicsSignal
           Set the flow rate of the HPLC
       flowrate_SP : EpicsSignal
           Set point for the flow rate
       pressure : EpicsSignal
           Pressure in the HPLC
       pressure_units : EpicsSignal
           Units for the pressure
       set_max_pressure : EpicsSignal
           Set the maximum pressure
       max_pressure : EpicsSignal
           Maximum pressure
       clear_error : EpicsSignal
           Clear errors
       '''
    
    status = FCpt(EpicsSignal, '{self._status}')
    run = FCpt(EpicsSignal, '{self._run}')
    
    flowrate = FCpt(EpicsSignal, '{self._flowrate}')
    set_flowrate = FCpt(EpicsSignal, '{self._set_flowrate}')
    flowrate_SP = FCpt(EpicsSignal, '{self._flowrate_SP}')
    
    pressure = FCpt(EpicsSignal, '{self._pressure}')
    pressure_units = FCpt(EpicsSignal, '{self._pressure_units}')
    set_max_pressure = FCpt(EpicsSignal, '{self._set_max_pressure')
    max_pressure = FCpt(EpicsSignal, '{self._max_pressure}')
    
    clear_error = FCpt(EpicsSignal, '{self._clear_error}')
    
    def __init__(self, name,
                       status, run,
                       flowrate, set_flowrate, flowrate_SP,
                       pressure, pressure_units, set_max_pressure, max_pressure,
                       clear_error, **kwargs):
        
        self._status = status
        self._run = run
        
        self._flowrate = flowrate
        self._set_flowrate = set_flowrate
        self._flowrate_SP = flowrate_SP
        
        self._pressure = pressure
        self._pressure_units = pressure_units
        self._set_max_pressure = set_max_pressure
        self._max_pressure = max_pressure
        
        self._clear_error = clear_error
        
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]



class PressureController(Device):
    '''An Pressure Controller for the sample delivery system
        
       Parameters
       ----------
       pvs : str dict
           A dictionary containing the PVs of all the pressure controller components
       name : str
           The device name
        
       Attributes
       ----------
       status : EpicsSignal
           Connection status of pressure controller
       pressure1 : EpicsSignal
           Pressure of 1
       enabled1 : EpicsSignal
           Is 1 enabled
       limit1 : EpicsSignal
           High pressure limit of 1
       SP1 : EpicsSignal
           Pressure set point of 1
       pressure2 : EpicsSignal
           Pressure of 2
       enabled2 : EpicsSignal
           Is 2 enabled
       limit2 : EpicsSignal
           High pressure limit of 2
       SP2 : EpicsSignal
           Pressure set point of 2
       '''
    
    status = FCpt(EpicsSignal, '{self._status}')
    
    pressure1 = FCpt(EpicsSignal, '{self._pressure1}')
    enabled1 = FCpt(EpicsSignal, '{self._enabled1}')
    limit1 = FCpt(EpicsSignal, '{self._limit1}')
    SP1 = FCpt(EpicsSignal, '{self._SP1}')
    
    pressure2 = FCpt(EpicsSignal, '{self._pressure2}')
    enabled2 = FCpt(EpicsSignal, '{self._enabled2}')
    limit2 = FCpt(EpicsSignal, '{self._limit2}')
    SP2 = FCpt(EpicsSignal, '{self._SP2}')
    
    def __init__(self, name,
                       status,
                       pressure1, enabled1, limit1, SP1,
                       pressure2, enabled2, limit2, SP2, **kwargs):
        
        self._status = status
        
        self._pressure1 = pressure1
        self._enabled1 = enabled1
        self._limit1 = limit1
        self._SP1 = SP1
        
        self._pressure2 = pressure2
        self._enabled2 = enabled2
        self._limit2 = limit2
        self._SP2 = SP2
        
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]


class FlowIntegrator(Device):
    '''An FlowIntegrator for the sample delivery system
        
       Parameters
       ----------
       pvs : str dict
           A dictionary containing the PVs of all the flow integrator components
       name : str
           The device name
        
       Attributes
       ----------
       integrator_source: EpicsSignal
       
       flow_source : EpicsSignal
       
       names : EpicsSignal
           Names of
       start1 : EpicsSignal
           Starting volume of 1
       used1 : EpicsSignal
           Flow of 1
       time1 : EpicsSignal
           Estimated depletion time of 1
       start2 : EpicsSignal
           Starting volume of 2
       used2 : EpicsSignal
           Flow of 2
       time2 : EpicsSignal
           Estimated depletion time of 2
       start3 : EpicsSignal
           Starting volume of 3
       used3 : EpicsSignal
           Flow of 3
       time3 : EpicsSignal
           Estimated depletion time of 3
       start4 : EpicsSignal
           Starting volume of 4
       used4 : EpicsSignal
           Flow of 4
       time4 : EpicsSignal
           Estimated depletion time of 4
       start5 : EpicsSignal
           Starting volume of 5
       used5 : EpicsSignal
           Flow of 5
       time5 : EpicsSignal
           Estimated depletion time of 5
       start6 : EpicsSignal
           Starting volume of 6
       used6 : EpicsSignal
           Flow of 6
       time6 : EpicsSignal
           Estimated depletion time of 6
       start7 : EpicsSignal
           Starting volume of 7
       used7 : EpicsSignal
           Flow of 7
       time7 : EpicsSignal
           Estimated depletion time of 7
       start8 : EpicsSignal
           Starting volume of 8
       used8 : EpicsSignal
           Flow of 8
       time8 : EpicsSignal
           Estimated depletion time of 8
       start9 : EpicsSignal
           Starting volume of 9
       used9 : EpicsSignal
           Flow of 9
       time9 : EpicsSignal
           Estimated depletion time of 9
       start10 : EpicsSignal
           Starting volume of 10
       used10 : EpicsSignal
           Flow of 10
       time10 : EpicsSignal
           Estimated depletion time of 10
       '''
    
    integrator_source = FCpt(EpicsSignal, '{self._integrator_source}')
    flow_source = FCpt(EpicsSignal, '{self._flow_source}')
    names = FCpt(EpicsSignal, '{self._names}')
    
    start1 = FCpt(EpicsSignal, '{self._start1}')
    used1 = FCpt(EpicsSignal, '{self._used1}')
    time1 = FCpt(EpicsSignal, '{self._time1}')
    
    start2 = FCpt(EpicsSignal, '{self._start2}')
    used2 = FCpt(EpicsSignal, '{self._used2}')
    time2 = FCpt(EpicsSignal, '{self._time2}')
    
    start3 = FCpt(EpicsSignal, '{self._start3}')
    used3 = FCpt(EpicsSignal, '{self._used3}')
    time3 = FCpt(EpicsSignal, '{self._time3}')
    
    start4 = FCpt(EpicsSignal, '{self._start4}')
    used4 = FCpt(EpicsSignal, '{self._used4}')
    time4 = FCpt(EpicsSignal, '{self._time4}')
    
    start5 = FCpt(EpicsSignal, '{self._start5}')
    used5 = FCpt(EpicsSignal, '{self._used5}')
    time5 = FCpt(EpicsSignal, '{self._time5}')
    
    start6 = FCpt(EpicsSignal, '{self._start6}')
    used6 = FCpt(EpicsSignal, '{self._used6}')
    time6 = FCpt(EpicsSignal, '{self._time6}')
    
    start7 = FCpt(EpicsSignal, '{self._start7}')
    used7 = FCpt(EpicsSignal, '{self._used7}')
    time7 = FCpt(EpicsSignal, '{self._time7}')
    
    start8 = FCpt(EpicsSignal, '{self._start8}')
    used8 = FCpt(EpicsSignal, '{self._used8}')
    time8 = FCpt(EpicsSignal, '{self._time8}')
    
    start9 = FCpt(EpicsSignal, '{self._start9}')
    used9 = FCpt(EpicsSignal, '{self._used9}')
    time9 = FCpt(EpicsSignal, '{self._time9}')
    
    start10 = FCpt(EpicsSignal, '{self._start10}')
    used10 = FCpt(EpicsSignal, '{self._used10}')
    time10 = FCpt(EpicsSignal, '{self._time10}')
    
    def __init__(self, name,
                       integrator_source, flow_source, names,
                       start1, used1, time1,
                       start2, used2, time2,
                       start3, used3, time3,
                       start4, used4, time4,
                       start5, used5, time5,
                       start6, used6, time6,
                       start7, used7, time7,
                       start8, used8, time8,
                       start9, used9, time9,
                       start10, used10, time10, **kwargs):
        
        self._integrator_source = integrator_source
        self._flow_source = flow_source
        self._names = names
        
        self._start1 = start1
        self._used1 = used1
        self._time1 = time1
        
        self._start2 = start2
        self._used2 = used2
        self._time2 = time2
        
        self._start3 = start3
        self._used3 = used3
        self._time3 = time3
        
        self._start4 = start4
        self._used4 = used4
        self._time4 = time4
        
        self._start5 = start5
        self._used5 = used5
        self._time5 = time5
        
        self._start6 = start6
        self._used6 = used6
        self._time6 = time6
        
        self._start7 = start7
        self._used7 = used7
        self._time7 = time7
        
        self._start8 = start8
        self._used8 = used8
        self._time8 = time8
        
        self._start9 = start9
        self._used9 = used9
        self._time9 = time9
        
        self._start10 = start10
        self._used10 = used10
        self._time10 = time10
        
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]



class SDS:
    '''Sample delivery system
        
       Parameters
       ----------
       devices : dict
           A dictionary of dictionaries containing the devices to be made and their PV names
           Key: str
               Type of device to be made. Valid keys are 'selector', 'cooler_shaker', 'hplc',
               'pressure_controller', and 'flow_integrator'
           Value: str dict
               Dictionary of PVs of the device
               
       Attributes
       ----------
       SDS_devices : list
           List containing all the devices that are in the sample delivery system
       '''
    
    SDS_devices = []
    
    def __init__(self, devices):
        
        for device in devices:
            if device == 'selector':
                self.SDS_devices.append(Selector(**devices[device]))
            elif device == 'cooler_shaker':
                self.SDS_devices.append(CoolerShaker(**devices[device]))
            elif device == 'hplc':
                self.SDS_devices.append(HPLC(**devices[device]))
            elif device == 'pressure_controller':
                self.SDS_devices.append(PressureController(**devices[device]))
            elif device == 'flow_integrator':
                self.SDS_devices.append(FlowIntegrator(**devices[device]))
            else:
                print(f'{device} is not a valid device')


class Offaxis(PCDSDetector):
    '''Area detector for Offaxis camera in CXI

    Parameters
    ----------
    port_names : str dict
        A dictionary containing the access port names for the plugins
    prefix : str
        Prefix for the PV name of the camera
    name : str
        Name of the camera
 
    Attributes
    ----------
    ROI : ROIPlugin
        ROI on original rate image
    ROI_stats : StatsPlugin
        Stats on ROI of original rate image
    '''

    ROI = FCpt(ROIPlugin, '{self._ROI_port}')
    ROI_stats = FCpt(StatsPlugin, '{self._ROI_stats_port}')
    ROI_image = FCpt(ImagePlugin, '{self._ROI_image_port}') 
    
    def __init__(self, ROI_port, 
                       ROI_stats_port,
                       ROI_image_port, 
                       prefix, *args, **kwargs):


        self._ROI_port = f'{prefix}:{ROI_port}:'
        self._ROI_stats_port = f'{prefix}:{ROI_stats_port}:'
        self._ROI_image_port = f'{prefix}:{ROI_image_port}:' 

        super().__init__(prefix, *args, **kwargs)
        
        self.ROI_stats.nd_array_port.put(ROI_port)
        self.ROI_image.nd_array_port.put(ROI_port) 

        
        self.ROI.enable.put('Enabled')
        self.ROI_stats.enable.put('Enabled')
        self.ROI_image.enable.put('Enabled') 



class Questar(PCDSDetector):
    '''
    Area detector for Inline Questar Camera in CXI
    
    Parameters
    ----------
    port_names : str dict
        A dictionary containing the access port names for the plugins
    prefix : str
        Prefix for the PV name of the camera
    name : str
        Name of the camera
 
    Attributes
    ----------
    ROI : ROIPlugin
        ROI on original rate image
    ROI_stats : StatsPlugin
        Stats on ROI of original rate image
    '''

    ROI = FCpt(ROIPlugin, '{self._ROI_port}')
    ROI_stats = FCpt(StatsPlugin, '{self._ROI_stats_port}')
    ROI_image = FCpt(ImagePlugin, '{self._ROI_image_port}') 
    
    def __init__(self, ROI_port, 
                       ROI_stats_port,
                       ROI_image_port, 
                       prefix, *args, **kwargs):


        self._ROI_port = f'{prefix}:{ROI_port}:'
        self._ROI_stats_port = f'{prefix}:{ROI_stats_port}:'
        self._ROI_image_port = f'{prefix}:{ROI_image_port}:' 

        super().__init__(prefix, *args, **kwargs)
        
        self.ROI_stats.nd_array_port.put(ROI_port)
        self.ROI_image.nd_array_port.put(ROI_port) 

        
        self.ROI.enable.put('Enabled')
        self.ROI_stats.enable.put('Enabled')
        self.ROI_image.enable.put('Enabled') 


class Parameters(Device):
    '''
    Contains EPICS PVs used for jet tracking
    
    Attributes
    ----------
    cam_x : EpicsSignal
        x-coordinate of camera position in mm
    cam_y : EpicsSignal
        y-coordinate of camera position in mm
    pxsize : EpicsSignal
        size of pixel in mm
    cam_roll : EpicsSignal
        rotation of camera about z axis in radians
    beam_x : EpicsSignal
        x-coordinate of x-ray beam in mm (usually 0)
    beam_y : EpicsSignal
        y-coordinate of x-ray beam in mm (usually 0)
    beam_x_px : EpicsSignal
        x-coordinate of x-ray beam in camera image in pixels
    beam_y_px : EpicsSignal
        y-coordinate of x-ray beam in camera image in pixels
    nozzle_x : EpicsSignal
        x-coordinate of nozzle in mm
    nozzle_y : EpicsSignal
        y-coordinate of nozzle in mm
    nozzle_xwidth : EpicsSignal
        width of nozzle in mm
    jet_x : EpicsSignal
        distance from sample jet to x-ray beam in mm
    jet_roll : EpicsSignal
        rotation of sample jet about z axis in radians
    state : EpicsSignal
        dictionary of strings
    '''

    cam_x = FCpt(EpicsSignal, '{self._cam_x}')
    cam_y = FCpt(EpicsSignal, '{self._cam_y}')
    pxsize = FCpt(EpicsSignal, '{self._pxsize}')
    cam_roll = FCpt(EpicsSignal, '{self._cam_roll}')
    beam_x = FCpt(EpicsSignal, '{self._beam_x}')
    beam_y = FCpt(EpicsSignal, '{self._beam_y}')
    beam_x_px = FCpt(EpicsSignal, '{self._beam_x_px}')
    beam_y_px = FCpt(EpicsSignal, '{self._beam_y_px}')
    nozzle_x = FCpt(EpicsSignal, '{self._nozzle_x}')
    nozzle_y = FCpt(EpicsSignal, '{self._nozzle_y}')
    nozzle_xwidth = FCpt(EpicsSignal, '{self._nozzle_xwidth}')
    jet_x = FCpt(EpicsSignal, '{self._jet_x}')
    jet_roll = FCpt(EpicsSignal, '{self._jet_roll}')
    state = FCpt(EpicsSignal, '{self._state}')
    jet_counter = FCpt(EpicsSignal, '{self._jet_counter}')
    jet_reprate = FCpt(EpicsSignal, '{self._jet_reprate}')
    nozzle_counter = FCpt(EpicsSignal, '{self._nozzle_counter}')
    nozzle_reprate = FCpt(EpicsSignal, '{self._nozzle_reprate}')

    def __init__(self, prefix, name, **kwargs):
        
        self._cam_x = f'{prefix}:CAM_X'
        self._cam_y = f'{prefix}:CAM_Y'
        self._pxsize = f'{prefix}:PXSIZE'
        self._cam_roll = f'{prefix}:CAM_ROLL'
        self._beam_x = f'{prefix}:BEAM_X'
        self._beam_y = f'{prefix}:BEAM_Y'
        self._beam_x_px = f'{prefix}:BEAM_X_PX'
        self._beam_y_px = f'{prefix}:BEAM_Y_PX'
        self._nozzle_x = f'{prefix}:NOZZLE_X'
        self._nozzle_y = f'{prefix}:NOZZLE_Y'
        self._nozzle_xwidth = f'{prefix}:NOZZLE_XWIDTH'
        self._jet_x = f'{prefix}:JET_X'
        self._jet_roll = f'{prefix}:JET_ROLL'
        self._state = f'{prefix}:STATE'
        self._jet_counter = f'{prefix}:JET_Counter'
        self._jet_reprate = f'{prefix}:JET_RepRate'
        self._nozzle_counter = f'{prefix}:NOZZLE_Counter'
        self._nozzle_reprate = f'{prefix}:NOZZLE_RepRate'
 
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]



class OffaxisParams(Device):
    '''
    Contains EPICS PVs used with Offaxis camera for jet tracking
    
    Attributes
    ----------
    cam_z : EpicsSignal
        z-coordinate of camera position in mm
    cam_y : EpicsSignal
        y-coordinate of camera position in mm
    pxsize : EpicsSignal
        size of pixel in mm
    cam_pitch : EpicsSignal
        rotation of camera about x axis in radians
    beam_z : EpicsSignal
        z-coordinate of x-ray beam in mm (usually 0)
    beam_y : EpicsSignal
        y-coordinate of x-ray beam in mm (usually 0)
    beam_z_px : EpicsSignal
        z-coordinate of x-ray beam in camera image in pixels
    beam_y_px : EpicsSignal
        y-coordinate of x-ray beam in camera image in pixels
    nozzle_z : EpicsSignal
        z-coordinate of nozzle in mm
    nozzle_y : EpicsSignal
        y-coordinate of nozzle in mm
    nozzle_zwidth : EpicsSignal
        width of nozzle in mm
    jet_z : EpicsSignal
        distance from sample jet to x-ray beam in mm
    jet_pitch : EpicsSignal
        rotation of sample jet about z axis in radians
    state : EpicsSignal
        dictionary of string
    '''

    cam_z = FCpt(EpicsSignal, '{self._cam_z}')
    cam_y = FCpt(EpicsSignal, '{self._cam_y}')
    pxsize = FCpt(EpicsSignal, '{self._pxsize}')
    cam_pitch = FCpt(EpicsSignal, '{self._cam_pitch}')
    beam_z = FCpt(EpicsSignal, '{self._beam_z}')
    beam_y = FCpt(EpicsSignal, '{self._beam_y}')
    beam_z_px = FCpt(EpicsSignal, '{self._beam_z_px}')
    beam_y_px = FCpt(EpicsSignal, '{self._beam_y_px}')
    nozzle_z = FCpt(EpicsSignal, '{self._nozzle_z}')
    nozzle_y = FCpt(EpicsSignal, '{self._nozzle_y}')
    nozzle_zwidth = FCpt(EpicsSignal, '{self._nozzle_zwidth}')
    jet_z = FCpt(EpicsSignal, '{self._jet_z}')
    jet_pitch = FCpt(EpicsSignal, '{self._jet_pitch}')
    state = FCpt(EpicsSignal, '{self._state}')
    jet_counter = FCpt(EpicsSignal, '{self._jet_counter}')
    jet_reprate = FCpt(EpicsSignal, '{self._jet_reprate}')
    nozzle_counter = FCpt(EpicsSignal, '{self._nozzle_counter}')
    nozzle_reprate = FCpt(EpicsSignal, '{self._nozzle_reprate}')

    def __init__(self, prefix, name, **kwargs):
        
        self._cam_z = f'{prefix}:CAM_Z'
        self._cam_y = f'{prefix}:CAM_Y'
        self._pxsize = f'{prefix}:PXSIZE'
        self._cam_pitch = f'{prefix}:CAM_PITCH'
        self._beam_z = f'{prefix}:BEAM_Z'
        self._beam_y = f'{prefix}:BEAM_Y'
        self._beam_z_px = f'{prefix}:BEAM_Z_PX'
        self._beam_y_px = f'{prefix}:BEAM_Y_PX'
        self._nozzle_z = f'{prefix}:NOZZLE_Z'
        self._nozzle_y = f'{prefix}:NOZZLE_Y'
        self._nozzle_zwidth = f'{prefix}:NOZZLE_ZWIDTH'
        self._jet_z = f'{prefix}:JET_Z'
        self._jet_pitch = f'{prefix}:JET_PITCH'
        self._state = f'{prefix}:STATE'
        self._jet_counter = f'{prefix}:JET_Counter'
        self._jet_reprate = f'{prefix}:JET_RepRate'
        self._nozzle_counter = f'{prefix}:NOZZLE_Counter'
        self._nozzle_reprate = f'{prefix}:NOZZLE_RepRate'
 
        super().__init__(name=name, **kwargs)

class Control(Device):
    '''
    Contains EPICS PVs used for jet tracking control
    '''

    re_state = FCpt(EpicsSignal, '{self._re_state}')
    beam_state = FCpt(EpicsSignal, '{self._beam_state}')
    injector_state = FCpt(EpicsSignal, '{self._injector_state}')
    beam_trans = FCpt(EpicsSignal, '{self._beam_trans}')
    beam_pulse_energy = FCpt(EpicsSignal, '{self._beam_pulse_energy}')
    beam_e_thresh = FCpt(EpicsSignal, '{self._beam_e_thresh}')
    xstep_size = FCpt(EpicsSignal, '{self._xstep_size}')
    xscan_min = FCpt(EpicsSignal, '{self._xscan_min}')
    xscan_max = FCpt(EpicsSignal, '{self._xscan_max}')
    bounce_width = FCpt(EpicsSignal, '{self._bounce_width}')
    xmin = FCpt(EpicsSignal, '{self._xmin}')
    xmax = FCpt(EpicsSignal, '{self._xmax}')

    def __init__(self, prefix, name, **kwargs):
        
        self._re_state = f'{prefix}:RE:STATE'
        self._beam_state = f'{prefix}:BEAM:STATE'
        self._injector_state = f'{prefix}:INJECTOR:STATE'
        self._beam_trans = f'{prefix}:BEAM:TRANS'
        self._beam_pulse_energy = f'{prefix}:BEAM:PULSE_ENERGY'
        self._beam_e_thresh = f'{prefix}:BEAM:E_THRESH'
        self._xstep_size = f'{prefix}:INJECTOR:XSTEP_SIZE'
        self._xscan_min = f'{prefix}:INJECTOR:XSCAN_MIN'
        self._xscan_max = f'{prefix}:INJECTOR:XSCAN_MAX'
        self._bounce_width = f'{prefix}:INJECTOR:BOUNCE_WIDTH'
        self._xmin = f'{prefix}:INJECTOR:XMIN'
        self._xmax = f'{prefix}:INJECTOR:XMAX'
 
        super().__init__(name=name, **kwargs)

    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]



class Diffract(Device):
    '''
    Contains EPICS PVs used for shared memory X-ray Diffraction detector
    used in jet trakcing.
    
    Attributes
    ----------
    model_adu : EpicsSignal
        Total detector model ADU 
    model_adu_err : EpicsSignal
        Total detector model ADU error estimate 
    model_intensity : EpicsSignal
        Diffraction model intensity waveform 
    model_intensity_err : EpicsSignal
        Diffraction model intensity waveform 
    model_xaxis : EpicsSignal
        Diffraction model xaxis waveform 
    psd_amplitude : EpicsSignal
        Diffraction periodogram Frequency analysis amplitude
    psd_amp_array : EpicsSignal
        Diffraction periodogram Frequency analysis amplitude array
    psd_amp_wf : EpicsSignal
        Diffraction periodogram Frequency analysis waveform array
    psd_counter : EpicsSignal
        Diffraction periodogram event counter 
    psd_events : EpicsSignal
        Diffraction periodogram 
    psd_frequency : EpicsSignal
        Diffraction periodogram fundamental frequency
    psd_freq_min : EpicsSignal
        Minimum frequency for periodogram calcs 
    psd_freq_wf : EpicsSignal
        Diffraction periodogram frequency waveform
    psd_rate : EpicsSignal
        Event frequency for periodogram 
    psd_resolution : EpicsSignal
        Resultion to smooth over for periodogra 
    psd_reprate : EpicsSignal
        Diffraction periodogram event counter 
    ring_adu : EpicsSignal
        Ring ADU 
    ring_adu_err : EpicsSignal
        Ring ADU error estimate 
    ring_counter : EpicsSignal
        Diffraction ring intensity event counte 
    ring_intensity : EpicsSignal
        Intensity of diffraction ring 
    ring_intensity_err : EpicsSignal
        Error in intensity of diffraction ring 
    ring_radius : EpicsSignal
        Radius of diffraction ring 
    ring_radius_err : EpicsSignal
        Error in Radius of diffraction ring 
    ring_reprate : EpicsSignal
        Diffraction ring intensity event counte 
    ring_width : EpicsSignal
        Width of diffraction ring 
    ring_width_err : EpicsSignal
        Width error estimate of diffraction rin 
    state : EpicsSignal
        State of diffraction analysis     
    stats_counter : EpicsSignal
        Diffraction stats event counter 
    stats_max : EpicsSignal
        Max Diffraction Statistic 
    stats_mean : EpicsSignal
        Mean Diffraction Statistic 
    stats_min : EpicsSignal
        Min Diffraction Statistic 
    stats_reprate : EpicsSignal
        Diffraction stats event counter 
    stats_std : EpicsSignal
        Std Diffraction Statistic 
    streak_calc_rate : EpicsSignal
        Rate of streak calculation
    streak_counter : EpicsSignal
        Diffraction streak event counter 
    streak_fraction : EpicsSignal
        Fraction of events with diffraction streak
    streak_intensity : EpicsSignal
        Intensity of diffraction streak 
    streak_intensity_err : EpicsSignal
        Error in Intensity of diffraction streak 
    streak_phi : EpicsSignal
        Angle of diffraction streak 
    streak_phi_err : EpicsSignal
        Error in Angle of diffraction streak 
    streak_reprate : EpicsSignal
        Diffraction streak event counter 
    streak_width : EpicsSignal
        Width of diffraction streak 
    streak_width_err : EpicsSignal
        Error in Width of diffraction streak 
    streak_x : EpicsSignal
        Event X origin of diffraction streak 
    streak_x_err : EpicsSignal
        Error in Event X origin of diffraction streak 
    streak_y : EpicsSignal
        Event Y origin of diffraction streak 
    streak_y_err : EpicsSignal
        Error in Event Y origin of diffraction streak 
    total_adu : EpicsSignal
        Total detector ADU 
    total_adu_err : EpicsSignal
        Total detector ADU error estimate 
    total_counter : EpicsSignal
        Total counter     
    total_reprate : EpicsSignal
        Diffraction total intensity calc rate 
    x0 : EpicsSignal
        Nominal X origin of diffraction 
    x0_err : EpicsSignal
        Error in Nominal X origin of diffraction 
    y0 : EpicsSignal
        Nominal Y origin of diffraction 
    y0_err : EpicsSignal
        Error in Nominal Y origin of diffraction 

    '''

    total_counter = FCpt(EpicsSignal, '{self._total_counter}')
    total_reprate = FCpt(EpicsSignal, '{self._total_reprate}')
    ring_counter = FCpt(EpicsSignal, '{self._ring_counter}')
    ring_reprate = FCpt(EpicsSignal, '{self._ring_reprate}')
    psd_counter = FCpt(EpicsSignal, '{self._psd_counter}')
    psd_reprate = FCpt(EpicsSignal, '{self._psd_reprate}')
    stats_counter = FCpt(EpicsSignal, '{self._stats_counter}')
    stats_reprate = FCpt(EpicsSignal, '{self._stats_reprate}')
    streak_counter = FCpt(EpicsSignal, '{self._streak_counter}')
    streak_reprate = FCpt(EpicsSignal, '{self._streak_reprate}')
    cspad_sum = FCpt(EpicsSignal, '{self._cspad_sum}')
    streak_fraction = FCpt(EpicsSignal, '{self._streak_fraction}')
    stats_mean = FCpt(EpicsSignal, '{self._stats_mean}')
    stats_std = FCpt(EpicsSignal, '{self._stats_std}')
    stats_min = FCpt(EpicsSignal, '{self._stats_min}')
    stats_max = FCpt(EpicsSignal, '{self._stats_max}')
    psd_frequency = FCpt(EpicsSignal, '{self._psd_frequency}')
    psd_amplitude = FCpt(EpicsSignal, '{self._psd_amplitude}')
    psd_rate = FCpt(EpicsSignal, '{self._psd_rate}')
    psd_events = FCpt(EpicsSignal, '{self._psd_events}')
    psd_resolution = FCpt(EpicsSignal, '{self._psd_resolution}')
    psd_freq_min = FCpt(EpicsSignal, '{self._psd_freq_min}')
    psd_amp_wf = FCpt(EpicsSignal, '{self._psd_amp_wf}')
    psd_freq_wf = FCpt(EpicsSignal, '{self._psd_freq_wf}')
    psd_amp_array = FCpt(EpicsSignal, '{self._psd_amp_array}')
    state = FCpt(EpicsSignal, '{self._state}')

    def __init__(self, prefix, name, **kwargs):
        
        self._total_counter = f'{prefix}:TOTAL_Counter'
        self._total_reprate = f'{prefix}:TOTAL_RepRate'
        self._ring_counter = f'{prefix}:RING_Counter'
        self._ring_reprate = f'{prefix}:RING_RepRate'
        self._psd_counter = f'{prefix}:PSD_Counter'
        self._psd_reprate = f'{prefix}:PSD_RepRate'
        self._stats_counter = f'{prefix}:STATS_Counter'
        self._stats_reprate = f'{prefix}:STATS_RepRate'
        self._streak_counter = f'{prefix}:STREAK_Counter'
        self._streak_reprate = f'{prefix}:STREAK_RepRate'
        self._cspad_sum = f'{prefix}:TOTAL_ADU'
        self._streak_fraction = f'{prefix}:STREAK_FRACTION'
        self._stats_mean = f'{prefix}:STATS_MEAN'
        self._stats_std = f'{prefix}:STATS_STD'
        self._stats_min = f'{prefix}:STATS_MIN'
        self._stats_max = f'{prefix}:STATS_MAX'
        self._psd_frequency = f'{prefix}:PSD_FREQUENCY'
        self._psd_amplitude = f'{prefix}:PSD_AMPLITUDE'
        self._psd_rate = f'{prefix}:PSD_RATE'
        self._psd_events = f'{prefix}:PSD_EVENTS'
        self._psd_resolution = f'{prefix}:PSD_RESOLUTION'
        self._psd_freq_min = f'{prefix}:PSD_FREQ_MIN'
        self._psd_freq_wf = f'{prefix}:PSD_FREQ_WF'
        self._psd_amp_wf = f'{prefix}:PSD_AMP_WF'
        self._psd_amp_array = f'{prefix}:PSD_AMP_ARRAY'
        self._state = f'{prefix}:STATE'
       
        super().__init__(name=name, **kwargs)
    
    @property
    def _descriptions(self):
        from ophyd.signal import EpicsSignal
        adesc = {}
        for name, signal in self._signals.items():
            adesc[name] = EpicsSignal(signal._read_pv.pvname+'.DESC').get()

        return adesc

    @property
    def table(self, attrs=['value', 'units', 'desc']):
        """
        Return table of injector settings.
        """
        adesc = self._descriptions
        import pandas as pd
        atable = {}
        for name, signal in sorted(self._signals.items()):
            atable[name] = {
                    'value': signal._read_pv.value,
                    'units': signal._read_pv.units,
                    'desc': adesc.get(name),
                    }

        return pd.DataFrame(atable).T[attrs]


