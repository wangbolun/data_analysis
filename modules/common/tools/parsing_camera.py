import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.drivers.camera.mobileye_pb2 as mobileye_pb2
from modules.common.tools.lcm_utilities import unpack_packets

CameraInfo = namedtuple(
    typename = "CameraInfo",
    field_names = (
        "timestamp",
        "center_line_a",
        "center_line_b",
        "center_line_c", 
        "center_line_d", 
        "center_line_curvature",
        "center_line_length", 
        "center_line_type", 
        "left_line_a",
        "left_line_b",
        "left_line_c", 
        "left_line_d", 
        "left_line_length", 
        "left_line_type", 
        "right_line_a",
        "right_line_b",
        "right_line_c", 
        "right_line_d", 
        "right_line_length", 
        "right_line_type", 
        "lane_width",
    ),
    defaults=(0,0)
)

def get_camera_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    center_line_a = np.zeros(n_packets)
    center_line_b = np.zeros(n_packets)
    center_line_c = np.zeros(n_packets) 
    center_line_d = np.zeros(n_packets) 
    center_line_curvature = np.zeros(n_packets) 
    center_line_length = np.zeros(n_packets) 
    center_line_type = np.zeros(n_packets) 
    left_line_a = np.zeros(n_packets)
    left_line_b = np.zeros(n_packets)
    left_line_c = np.zeros(n_packets) 
    left_line_d = np.zeros(n_packets) 
    left_line_length = np.zeros(n_packets) 
    left_line_type = np.zeros(n_packets) 
    right_line_a = np.zeros(n_packets)
    right_line_b = np.zeros(n_packets)
    right_line_c = np.zeros(n_packets) 
    right_line_d = np.zeros(n_packets) 
    right_line_length = np.zeros(n_packets) 
    right_line_type = np.zeros(n_packets) 
    lane_width = np.zeros(n_packets)
    
    camera_info = mobileye_pb2.MobileyeInfo()
    for i,packet in enumerate(packets):
        camera_info.ParseFromString( packet )
        center_line_a[i] = camera_info.center_line.a
        center_line_b[i] = camera_info.center_line.b
        center_line_c[i] = camera_info.center_line.c
        center_line_d[i] = camera_info.center_line.d
        center_line_curvature[i] = -camera_info.center_line.c/( (1 + camera_info.center_line.b**2)**1.5 / 2 )
        center_line_length[i] = camera_info.center_line.length
        center_line_type[i] = camera_info.center_line.type
        lane_width[i] = camera_info.lane_width
        
        if len(camera_info.line) >= 1:
            left_line_a[i] = camera_info.line[1].a
            left_line_b[i] = camera_info.line[1].b
            left_line_c[i] = camera_info.line[1].c
            left_line_d[i] = camera_info.line[1].d
            left_line_length[i] = camera_info.line[1].length
            left_line_type[i] = camera_info.line[1].type
        if len(camera_info.line) >= 2:
            right_line_a[i] = camera_info.line[2].a
            right_line_b[i] = camera_info.line[2].b
            right_line_c[i] = camera_info.line[2].c
            right_line_d[i] = camera_info.line[2].d
            right_line_length[i] = camera_info.line[2].length
            right_line_type[i] = camera_info.line[2].type

    return CameraInfo(
        timestamp = timestamp,
        center_line_a = center_line_a,
        center_line_b = center_line_b,
        center_line_c = center_line_c,
        center_line_d = center_line_d,
        center_line_curvature = center_line_curvature,
        center_line_length = center_line_length,
        center_line_type = center_line_type,
        left_line_a = left_line_a,
        left_line_b = left_line_b,
        left_line_c = left_line_c,
        left_line_d = left_line_d,
        left_line_length = left_line_length,
        left_line_type = left_line_type,
        right_line_a = right_line_a,
        right_line_b = right_line_b,
        right_line_c = right_line_c,
        right_line_d = right_line_d,
        right_line_length = right_line_length,
        right_line_type = right_line_type,
        lane_width=lane_width,
    )