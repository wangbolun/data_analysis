import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.planning.trajectory_pb2 as trajectory_pb2
from modules.common.tools.lcm_utilities import unpack_packets

PlannerTrajectory = namedtuple(
    typename = "PlannerTrajectory",
    field_names = (
        "timestamp",
        "ego_x",
        "ego_y",
        "ego_heading",
        "point",
        "speed_p0",
        "comfort_acc_acceleration",
        "safety_acc_acceleration",
        "gear", 
        "estop_intensity",
    ),
    defaults=(0,0,0,0,0,0)
)

def get_planner_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    gear_target = np.zeros(n_packets)
    ego_x = np.zeros(n_packets)
    ego_y = np.zeros(n_packets)
    ego_heading = np.zeros(n_packets)
    point = [np.array([])]*n_packets
    comfort_acc_acceleration = np.zeros(n_packets)
    safety_acc_acceleration = np.zeros(n_packets)
    speed_p0 = np.zeros(n_packets)
    estop_intensity = np.zeros(n_packets)

    trajectory = trajectory_pb2.Trajectory()
    for i,packet in enumerate(packets):
        trajectory.ParseFromString( packet )
        ego_x[i] = trajectory.vehicle_pose.x
        ego_y[i] = trajectory.vehicle_pose.y
        ego_heading[i] = trajectory.vehicle_pose.heading_angle
        point[i] = trajectory.point
        gear_target[i] = trajectory.gear_location 
        speed_p0[i] = trajectory.point[0].speed
        comfort_acc_acceleration[i] = trajectory.point[0].acceleration
        safety_acc_acceleration[i] = trajectory.point[1].acceleration
        estop_intensity[i] = trajectory.estop_intensity

    return PlannerTrajectory(
        timestamp = timestamp,
        ego_x = ego_x,
        ego_y = ego_y,
        ego_heading = ego_heading,
        point = point,
        gear = gear_target,
        comfort_acc_acceleration = comfort_acc_acceleration,
        safety_acc_acceleration = safety_acc_acceleration,
        speed_p0 = speed_p0,
        estop_intensity = estop_intensity,
    )