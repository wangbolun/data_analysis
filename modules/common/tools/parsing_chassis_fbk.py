import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.vehicle.chassis_pb2 as chassis_pb2
import modules.common.data_struct.proto.vehicle.gear_pb2 as gear_pb2
from modules.common.tools.lcm_utilities import unpack_packets

ChassisStatus = namedtuple(
    typename = "ChassisStatus",
    field_names = (
        "timestamp",
        "timestamp_abs",
        "log_starting_time",
        "gear",
        "vehicle_speed",
        "maximum_user_speed",
        "vehicle_acceleration_longitudinal", 
        "vehicle_acceleration_lateral", 
        "steering_system_steering_wheel_angle",
        "steering_angle", 
        "yaw_rate", 
        "autodrive_mode", 
        "turn_signal", 
        "steering_torque",
    ),
    defaults=(0,0,0,0,0,0,0,0,0)
)


def get_chassis_fbk_data(lcmlog_dataframe, channel):
    log_starting_time, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    vehicle_gear = np.zeros(n_packets)
    vehicle_speed = np.zeros(n_packets)
    maximum_user_speed = np.zeros(n_packets)
    vehicle_acceleration_longitudinal = np.zeros(n_packets)
    vehicle_acceleration_lateral = np.zeros(n_packets)
    steering_system_steering_wheel_angle = np.zeros(n_packets)
    steering_angle = np.zeros(n_packets)
    yaw_rate = np.zeros(n_packets)
    autodrive_mode = np.zeros(n_packets)
    turn_signal = np.zeros(n_packets)
    steering_torque = np.zeros(n_packets)

    chassis = chassis_pb2.Chassis()
    for i,packet in enumerate(packets):
        chassis.ParseFromString( packet )

        vehicle_speed[i] = chassis.vehicle_speed.vehicle_speed
        maximum_user_speed[i] = chassis.maximum_user_speed
        if gear_pb2.GearPosition.Name(chassis.gear_location) == 'GEAR_REVERSE':
            vehicle_speed[i] *= -1

        vehicle_acceleration_longitudinal[i] = chassis.acceleration.longitudinal
        vehicle_acceleration_lateral[i] = chassis.acceleration.lateral
        vehicle_gear[i] = chassis.gear_location
        steering_angle[i] = chassis.steering_angle
        yaw_rate[i] = chassis.yaw_rate
        steering_system_steering_wheel_angle[i] = chassis.steering_system.steering_wheel_angle
        autodrive_mode[i] = chassis.driving_mode
        turn_signal[i] = chassis.vehicle_signal.turn_signal
        steering_torque[i] = chassis.steering_system.steering_wheel_torque

    return ChassisStatus(
        log_starting_time = log_starting_time,
        timestamp = timestamp,
        timestamp_abs = timestamp + log_starting_time * 1e-6,
        gear = vehicle_gear,
        vehicle_speed = vehicle_speed,
        maximum_user_speed = maximum_user_speed,
        vehicle_acceleration_longitudinal = vehicle_acceleration_longitudinal,
        vehicle_acceleration_lateral = vehicle_acceleration_lateral,
        steering_system_steering_wheel_angle = steering_system_steering_wheel_angle,
        steering_angle = steering_angle,
        yaw_rate = yaw_rate,
        autodrive_mode = autodrive_mode,
        turn_signal = turn_signal,
        steering_torque = steering_torque,
    )