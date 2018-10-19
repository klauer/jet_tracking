#!/usr/bin/env python3
from caproto.server import (pvproperty, get_pv_pair_wrapper, PVGroup, SubGroup,
                            ioc_arg_parser, run)


pvproperty_with_rbv = get_pv_pair_wrapper(setpoint_suffix='',
                                          readback_suffix='_RBV')



# -- InjectorGroup --

class InjectorGroup(PVGroup):

    class IMSGroup(PVGroup):
        user_readback = pvproperty(name='.RBV', dtype=float, value=-2.100830078125, read_only=True)
        user_setpoint = pvproperty(name='.VAL', dtype=float, value=-2.101318359375, doc='PI X')
        user_offset = pvproperty(name='.OFF', dtype=float, value=0.0)
        user_offset_dir = pvproperty(name='.DIR', dtype=int, value=1)
        offset_freeze_switch = pvproperty(name='.FOFF', dtype=int, value=1)
        set_use_switch = pvproperty(name='.SET', dtype=int, value=0)
        velocity = pvproperty(name='.VELO', dtype=float, value=1.25)
        acceleration = pvproperty(name='.ACCL', dtype=float, value=1.0)
        motor_egu = pvproperty(name='.EGU', dtype=str, value='m')
        motor_is_moving = pvproperty(name='.MOVN', dtype=int, value=0, read_only=True)
        motor_done_move = pvproperty(name='.DMOV', dtype=int, value=1, read_only=True)
        high_limit_switch = pvproperty(name='.HLS', dtype=int, value=0)
        low_limit_switch = pvproperty(name='.LLS', dtype=int, value=0)
        # direction_of_travel = pvproperty(name=None, dtype=int, value=0)
        motor_stop = pvproperty(name='.STOP', dtype=int, value=0)
        home_forward = pvproperty(name='.HOMF', dtype=int, value=0)
        home_reverse = pvproperty(name='.HOMR', dtype=int, value=0)
        low_soft_limit = pvproperty(name='.LLM', dtype=float, value=-10.0)
        high_soft_limit = pvproperty(name='.HLM', dtype=float, value=10.0)
        disabled = pvproperty(name='.DISP', dtype=int, value=0)
        description = pvproperty(name='.DESC', dtype=str, value='P')
        motor_spg = pvproperty(name='.SPG', dtype=int, value=2)
        reinit_command = pvproperty(name='.RINI', dtype=int, value=0)
        bit_status = pvproperty(name='.MSTA', dtype=float, value=274.0, read_only=True)
        seq_seln = pvproperty(name=':SEQ_SELN', dtype=int, value=48, doc='Sequencer SELN Mask')
        error_severity = pvproperty(name='.SEVR', dtype=int, value=0)
        part_number = pvproperty(name='.PN', dtype=str, value='M', read_only=True)
        velocity_base = pvproperty(name='.VBAS', dtype=float, value=0.00625)
        velocity_max = pvproperty(name='.VMAX', dtype=float, value=25.0)

    coarseX = SubGroup(IMSGroup, prefix='{coarseX}')
    coarseY = SubGroup(IMSGroup, prefix='{coarseY}')
    coarseZ = SubGroup(IMSGroup, prefix='{coarseZ}')
    fineX = SubGroup(IMSGroup, prefix='{fineX}')
    fineY = SubGroup(IMSGroup, prefix='{fineY}')
    fineZ = SubGroup(IMSGroup, prefix='{fineZ}')


# -- QuestarGroup --

