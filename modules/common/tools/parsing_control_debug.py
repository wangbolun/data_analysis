import numpy as np
from collections import namedtuple

import modules.common.data_struct.lcm.control.control_debug_t as control_debug_t
from modules.common.tools.lcm_utilities import unpack_packets

ControlDebug = namedtuple(
    typename = "ControlDebug",
    field_names = (
        "timestamp",
        "x",
        "y",
        "heading_angle",
        "longitudinal_speed_target",
        "longitudinal_acceleration_target",
        "longitudinal_position_error",
        "longitudinal_speed_error", 
        "longitudinal_acceleration_error",
        "lateral_position_error",
        "heading_angle_error",
        "curvature",
        "steering_angle_target",
        "steering_angle_status",
        "steering_angle_command",
    ),
    defaults=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
)

def get_control_debug_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    x = np.zeros(n_packets)
    y = np.zeros(n_packets)
    heading_angle = np.zeros(n_packets)
    
    # longitudinal signals
    longitudinal_position_error = np.zeros(n_packets)
    longitudinal_speed_error = np.zeros(n_packets)
    longitudinal_acceleration_error = np.zeros(n_packets)
    longitudinal_speed_target = np.zeros(n_packets)
    longitudinal_acceleration_target = np.zeros(n_packets)
    
    # lateral signals
    steering_angle_target = np.zeros(n_packets)
    steering_angle_status = np.zeros(n_packets)
    steering_angle_command = np.zeros(n_packets)
    
    lateral_position_error = np.zeros(n_packets)
    heading_angle_error = np.zeros(n_packets)
    curvature = np.zeros(n_packets)

    for i,packet in enumerate(packets):
        msg = control_debug_t.decode(packet)
        
        x[i] = msg.x_ego
        y[i] = msg.y_ego 
        heading_angle[i] = msg.heading_angle
        longitudinal_position_error[i] = msg.longitudinal_position - msg.longitudinal_position_target
        longitudinal_speed_target[i] = msg.longitudinal_speed_target
        longitudinal_acceleration_target[i] = msg.longitudinal_acceleration_target
        longitudinal_speed_error[i] = msg.longitudinal_speed - msg.longitudinal_speed_target
        longitudinal_acceleration_error[i] = msg.longitudinal_acceleration - msg.longitudinal_acceleration_target
        longitudinal_speed_target[i] = msg.longitudinal_speed_target
        longitudinal_acceleration_target[i] = msg.longitudinal_acceleration_target
        
        steering_angle_target[i] = msg.steering_angle_target
        steering_angle_status[i] = msg.steering_angle_status
        steering_angle_command[i] = msg.steering_angle_command
        lateral_position_error[i] = msg.lateral_position_error
        heading_angle_error[i] = msg.heading_angle_error
        curvature[i] = msg.curvature
        
    return ControlDebug(
        timestamp = timestamp,
        x = x,
        y = y,
        heading_angle = heading_angle,
        longitudinal_speed_target = longitudinal_speed_target,
        longitudinal_acceleration_target = longitudinal_acceleration_target,
        longitudinal_position_error = longitudinal_position_error,
        longitudinal_speed_error = longitudinal_speed_error,
        longitudinal_acceleration_error = longitudinal_acceleration_error,
        steering_angle_target = steering_angle_target,
        steering_angle_status = steering_angle_status,
        steering_angle_command = steering_angle_command,
        lateral_position_error = lateral_position_error,
        heading_angle_error = heading_angle_error,
        curvature = curvature
    )