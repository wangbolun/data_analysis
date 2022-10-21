import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.perception.perception_obstacle_pb2 as perception_obstacle_pb2
from modules.common.tools.lcm_utilities import unpack_packets

FusionObstacles = namedtuple(
    typename = "FusionObstacles",
    field_names = (
        "timestamp",
        "obstacle_positions",
        "obstacle_velocitys",
    ),
    defaults=(0,0)
)

def get_fusion_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)

    obstacle_positions = []
    obstacle_velocitys = []
    
    obstacles = perception_obstacle_pb2.PerceptionObstacles()
    for i,packet in enumerate(packets):
        obstacles.ParseFromString( packet )
        obstacle_positions.append(
            [(obstacle.position.x, obstacle.position.y) for obstacle in obstacles.perception_obstacle]
        )
        obstacle_velocitys.append(
            [(obstacle.velocity.x, obstacle.velocity.y) for obstacle in obstacles.perception_obstacle]
        )
        
    return FusionObstacles(
        timestamp = timestamp,
        obstacle_positions = obstacle_positions,
        obstacle_velocitys = obstacle_velocitys,
    )