class QuestarGroup(PVGroup):
    # configuration_names = pvproperty(name=None, dtype=str, value='')

    class CamBaseGroup(PVGroup):
        # configuration_names = pvproperty(name=None, dtype=str, value='')
        array_counter = pvproperty_with_rbv(name='ArrayCounter', dtype=int, value=58687833)
        array_rate = pvproperty(name='ArrayRate_RBV', dtype=float, value=118.0, read_only=True)
        asyn_io = pvproperty(name='AsynIO', dtype=int, value=0)
        nd_attributes_file = pvproperty(name='NDAttributesFile', dtype=str, max_length=256)
        pool_alloc_buffers = pvproperty(name='PoolAllocBuffers', dtype=int, value=4, read_only=True)
        pool_free_buffers = pvproperty(name='PoolFreeBuffers', dtype=int, value=2, read_only=True)
        pool_max_buffers = pvproperty(name='PoolMaxBuffers', dtype=int, value=0, read_only=True)
        pool_max_mem = pvproperty(name='PoolMaxMem', dtype=float, value=0.0, read_only=True)
        pool_used_buffers = pvproperty(
            name='PoolUsedBuffers', dtype=float, value=2.0, read_only=True)
        pool_used_mem = pvproperty(name='PoolUsedMem', dtype=float, value=8.0, read_only=True)
        port_name = pvproperty(name='PortName_RBV', dtype=str, value='C', read_only=True)
        acquire = pvproperty_with_rbv(name='Acquire', dtype=int, value=1)
        acquire_period = pvproperty_with_rbv(name='AcquirePeriod', dtype=float, value=0.1)
        acquire_time = pvproperty_with_rbv(name='AcquireTime', dtype=float, value=0.00809)
        array_callbacks = pvproperty_with_rbv(name='ArrayCallbacks', dtype=int, value=1)

        class CamBaseArraySizeGroup(PVGroup):
            array_size_x = pvproperty(name='ArraySizeX_RBV', dtype=int, value=1024, read_only=True)
            array_size_y = pvproperty(name='ArraySizeY_RBV', dtype=int, value=1024, read_only=True)
            array_size_z = pvproperty(name='ArraySizeZ_RBV', dtype=int, value=0, read_only=True)

        array_size = SubGroup(CamBaseArraySizeGroup, prefix='')

        array_size_bytes = pvproperty(
            name='ArraySize_RBV', dtype=int, value=1048576, read_only=True)
        bin_x = pvproperty_with_rbv(name='BinX', dtype=int, value=1)
        bin_y = pvproperty_with_rbv(name='BinY', dtype=int, value=1)
        color_mode = pvproperty_with_rbv(name='ColorMode', dtype=int, value=0)
        data_type = pvproperty_with_rbv(name='DataType', dtype=int, value=3)
        detector_state = pvproperty(name='DetectorState_RBV', dtype=int, value=7, read_only=True)
        frame_type = pvproperty_with_rbv(name='FrameType', dtype=int, value=0)
        gain = pvproperty_with_rbv(name='Gain', dtype=float, value=7.88)
        image_mode = pvproperty_with_rbv(name='ImageMode', dtype=int, value=2)
        manufacturer = pvproperty(name='Manufacturer_RBV', dtype=str, value='A', read_only=True)

        class CamBaseMaxSizeGroup(PVGroup):
            max_size_x = pvproperty(name='MaxSizeX_RBV', dtype=int, value=1024, read_only=True)
            max_size_y = pvproperty(name='MaxSizeY_RBV', dtype=int, value=1024, read_only=True)

        max_size = SubGroup(CamBaseMaxSizeGroup, prefix='')

        min_x = pvproperty_with_rbv(name='MinX', dtype=int, value=0)
        min_y = pvproperty_with_rbv(name='MinY', dtype=int, value=0)
        model = pvproperty(name='Model_RBV', dtype=str, value='1', read_only=True)
        num_exposures = pvproperty_with_rbv(name='NumExposures', dtype=int, value=1)
        num_exposures_counter = pvproperty(
            name='NumExposuresCounter_RBV', dtype=int, value=0, read_only=True)
        num_images = pvproperty_with_rbv(name='NumImages', dtype=int, value=1)
        num_images_counter = pvproperty(
            name='NumImagesCounter_RBV', dtype=int, value=61067873, read_only=True)
        read_status = pvproperty(name='ReadStatus', dtype=int, value=1)

        class CamBaseReverseGroup(PVGroup):
            reverse_x = pvproperty_with_rbv(name='ReverseX', dtype=int, value=0)
            reverse_y = pvproperty_with_rbv(name='ReverseY', dtype=int, value=0)

        reverse = SubGroup(CamBaseReverseGroup, prefix='')

        shutter_close_delay = pvproperty_with_rbv(name='ShutterCloseDelay', dtype=float, value=0.0)
        shutter_close_epics = pvproperty(name='ShutterCloseEPICS', dtype=float, value=0.0)
        shutter_control = pvproperty_with_rbv(name='ShutterControl', dtype=int, value=0)
        shutter_control_epics = pvproperty(name='ShutterControlEPICS', dtype=int, value=0)
        shutter_fanout = pvproperty(name='ShutterFanout', dtype=int, value=0)
        shutter_mode = pvproperty_with_rbv(name='ShutterMode', dtype=int, value=0)
        shutter_open_delay = pvproperty_with_rbv(name='ShutterOpenDelay', dtype=float, value=0.0)
        shutter_open_epics = pvproperty(name='ShutterOpenEPICS', dtype=float, value=0.0)
        shutter_status_epics = pvproperty(
            name='ShutterStatusEPICS_RBV', dtype=int, value=0, read_only=True)
        shutter_status = pvproperty(name='ShutterStatus_RBV', dtype=int, value=0, read_only=True)

        class CamBaseSizeGroup(PVGroup):
            size_x = pvproperty_with_rbv(name='SizeX', dtype=int, value=1024)
            size_y = pvproperty_with_rbv(name='SizeY', dtype=int, value=1024)

        size = SubGroup(CamBaseSizeGroup, prefix='')

        status_message = pvproperty(
            name='StatusMessage_RBV', dtype=str, max_length=256, read_only=True)
        string_from_server = pvproperty(
            name='StringFromServer_RBV', dtype=str, max_length=256, read_only=True)
        string_to_server = pvproperty(
            name='StringToServer_RBV', dtype=str, max_length=256, read_only=True)
        temperature = pvproperty_with_rbv(name='Temperature', dtype=float, value=25.0)
        temperature_actual = pvproperty(name='TemperatureActual', dtype=float, value=0.0)
        time_remaining = pvproperty(
            name='TimeRemaining_RBV', dtype=float, value=0.0, read_only=True)
        trigger_mode = pvproperty_with_rbv(name='TriggerMode', dtype=int, value=0)

    cam = SubGroup(CamBaseGroup, prefix='{prefix}:')


    class ImagePluginGroup(PVGroup):
        # configuration_names = pvproperty(name=None, dtype=str, value='')
        array_counter = pvproperty_with_rbv(name='ArrayCounter', dtype=int, value=4686211)
        array_rate = pvproperty(name='ArrayRate_RBV', dtype=float, value=10.0, read_only=True)
        asyn_io = pvproperty(name='AsynIO', dtype=int, value=0)
        nd_attributes_file = pvproperty(name='NDAttributesFile', dtype=str, max_length=256)
        pool_alloc_buffers = pvproperty(name='PoolAllocBuffers', dtype=int, value=1, read_only=True)
        pool_free_buffers = pvproperty(name='PoolFreeBuffers', dtype=int, value=1, read_only=True)
        pool_max_buffers = pvproperty(name='PoolMaxBuffers', dtype=int, value=-1, read_only=True)
        pool_max_mem = pvproperty(name='PoolMaxMem', dtype=float, value=0.0, read_only=True)
        pool_used_buffers = pvproperty(
            name='PoolUsedBuffers', dtype=float, value=0.0, read_only=True)
        pool_used_mem = pvproperty(name='PoolUsedMem', dtype=float, value=2.0, read_only=True)
        port_name = pvproperty(name='PortName_RBV', dtype=str, value='I', read_only=True)
        # asyn_pipeline_config = pvproperty(name=None, dtype=str, value='')

        class ImagePluginArraySizeGroup(PVGroup):
            height = pvproperty(name='ArraySize1_RBV', dtype=int, value=512, read_only=True)
            width = pvproperty(name='ArraySize0_RBV', dtype=int, value=512, read_only=True)
            depth = pvproperty(name='ArraySize2_RBV', dtype=int, value=0, read_only=True)

        array_size = SubGroup(ImagePluginArraySizeGroup, prefix='')

        bayer_pattern = pvproperty(name='BayerPattern_RBV', dtype=int, value=0, read_only=True)
        blocking_callbacks = pvproperty_with_rbv(name='BlockingCallbacks', dtype=str, value='N')
        color_mode = pvproperty(name='ColorMode_RBV', dtype=int, value=0, read_only=True)
        data_type = pvproperty(name='DataType_RBV', dtype=str, value='U', read_only=True)

        class ImagePluginDimSaGroup(PVGroup):
            dim0 = pvproperty(name='Dim0SA', dtype=int, max_length=10)
            dim1 = pvproperty(name='Dim1SA', dtype=int, max_length=10)
            dim2 = pvproperty(name='Dim2SA', dtype=int, max_length=10)

        dim_sa = SubGroup(ImagePluginDimSaGroup, prefix='')

        dimensions = pvproperty(name='Dimensions_RBV', dtype=int, max_length=10, read_only=True)
        dropped_arrays = pvproperty_with_rbv(name='DroppedArrays', dtype=int, value=0)
        enable = pvproperty_with_rbv(name='EnableCallbacks', dtype=float, value=1.0)
        min_callback_time = pvproperty_with_rbv(name='MinCallbackTime', dtype=float, value=0.1)
        nd_array_address = pvproperty_with_rbv(name='NDArrayAddress', dtype=int, value=0)
        nd_array_port = pvproperty_with_rbv(name='NDArrayPort', dtype=str, value='I')
        ndimensions = pvproperty(name='NDimensions_RBV', dtype=int, value=2, read_only=True)
        plugin_type = pvproperty(name='PluginType_RBV', dtype=str, value='N', read_only=True)
        queue_free = pvproperty(name='QueueFree', dtype=int, value=10)
        queue_free_low = pvproperty(name='QueueFreeLow', dtype=float, value=2.5)
        queue_size = pvproperty(name='QueueSize', dtype=int, value=10)
        queue_use = pvproperty(name='QueueUse', dtype=float, value=0.0)
        queue_use_high = pvproperty(name='QueueUseHIGH', dtype=float, value=7.5)
        queue_use_hihi = pvproperty(name='QueueUseHIHI', dtype=float, value=10.0)
        time_stamp = pvproperty(
            name='TimeStamp_RBV', dtype=float, value=1540232412.8056138, read_only=True)
        unique_id = pvproperty(name='UniqueId_RBV', dtype=int, value=45240, read_only=True)
        array_data = pvproperty(name='ArrayData', dtype=int, max_length=1048576)

    image = SubGroup(ImagePluginGroup, prefix='{prefix}:IMAGE2:')


    class StatsPluginGroup(PVGroup):
        # configuration_names = pvproperty(name=None, dtype=str, value='')
        array_counter = pvproperty_with_rbv(name='ArrayCounter', dtype=int, value=0)
        array_rate = pvproperty(name='ArrayRate_RBV', dtype=float, value=0.0, read_only=True)
        asyn_io = pvproperty(name='AsynIO', dtype=int, value=0)
        nd_attributes_file = pvproperty(name='NDAttributesFile', dtype=str, max_length=256)
        pool_alloc_buffers = pvproperty(name='PoolAllocBuffers', dtype=int, value=0, read_only=True)
        pool_free_buffers = pvproperty(name='PoolFreeBuffers', dtype=int, value=0, read_only=True)
        pool_max_buffers = pvproperty(name='PoolMaxBuffers', dtype=int, value=0, read_only=True)
        pool_max_mem = pvproperty(name='PoolMaxMem', dtype=float, value=0.0, read_only=True)
        pool_used_buffers = pvproperty(
            name='PoolUsedBuffers', dtype=float, value=0.0, read_only=True)
        pool_used_mem = pvproperty(name='PoolUsedMem', dtype=float, value=0.0, read_only=True)
        port_name = pvproperty(name='PortName_RBV', dtype=str, value='S', read_only=True)
        # asyn_pipeline_config = pvproperty(name=None, dtype=str, value='')

        class StatsPluginArraySizeGroup(PVGroup):
            height = pvproperty(name='ArraySize1_RBV', dtype=int, value=0, read_only=True)
            width = pvproperty(name='ArraySize0_RBV', dtype=int, value=0, read_only=True)
            depth = pvproperty(name='ArraySize2_RBV', dtype=int, value=0, read_only=True)

        array_size = SubGroup(StatsPluginArraySizeGroup, prefix='')

        bayer_pattern = pvproperty(name='BayerPattern_RBV', dtype=int, value=0, read_only=True)
        blocking_callbacks = pvproperty_with_rbv(name='BlockingCallbacks', dtype=str, value='N')
        color_mode = pvproperty(name='ColorMode_RBV', dtype=int, value=0, read_only=True)
        data_type = pvproperty(name='DataType_RBV', dtype=str, value='U', read_only=True)

        class StatsPluginDimSaGroup(PVGroup):
            dim0 = pvproperty(name='Dim0SA', dtype=int, max_length=10)
            dim1 = pvproperty(name='Dim1SA', dtype=int, max_length=10)
            dim2 = pvproperty(name='Dim2SA', dtype=int, max_length=10)

        dim_sa = SubGroup(StatsPluginDimSaGroup, prefix='')

        dimensions = pvproperty(name='Dimensions_RBV', dtype=int, max_length=10, read_only=True)
        dropped_arrays = pvproperty_with_rbv(name='DroppedArrays', dtype=int, value=0)
        enable = pvproperty_with_rbv(name='EnableCallbacks', dtype=float, value=0.0)
        min_callback_time = pvproperty_with_rbv(name='MinCallbackTime', dtype=float, value=0.0)
        nd_array_address = pvproperty_with_rbv(name='NDArrayAddress', dtype=int, value=0)
        nd_array_port = pvproperty_with_rbv(name='NDArrayPort', dtype=str, value='C')
        ndimensions = pvproperty(name='NDimensions_RBV', dtype=int, value=0, read_only=True)
        plugin_type = pvproperty(name='PluginType_RBV', dtype=str, value='N', read_only=True)
        queue_free = pvproperty(name='QueueFree', dtype=int, value=5)
        queue_free_low = pvproperty(name='QueueFreeLow', dtype=float, value=1.25)
        queue_size = pvproperty(name='QueueSize', dtype=int, value=5)
        queue_use = pvproperty(name='QueueUse', dtype=float, value=0.0)
        queue_use_high = pvproperty(name='QueueUseHIGH', dtype=float, value=3.75)
        queue_use_hihi = pvproperty(name='QueueUseHIHI', dtype=float, value=5.0)
        time_stamp = pvproperty(name='TimeStamp_RBV', dtype=float, value=0.0, read_only=True)
        unique_id = pvproperty(name='UniqueId_RBV', dtype=int, value=0, read_only=True)
        bgd_width = pvproperty_with_rbv(name='BgdWidth', dtype=int, value=1)
        centroid_threshold = pvproperty_with_rbv(name='CentroidThreshold', dtype=float, value=1.0)

        class StatsPluginCentroidGroup(PVGroup):
            x = pvproperty(name='CentroidX_RBV', dtype=float, value=0.0, read_only=True)
            y = pvproperty(name='CentroidY_RBV', dtype=float, value=0.0, read_only=True)

        centroid = SubGroup(StatsPluginCentroidGroup, prefix='')

        compute_centroid = pvproperty_with_rbv(name='ComputeCentroid', dtype=str, value='N')
        compute_histogram = pvproperty_with_rbv(name='ComputeHistogram', dtype=str, value='N')
        compute_profiles = pvproperty_with_rbv(name='ComputeProfiles', dtype=str, value='N')
        compute_statistics = pvproperty_with_rbv(name='ComputeStatistics', dtype=str, value='Y')

        class StatsPluginCursorGroup(PVGroup):
            x = pvproperty_with_rbv(name='CursorX', dtype=int, value=256)
            y = pvproperty_with_rbv(name='CursorY', dtype=int, value=256)

        cursor = SubGroup(StatsPluginCursorGroup, prefix='')

        hist_entropy = pvproperty(name='HistEntropy_RBV', dtype=float, value=0.0, read_only=True)
        hist_max = pvproperty_with_rbv(name='HistMax', dtype=float, value=255.0)
        hist_min = pvproperty_with_rbv(name='HistMin', dtype=float, value=0.0)
        hist_size = pvproperty_with_rbv(name='HistSize', dtype=int, value=256)
        histogram = pvproperty(name='Histogram_RBV', dtype=float, max_length=256, read_only=True)

        class StatsPluginMaxSizeGroup(PVGroup):
            x = pvproperty(name='MaxSizeX', dtype=int, value=0)
            y = pvproperty(name='MaxSizeY', dtype=int, value=0)

        max_size = SubGroup(StatsPluginMaxSizeGroup, prefix='')

        max_value = pvproperty(name='MaxValue_RBV', dtype=float, value=0.0, read_only=True)

        class StatsPluginMaxXyGroup(PVGroup):
            x = pvproperty(name='MaxX_RBV', dtype=float, value=0.0, read_only=True)
            y = pvproperty(name='MaxY_RBV', dtype=float, value=0.0, read_only=True)

        max_xy = SubGroup(StatsPluginMaxXyGroup, prefix='')

        mean_value = pvproperty(name='MeanValue_RBV', dtype=float, value=0.0, read_only=True)
        min_value = pvproperty(name='MinValue_RBV', dtype=float, value=0.0, read_only=True)

        class StatsPluginMinXyGroup(PVGroup):
            x = pvproperty(name='MinX_RBV', dtype=float, value=0.0, read_only=True)
            y = pvproperty(name='MinY_RBV', dtype=float, value=0.0, read_only=True)

        min_xy = SubGroup(StatsPluginMinXyGroup, prefix='')

        net = pvproperty(name='Net_RBV', dtype=float, value=0.0, read_only=True)

        class StatsPluginProfileAverageGroup(PVGroup):
            x = pvproperty(name='ProfileAverageX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(name='ProfileAverageY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_average = SubGroup(StatsPluginProfileAverageGroup, prefix='')


        class StatsPluginProfileCentroidGroup(PVGroup):
            x = pvproperty(
                name='ProfileCentroidX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(
                name='ProfileCentroidY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_centroid = SubGroup(StatsPluginProfileCentroidGroup, prefix='')


        class StatsPluginProfileCursorGroup(PVGroup):
            x = pvproperty(name='ProfileCursorX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(name='ProfileCursorY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_cursor = SubGroup(StatsPluginProfileCursorGroup, prefix='')


        class StatsPluginProfileSizeGroup(PVGroup):
            x = pvproperty(name='ProfileSizeX_RBV', dtype=int, value=0, read_only=True)
            y = pvproperty(name='ProfileSizeY_RBV', dtype=int, value=0, read_only=True)

        profile_size = SubGroup(StatsPluginProfileSizeGroup, prefix='')


        class StatsPluginProfileThresholdGroup(PVGroup):
            x = pvproperty(
                name='ProfileThresholdX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(
                name='ProfileThresholdY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_threshold = SubGroup(StatsPluginProfileThresholdGroup, prefix='')

        set_xhopr = pvproperty(name='SetXHOPR', dtype=float, value=0.0)
        set_yhopr = pvproperty(name='SetYHOPR', dtype=float, value=0.0)
        sigma_xy = pvproperty(name='SigmaXY_RBV', dtype=float, value=0.0, read_only=True)
        sigma_x = pvproperty(name='SigmaX_RBV', dtype=float, value=0.0, read_only=True)
        sigma_y = pvproperty(name='SigmaY_RBV', dtype=float, value=0.0, read_only=True)
        sigma = pvproperty(name='Sigma_RBV', dtype=float, value=0.0, read_only=True)
        ts_acquiring = pvproperty(name='TSAcquiring', dtype=int, value=0)

        class StatsPluginTsCentroidGroup(PVGroup):
            x = pvproperty(name='TSCentroidX', dtype=float, max_length=2048)
            y = pvproperty(name='TSCentroidY', dtype=float, max_length=2048)

        ts_centroid = SubGroup(StatsPluginTsCentroidGroup, prefix='')

        ts_control = pvproperty(name='TSControl', dtype=str, value='E')
        ts_current_point = pvproperty(name='TSCurrentPoint', dtype=int, value=0)
        ts_max_value = pvproperty(name='TSMaxValue', dtype=float, max_length=2048)

        class StatsPluginTsMaxGroup(PVGroup):
            x = pvproperty(name='TSMaxX', dtype=float, max_length=2048)
            y = pvproperty(name='TSMaxY', dtype=float, max_length=2048)

        ts_max = SubGroup(StatsPluginTsMaxGroup, prefix='')

        ts_mean_value = pvproperty(name='TSMeanValue', dtype=float, max_length=2048)
        ts_min_value = pvproperty(name='TSMinValue', dtype=float, max_length=2048)

        class StatsPluginTsMinGroup(PVGroup):
            x = pvproperty(name='TSMinX', dtype=float, max_length=2048)
            y = pvproperty(name='TSMinY', dtype=float, max_length=2048)

        ts_min = SubGroup(StatsPluginTsMinGroup, prefix='')

        ts_net = pvproperty(name='TSNet', dtype=float, max_length=2048)
        ts_num_points = pvproperty(name='TSNumPoints', dtype=int, value=2048)
        ts_read = pvproperty(name='TSRead', dtype=int, value=3)
        ts_sigma = pvproperty(name='TSSigma', dtype=float, max_length=2048)
        ts_sigma_x = pvproperty(name='TSSigmaX', dtype=float, max_length=2048)
        ts_sigma_xy = pvproperty(name='TSSigmaXY', dtype=float, max_length=2048)
        ts_sigma_y = pvproperty(name='TSSigmaY', dtype=float, max_length=2048)
        ts_total = pvproperty(name='TSTotal', dtype=float, max_length=2048)
        total = pvproperty(name='Total_RBV', dtype=float, value=0.0, read_only=True)

    stats = SubGroup(StatsPluginGroup, prefix='{prefix}:Stats2:')


    class ROIPluginGroup(PVGroup):
        # configuration_names = pvproperty(name=None, dtype=str, value='')
        array_counter = pvproperty_with_rbv(name='ArrayCounter', dtype=int, value=58493174)
        array_rate = pvproperty(name='ArrayRate_RBV', dtype=float, value=118.0, read_only=True)
        asyn_io = pvproperty(name='AsynIO', dtype=int, value=0)
        nd_attributes_file = pvproperty(name='NDAttributesFile', dtype=str, max_length=256)
        pool_alloc_buffers = pvproperty(name='PoolAllocBuffers', dtype=int, value=4, read_only=True)
        pool_free_buffers = pvproperty(name='PoolFreeBuffers', dtype=int, value=2, read_only=True)
        pool_max_buffers = pvproperty(name='PoolMaxBuffers', dtype=int, value=0, read_only=True)
        pool_max_mem = pvproperty(name='PoolMaxMem', dtype=float, value=0.0, read_only=True)
        pool_used_buffers = pvproperty(
            name='PoolUsedBuffers', dtype=float, value=2.0, read_only=True)
        pool_used_mem = pvproperty(
            name='PoolUsedMem', dtype=float, value=0.30517578125, read_only=True)
        port_name = pvproperty(name='PortName_RBV', dtype=str, value='R', read_only=True)
        # asyn_pipeline_config = pvproperty(name=None, dtype=str, value='')

        class ROIPluginArraySizeGroup(PVGroup):
            x = pvproperty(name='ArraySizeX_RBV', dtype=int, value=200, read_only=True)
            y = pvproperty(name='ArraySizeY_RBV', dtype=int, value=200, read_only=True)
            z = pvproperty(name='ArraySizeZ_RBV', dtype=int, value=0, read_only=True)

        array_size = SubGroup(ROIPluginArraySizeGroup, prefix='')

        bayer_pattern = pvproperty(name='BayerPattern_RBV', dtype=int, value=0, read_only=True)
        blocking_callbacks = pvproperty_with_rbv(name='BlockingCallbacks', dtype=str, value='N')
        color_mode = pvproperty(name='ColorMode_RBV', dtype=int, value=0, read_only=True)
        data_type = pvproperty(name='DataType_RBV', dtype=str, value='U', read_only=True)

        class ROIPluginDimSaGroup(PVGroup):
            dim0 = pvproperty(name='Dim0SA', dtype=int, max_length=10)
            dim1 = pvproperty(name='Dim1SA', dtype=int, max_length=10)
            dim2 = pvproperty(name='Dim2SA', dtype=int, max_length=10)

        dim_sa = SubGroup(ROIPluginDimSaGroup, prefix='')

        dimensions = pvproperty(name='Dimensions_RBV', dtype=int, max_length=10, read_only=True)
        dropped_arrays = pvproperty_with_rbv(name='DroppedArrays', dtype=int, value=0)
        enable = pvproperty_with_rbv(name='EnableCallbacks', dtype=str, value='E')
        min_callback_time = pvproperty_with_rbv(name='MinCallbackTime', dtype=float, value=0.0)
        nd_array_address = pvproperty_with_rbv(name='NDArrayAddress', dtype=int, value=0)
        nd_array_port = pvproperty_with_rbv(name='NDArrayPort', dtype=str, value='C')
        ndimensions = pvproperty(name='NDimensions_RBV', dtype=int, value=2, read_only=True)
        plugin_type = pvproperty(name='PluginType_RBV', dtype=str, value='N', read_only=True)
        queue_free = pvproperty(name='QueueFree', dtype=int, value=5)
        queue_free_low = pvproperty(name='QueueFreeLow', dtype=float, value=1.25)
        queue_size = pvproperty(name='QueueSize', dtype=int, value=5)
        queue_use = pvproperty(name='QueueUse', dtype=float, value=0.0)
        queue_use_high = pvproperty(name='QueueUseHIGH', dtype=float, value=3.75)
        queue_use_hihi = pvproperty(name='QueueUseHIHI', dtype=float, value=5.0)
        time_stamp = pvproperty(
            name='TimeStamp_RBV', dtype=float, value=1540232423.3518462, read_only=True)
        unique_id = pvproperty(name='UniqueId_RBV', dtype=int, value=49056, read_only=True)

        class ROIPluginAutoSizeGroup(PVGroup):
            x = pvproperty_with_rbv(name='AutoSizeX', dtype=int, value=0)
            y = pvproperty_with_rbv(name='AutoSizeY', dtype=int, value=0)
            z = pvproperty_with_rbv(name='AutoSizeZ', dtype=int, value=0)

        auto_size = SubGroup(ROIPluginAutoSizeGroup, prefix='')


        class ROIPluginBinGroup(PVGroup):
            x = pvproperty_with_rbv(name='BinX', dtype=int, value=1)
            y = pvproperty_with_rbv(name='BinY', dtype=int, value=1)
            z = pvproperty_with_rbv(name='BinZ', dtype=int, value=1)

        bin_ = SubGroup(ROIPluginBinGroup, prefix='')

        data_type_out = pvproperty_with_rbv(name='DataTypeOut', dtype=str, value='A')
        enable_scale = pvproperty_with_rbv(name='EnableScale', dtype=str, value='D')

        class ROIPluginRoiEnableGroup(PVGroup):
            x = pvproperty_with_rbv(name='EnableX', dtype=str, value='E')
            y = pvproperty_with_rbv(name='EnableY', dtype=str, value='E')
            z = pvproperty_with_rbv(name='EnableZ', dtype=str, value='E')

        roi_enable = SubGroup(ROIPluginRoiEnableGroup, prefix='')


        class ROIPluginMaxXyGroup(PVGroup):
            x = pvproperty(name='MaxX', dtype=int, value=1024)
            y = pvproperty(name='MaxY', dtype=int, value=1024)

        max_xy = SubGroup(ROIPluginMaxXyGroup, prefix='')


        class ROIPluginMaxSizeGroup(PVGroup):
            x = pvproperty(name='MaxSizeX_RBV', dtype=int, value=1024, read_only=True)
            y = pvproperty(name='MaxSizeY_RBV', dtype=int, value=1024, read_only=True)
            z = pvproperty(name='MaxSizeZ_RBV', dtype=int, value=0, read_only=True)

        max_size = SubGroup(ROIPluginMaxSizeGroup, prefix='')


        class ROIPluginMinXyzGroup(PVGroup):
            min_x = pvproperty_with_rbv(name='MinX', dtype=int, value=348)
            min_y = pvproperty_with_rbv(name='MinY', dtype=int, value=540)
            min_z = pvproperty_with_rbv(name='MinZ', dtype=int, value=0)

        min_xyz = SubGroup(ROIPluginMinXyzGroup, prefix='')

        name_ = pvproperty_with_rbv(name='Name', dtype=str, value='')

        class ROIPluginReverseGroup(PVGroup):
            x = pvproperty_with_rbv(name='ReverseX', dtype=int, value=0)
            y = pvproperty_with_rbv(name='ReverseY', dtype=int, value=0)
            z = pvproperty_with_rbv(name='ReverseZ', dtype=int, value=0)

        reverse = SubGroup(ROIPluginReverseGroup, prefix='')

        scale = pvproperty_with_rbv(name='Scale', dtype=float, value=1.0)
        set_xhopr = pvproperty(name='SetXHOPR', dtype=float, value=1024.0)
        set_yhopr = pvproperty(name='SetYHOPR', dtype=float, value=1024.0)

        class ROIPluginSizeGroup(PVGroup):
            x = pvproperty_with_rbv(name='SizeX', dtype=int, value=200)
            y = pvproperty_with_rbv(name='SizeY', dtype=int, value=200)
            z = pvproperty_with_rbv(name='SizeZ', dtype=int, value=1000000)

        size = SubGroup(ROIPluginSizeGroup, prefix='')


    ROI = SubGroup(ROIPluginGroup, prefix='{prefix}:{ROI_port}:')


    class StatsPluginGroup(PVGroup):
        # configuration_names = pvproperty(name=None, dtype=str, value='')
        array_counter = pvproperty_with_rbv(name='ArrayCounter', dtype=int, value=58493709)
        array_rate = pvproperty(name='ArrayRate_RBV', dtype=float, value=117.0, read_only=True)
        asyn_io = pvproperty(name='AsynIO', dtype=int, value=0)
        nd_attributes_file = pvproperty(name='NDAttributesFile', dtype=str, max_length=256)
        pool_alloc_buffers = pvproperty(name='PoolAllocBuffers', dtype=int, value=2, read_only=True)
        pool_free_buffers = pvproperty(name='PoolFreeBuffers', dtype=int, value=1, read_only=True)
        pool_max_buffers = pvproperty(name='PoolMaxBuffers', dtype=int, value=0, read_only=True)
        pool_max_mem = pvproperty(name='PoolMaxMem', dtype=float, value=0.0, read_only=True)
        pool_used_buffers = pvproperty(
            name='PoolUsedBuffers', dtype=float, value=1.0, read_only=True)
        pool_used_mem = pvproperty(
            name='PoolUsedMem', dtype=float, value=0.152587890625, read_only=True)
        port_name = pvproperty(name='PortName_RBV', dtype=str, value='S', read_only=True)
        # asyn_pipeline_config = pvproperty(name=None, dtype=str, value='')

        class StatsPluginArraySizeGroup(PVGroup):
            height = pvproperty(name='ArraySize1_RBV', dtype=int, value=200, read_only=True)
            width = pvproperty(name='ArraySize0_RBV', dtype=int, value=200, read_only=True)
            depth = pvproperty(name='ArraySize2_RBV', dtype=int, value=0, read_only=True)

        array_size = SubGroup(StatsPluginArraySizeGroup, prefix='')

        bayer_pattern = pvproperty(name='BayerPattern_RBV', dtype=int, value=0, read_only=True)
        blocking_callbacks = pvproperty_with_rbv(name='BlockingCallbacks', dtype=str, value='N')
        color_mode = pvproperty(name='ColorMode_RBV', dtype=int, value=0, read_only=True)
        data_type = pvproperty(name='DataType_RBV', dtype=str, value='U', read_only=True)

        class StatsPluginDimSaGroup(PVGroup):
            dim0 = pvproperty(name='Dim0SA', dtype=int, max_length=10)
            dim1 = pvproperty(name='Dim1SA', dtype=int, max_length=10)
            dim2 = pvproperty(name='Dim2SA', dtype=int, max_length=10)

        dim_sa = SubGroup(StatsPluginDimSaGroup, prefix='')

        dimensions = pvproperty(name='Dimensions_RBV', dtype=int, max_length=10, read_only=True)
        dropped_arrays = pvproperty_with_rbv(name='DroppedArrays', dtype=int, value=0)
        enable = pvproperty_with_rbv(name='EnableCallbacks', dtype=str, value='E')
        min_callback_time = pvproperty_with_rbv(name='MinCallbackTime', dtype=float, value=0.0)
        nd_array_address = pvproperty_with_rbv(name='NDArrayAddress', dtype=int, value=0)
        nd_array_port = pvproperty_with_rbv(name='NDArrayPort', dtype=str, value='R')
        ndimensions = pvproperty(name='NDimensions_RBV', dtype=int, value=2, read_only=True)
        plugin_type = pvproperty(name='PluginType_RBV', dtype=str, value='N', read_only=True)
        queue_free = pvproperty(name='QueueFree', dtype=int, value=5)
        queue_free_low = pvproperty(name='QueueFreeLow', dtype=float, value=1.25)
        queue_size = pvproperty(name='QueueSize', dtype=int, value=5)
        queue_use = pvproperty(name='QueueUse', dtype=float, value=0.0)
        queue_use_high = pvproperty(name='QueueUseHIGH', dtype=float, value=3.75)
        queue_use_hihi = pvproperty(name='QueueUseHIHI', dtype=float, value=5.0)
        time_stamp = pvproperty(
            name='TimeStamp_RBV', dtype=float, value=1540232427.767215, read_only=True)
        unique_id = pvproperty(name='UniqueId_RBV', dtype=int, value=50646, read_only=True)
        bgd_width = pvproperty_with_rbv(name='BgdWidth', dtype=int, value=1)
        centroid_threshold = pvproperty_with_rbv(name='CentroidThreshold', dtype=float, value=1.0)

        class StatsPluginCentroidGroup(PVGroup):
            x = pvproperty(name='CentroidX_RBV', dtype=float, value=0.0, read_only=True)
            y = pvproperty(name='CentroidY_RBV', dtype=float, value=0.0, read_only=True)

        centroid = SubGroup(StatsPluginCentroidGroup, prefix='')

        compute_centroid = pvproperty_with_rbv(name='ComputeCentroid', dtype=str, value='N')
        compute_histogram = pvproperty_with_rbv(name='ComputeHistogram', dtype=str, value='N')
        compute_profiles = pvproperty_with_rbv(name='ComputeProfiles', dtype=str, value='N')
        compute_statistics = pvproperty_with_rbv(name='ComputeStatistics', dtype=str, value='Y')

        class StatsPluginCursorGroup(PVGroup):
            x = pvproperty_with_rbv(name='CursorX', dtype=int, value=256)
            y = pvproperty_with_rbv(name='CursorY', dtype=int, value=256)

        cursor = SubGroup(StatsPluginCursorGroup, prefix='')

        hist_entropy = pvproperty(name='HistEntropy_RBV', dtype=float, value=0.0, read_only=True)
        hist_max = pvproperty_with_rbv(name='HistMax', dtype=float, value=255.0)
        hist_min = pvproperty_with_rbv(name='HistMin', dtype=float, value=0.0)
        hist_size = pvproperty_with_rbv(name='HistSize', dtype=int, value=256)
        histogram = pvproperty(name='Histogram_RBV', dtype=float, max_length=256, read_only=True)

        class StatsPluginMaxSizeGroup(PVGroup):
            x = pvproperty(name='MaxSizeX', dtype=int, value=0)
            y = pvproperty(name='MaxSizeY', dtype=int, value=0)

        max_size = SubGroup(StatsPluginMaxSizeGroup, prefix='')

        max_value = pvproperty(name='MaxValue_RBV', dtype=float, value=260.0, read_only=True)

        class StatsPluginMaxXyGroup(PVGroup):
            x = pvproperty(name='MaxX_RBV', dtype=float, value=193.0, read_only=True)
            y = pvproperty(name='MaxY_RBV', dtype=float, value=111.0, read_only=True)

        max_xy = SubGroup(StatsPluginMaxXyGroup, prefix='')

        mean_value = pvproperty(name='MeanValue_RBV', dtype=float, value=154.53605, read_only=True)
        min_value = pvproperty(name='MinValue_RBV', dtype=float, value=55.0, read_only=True)

        class StatsPluginMinXyGroup(PVGroup):
            x = pvproperty(name='MinX_RBV', dtype=float, value=167.0, read_only=True)
            y = pvproperty(name='MinY_RBV', dtype=float, value=160.0, read_only=True)

        min_xy = SubGroup(StatsPluginMinXyGroup, prefix='')

        net = pvproperty(name='Net_RBV', dtype=float, value=-83816.0, read_only=True)

        class StatsPluginProfileAverageGroup(PVGroup):
            x = pvproperty(name='ProfileAverageX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(name='ProfileAverageY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_average = SubGroup(StatsPluginProfileAverageGroup, prefix='')


        class StatsPluginProfileCentroidGroup(PVGroup):
            x = pvproperty(
                name='ProfileCentroidX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(
                name='ProfileCentroidY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_centroid = SubGroup(StatsPluginProfileCentroidGroup, prefix='')


        class StatsPluginProfileCursorGroup(PVGroup):
            x = pvproperty(name='ProfileCursorX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(name='ProfileCursorY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_cursor = SubGroup(StatsPluginProfileCursorGroup, prefix='')


        class StatsPluginProfileSizeGroup(PVGroup):
            x = pvproperty(name='ProfileSizeX_RBV', dtype=int, value=0, read_only=True)
            y = pvproperty(name='ProfileSizeY_RBV', dtype=int, value=0, read_only=True)

        profile_size = SubGroup(StatsPluginProfileSizeGroup, prefix='')


        class StatsPluginProfileThresholdGroup(PVGroup):
            x = pvproperty(
                name='ProfileThresholdX_RBV', dtype=float, max_length=1024, read_only=True)
            y = pvproperty(
                name='ProfileThresholdY_RBV', dtype=float, max_length=1024, read_only=True)

        profile_threshold = SubGroup(StatsPluginProfileThresholdGroup, prefix='')

        set_xhopr = pvproperty(name='SetXHOPR', dtype=float, value=0.0)
        set_yhopr = pvproperty(name='SetYHOPR', dtype=float, value=0.0)
        sigma_xy = pvproperty(name='SigmaXY_RBV', dtype=float, value=0.0, read_only=True)
        sigma_x = pvproperty(name='SigmaX_RBV', dtype=float, value=0.0, read_only=True)
        sigma_y = pvproperty(name='SigmaY_RBV', dtype=float, value=0.0, read_only=True)
        sigma = pvproperty(name='Sigma_RBV', dtype=float, value=12.556249451070101, read_only=True)
        ts_acquiring = pvproperty(name='TSAcquiring', dtype=int, value=0)

        class StatsPluginTsCentroidGroup(PVGroup):
            x = pvproperty(name='TSCentroidX', dtype=float, max_length=2048)
            y = pvproperty(name='TSCentroidY', dtype=float, max_length=2048)

        ts_centroid = SubGroup(StatsPluginTsCentroidGroup, prefix='')

        ts_control = pvproperty(name='TSControl', dtype=str, value='E')
        ts_current_point = pvproperty(name='TSCurrentPoint', dtype=int, value=0)
        ts_max_value = pvproperty(name='TSMaxValue', dtype=float, max_length=2048)

        class StatsPluginTsMaxGroup(PVGroup):
            x = pvproperty(name='TSMaxX', dtype=float, max_length=2048)
            y = pvproperty(name='TSMaxY', dtype=float, max_length=2048)

        ts_max = SubGroup(StatsPluginTsMaxGroup, prefix='')

        ts_mean_value = pvproperty(name='TSMeanValue', dtype=float, max_length=2048)
        ts_min_value = pvproperty(name='TSMinValue', dtype=float, max_length=2048)

        class StatsPluginTsMinGroup(PVGroup):
            x = pvproperty(name='TSMinX', dtype=float, max_length=2048)
            y = pvproperty(name='TSMinY', dtype=float, max_length=2048)

        ts_min = SubGroup(StatsPluginTsMinGroup, prefix='')

        ts_net = pvproperty(name='TSNet', dtype=float, max_length=2048)
        ts_num_points = pvproperty(name='TSNumPoints', dtype=int, value=2048)
        ts_read = pvproperty(name='TSRead', dtype=int, value=3)
        ts_sigma = pvproperty(name='TSSigma', dtype=float, max_length=2048)
        ts_sigma_x = pvproperty(name='TSSigmaX', dtype=float, max_length=2048)
        ts_sigma_xy = pvproperty(name='TSSigmaXY', dtype=float, max_length=2048)
        ts_sigma_y = pvproperty(name='TSSigmaY', dtype=float, max_length=2048)
        ts_total = pvproperty(name='TSTotal', dtype=float, max_length=2048)
        total = pvproperty(name='Total_RBV', dtype=float, value=6176330.0, read_only=True)

    ROI_stats = SubGroup(StatsPluginGroup, prefix='{prefix}:{ROI_stats_port}:')


    class ImagePluginGroup(PVGroup):
        # configuration_names = pvproperty(name=None, dtype=str, value='')
        array_counter = pvproperty_with_rbv(name='ArrayCounter', dtype=int, value=981497)
        array_rate = pvproperty(name='ArrayRate_RBV', dtype=float, value=2.0, read_only=True)
        asyn_io = pvproperty(name='AsynIO', dtype=int, value=0)
        nd_attributes_file = pvproperty(name='NDAttributesFile', dtype=str, max_length=256)
        pool_alloc_buffers = pvproperty(name='PoolAllocBuffers', dtype=int, value=1, read_only=True)
        pool_free_buffers = pvproperty(name='PoolFreeBuffers', dtype=int, value=1, read_only=True)
        pool_max_buffers = pvproperty(name='PoolMaxBuffers', dtype=int, value=-1, read_only=True)
        pool_max_mem = pvproperty(name='PoolMaxMem', dtype=float, value=0.0, read_only=True)
        pool_used_buffers = pvproperty(
            name='PoolUsedBuffers', dtype=float, value=0.0, read_only=True)
        pool_used_mem = pvproperty(
            name='PoolUsedMem', dtype=float, value=0.0762939453125, read_only=True)
        port_name = pvproperty(name='PortName_RBV', dtype=str, value='I', read_only=True)
        # asyn_pipeline_config = pvproperty(name=None, dtype=str, value='')

        class ImagePluginArraySizeGroup(PVGroup):
            height = pvproperty(name='ArraySize1_RBV', dtype=int, value=200, read_only=True)
            width = pvproperty(name='ArraySize0_RBV', dtype=int, value=200, read_only=True)
            depth = pvproperty(name='ArraySize2_RBV', dtype=int, value=0, read_only=True)

        array_size = SubGroup(ImagePluginArraySizeGroup, prefix='')

        bayer_pattern = pvproperty(name='BayerPattern_RBV', dtype=int, value=0, read_only=True)
        blocking_callbacks = pvproperty_with_rbv(name='BlockingCallbacks', dtype=str, value='N')
        color_mode = pvproperty(name='ColorMode_RBV', dtype=int, value=0, read_only=True)
        data_type = pvproperty(name='DataType_RBV', dtype=str, value='U', read_only=True)

        class ImagePluginDimSaGroup(PVGroup):
            dim0 = pvproperty(name='Dim0SA', dtype=int, max_length=10)
            dim1 = pvproperty(name='Dim1SA', dtype=int, max_length=10)
            dim2 = pvproperty(name='Dim2SA', dtype=int, max_length=10)

        dim_sa = SubGroup(ImagePluginDimSaGroup, prefix='')

        dimensions = pvproperty(name='Dimensions_RBV', dtype=int, max_length=10, read_only=True)
        dropped_arrays = pvproperty_with_rbv(name='DroppedArrays', dtype=int, value=0)
        enable = pvproperty_with_rbv(name='EnableCallbacks', dtype=str, value='E')
        min_callback_time = pvproperty_with_rbv(name='MinCallbackTime', dtype=float, value=0.5)
        nd_array_address = pvproperty_with_rbv(name='NDArrayAddress', dtype=int, value=0)
        nd_array_port = pvproperty_with_rbv(name='NDArrayPort', dtype=str, value='R')
        ndimensions = pvproperty(name='NDimensions_RBV', dtype=int, value=2, read_only=True)
        plugin_type = pvproperty(name='PluginType_RBV', dtype=str, value='N', read_only=True)
        queue_free = pvproperty(name='QueueFree', dtype=int, value=10)
        queue_free_low = pvproperty(name='QueueFreeLow', dtype=float, value=2.5)
        queue_size = pvproperty(name='QueueSize', dtype=int, value=10)
        queue_use = pvproperty(name='QueueUse', dtype=float, value=0.0)
        queue_use_high = pvproperty(name='QueueUseHIGH', dtype=float, value=7.5)
        queue_use_hihi = pvproperty(name='QueueUseHIHI', dtype=float, value=10.0)
        time_stamp = pvproperty(
            name='TimeStamp_RBV', dtype=float, value=1540232433.7328763, read_only=True)
        unique_id = pvproperty(name='UniqueId_RBV', dtype=int, value=52956, read_only=True)
        array_data = pvproperty(name='ArrayData', dtype=int, max_length=1048576)

    ROI_image = SubGroup(ImagePluginGroup, prefix='{prefix}:{ROI_image_port}:')



# -- ParametersGroup --

class ParametersGroup(PVGroup):
    cam_x = pvproperty(name=':CAM_X', dtype=float, value=0.0, doc='Onaxis camera origin x position')
    cam_y = pvproperty(name=':CAM_Y', dtype=float, value=0.0, doc='Onaxis camera origin y position')
    pxsize = pvproperty(name=':PXSIZE', dtype=float, value=0.0, doc='Onaxis camera pixel size')
    cam_roll = pvproperty(
        name=':CAM_ROLL', dtype=float, value=0.0, doc='Rotation of on axis camera around z axi')
    beam_x = pvproperty(name=':BEAM_X', dtype=float, value=0.0, doc='X position of the x-ray beam')
    beam_y = pvproperty(name=':BEAM_Y', dtype=float, value=0.0, doc='Y position of the x-ray beam')
    beam_x_px = pvproperty(name=':BEAM_X_PX', dtype=float, value=0.0)
    beam_y_px = pvproperty(name=':BEAM_Y_PX', dtype=float, value=0.0)
    nozzle_x = pvproperty(
        name=':NOZZLE_X', dtype=float, value=0.0, doc='X position of jet coming out of nozzle')
    nozzle_y = pvproperty(
        name=':NOZZLE_Y', dtype=float, value=0.0, doc='Y position of jet coming out of nozzle')
    nozzle_xwidth = pvproperty(name=':NOZZLE_XWIDTH', dtype=float, value=0.0, doc='Width of nozzle')
    jet_x = pvproperty(
        name=':JET_X', dtype=float, value=0.0, doc='X position of jet at beam height')
    jet_roll = pvproperty(
        name=':JET_ROLL', dtype=float, value=0.0, doc='Rotation of jet about z-axis')
    state = pvproperty(name=':STATE', dtype=int, value=0)
    jet_counter = pvproperty(name=':JET_Counter', dtype=float, value=0.0, doc='Jet event counter')
    jet_reprate = pvproperty(name=':JET_RepRate', dtype=float, value=0.0, doc='Jet event counter')
    nozzle_counter = pvproperty(
        name=':NOZZLE_Counter', dtype=float, value=0.0, doc='Inline camera nozzle event counter')
    nozzle_reprate = pvproperty(
        name=':NOZZLE_RepRate', dtype=float, value=0.0, doc='Inline camera nozzle event counter')


class JetTracking(PVGroup):
    pi1_injector = SubGroup(
        InjectorGroup,
        prefix='',
        macros={
            'coarseX': 'CXI:PI1:MMS:01',
            'coarseY': 'CXI:PI1:MMS:02',
            'coarseZ': 'CXI:PI1:MMS:03',
            'fineX': 'CXI:USR:MMS:01',
            'fineY': 'CXI:USR:MMS:02',
            'fineZ': 'CXI:USR:MMS:03'}
        )
    sc1_questar = SubGroup(
        QuestarGroup,
        prefix='',
        macros={'ROI_port': 'ROI1',
                'ROI_stats_port': 'Stats1',
                'ROI_image_port': 'IMAGE1',
                'prefix': 'CXI:SC1:INLINE'}
        )
    sc1_params = SubGroup(
        ParametersGroup,
        prefix='CXI:SC1:INLINE',
        macros={}
        )


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='TEST:',
        desc="CXI jet tracking mocked IOC")
    ioc = JetTracking(**ioc_options)
    run(ioc.pvdb, **run_options)
