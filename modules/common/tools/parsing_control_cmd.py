import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.control.control_cmd_pb2 as control_cmd_pb2
from modules.common.tools.lcm_utilities import unpack_packets

ControlCmd = namedtuple(
    typename = "ControlCmd",
    field_names = (
        "timestamp",
        "acceleration",
        "steering_angle",
        "brake",
        "gear", 
        "estop_intensity",
    ),
    defaults=(0,0,0,0,0,0)
)


def get_control_cmd_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    acceleration = np.zeros(n_packets)
    steering_angle = np.zeros(n_packets)
    gear = np.zeros(n_packets)
    brake = np.zeros(n_packets)
    estop_intensity = np.zeros(n_packets)

    control_cmd = control_cmd_pb2.ControlCommand()
    for i,packet in enumerate(packets):
        control_cmd.ParseFromString( packet )
        acceleration[i] = control_cmd.acceleration
        gear[i] = control_cmd.gear_location
        steering_angle[i] = control_cmd.steering_angle
        brake[i] = control_cmd.brake
        estop_intensity[i] = control_cmd.estop_intensity

    return ControlCmd(
        timestamp = timestamp,
        acceleration = acceleration,
        brake = brake,
        gear = gear,
        steering_angle = steering_angle,
        estop_intensity = estop_intensity,
    )