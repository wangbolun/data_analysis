from modules.common.tools.lcm_utilities import get_lcm_dataset_test_ph
from modules.common.tools.lcm_utilities import unpack_packets  # 解包工具
import modules.common.data_struct.proto.vehicle.chassis_pb2 as chassis_pb2
import modules.common.data_struct.proto.drivers.camera.mobileye_pb2 as mobileye_pb2
import modules.common.data_struct.proto.localization.gps_imu_info_pb2 as gps_imu_info_pb2
from pyproj import Transformer
import math


class ReadLcmAll:
    def __init__(self, lcm_name):
        self.dot_x = 522149
        self.dot_y = 4320960
        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:32650")
        self.dataframe = get_lcm_dataset_test_ph(lcm_name)
        self.chassis_dict = {
            'chassis_channel_starting_time': [],
            'chassis_timestamp': [],
            'chassis_vehicle_speed': [],
            'chassis_maximum_user_speed': [],
        }

        self.gps_imu_dict = {'gps_imu_channel_starting_time': [],
                             'gps_imu_timestamp': [],
                             'gps_longitude': [],
                             'gps_latitude': [],
                             'gps_yaw': [],
                             'UTM_X': [],
                             'UTM_Y': [],
                             'heding': []}

        self.camera_info_dict = {"timestamp": [],
                                 "center_length": [],
                                 "line1_a": [],
                                 "line1_b": [],
                                 'line1_c': [],
                                 'line1_d': [],
                                 'line1_length': [],
                                 "line2_a": [],
                                 "line2_b": [],
                                 'line2_c': [],
                                 'line2_d': [],
                                 'line2_length': [],
                                 'line0_length': [],
                                 'line3_length': [],
                                 'line0_type': [],
                                 'line1_type': [],
                                 'line2_type': [],
                                 'line3_type': [],
                                 }
    
    def read_lcm(self):
        channel_starting_time, timestamp, packets = unpack_packets(self.dataframe, "abChassis")  # 车身底盘数据
        self.chassis_dict['chassis_channel_starting_time'] = channel_starting_time
        self.chassis_dict['chassis_timestamp'] = timestamp
        chassis = chassis_pb2.Chassis()
        for i, packet in enumerate(packets):
            chassis.ParseFromString(packet)
            self.chassis_dict['chassis_vehicle_speed'].append(chassis.vehicle_speed.vehicle_speed * 3.6)
            self.chassis_dict['chassis_maximum_user_speed'].append(chassis.maximum_user_speed)

        channel_starting_time, timestamp, packets = unpack_packets(self.dataframe, "abL10n")  # 车身底盘数据
        self.gps_imu_dict['gps_imu_channel_starting_time'] = channel_starting_time
        self.gps_imu_dict['gps_imu_timestamp'] = timestamp
        gps = gps_imu_info_pb2.gpsImu()
        for i, packet in enumerate(packets):
            gps.ParseFromString(packet)
            self.gps_imu_dict["gps_latitude"].append(gps.latitude)
            self.gps_imu_dict["gps_longitude"].append(gps.longitude)
            self.gps_imu_dict["gps_yaw"].append(gps.yaw)
            # 计算大地坐标系
            x, y = self.transformer.transform(gps.latitude, gps.longitude)
            self.gps_imu_dict["UTM_X"].append(x - self.dot_x)
            self.gps_imu_dict["UTM_Y"].append(y - self.dot_y)
            aa = -gps.yaw
            b = aa + math.pi / 2
            c = (b + math.pi) % (2 * math.pi)
            if c < 0.0:
                c = c + 2 * math.pi
            d = c - math.pi
            self.gps_imu_dict["heding"].append(d - math.pi / 2)

        channel_starting_time, timestamp, packets = unpack_packets(self.dataframe, 'abCamera')  # camera数据
        camera_info = mobileye_pb2.MobileyeInfo()
        self.camera_info_dict['timestamp'].append(timestamp)  # 获取时间戳
        for i, packet in enumerate(packets):
            camera_info.ParseFromString(packet)
            self.camera_info_dict['center_length'].append(camera_info.center_line.length)
            self.camera_info_dict['line1_a'].append(camera_info.line[1].a)
            self.camera_info_dict['line1_b'].append(camera_info.line[1].b)
            self.camera_info_dict['line1_c'].append(camera_info.line[1].c)
            self.camera_info_dict['line1_d'].append(camera_info.line[1].d)
            self.camera_info_dict['line1_length'].append(camera_info.line[1].length)

            self.camera_info_dict['line2_a'].append(camera_info.line[2].a)
            self.camera_info_dict['line2_b'].append(camera_info.line[2].b)
            self.camera_info_dict['line2_c'].append(camera_info.line[2].c)
            self.camera_info_dict['line2_d'].append(camera_info.line[2].d)
            self.camera_info_dict['line2_length'].append(camera_info.line[2].length)

            self.camera_info_dict['line0_length'].append(camera_info.line[0].length)
            self.camera_info_dict['line3_length'].append(camera_info.line[3].length)

            self.camera_info_dict['line0_type'].append(camera_info.line[0].type)
            self.camera_info_dict['line1_type'].append(camera_info.line[1].type)
            self.camera_info_dict['line2_type'].append(camera_info.line[2].type)
            self.camera_info_dict['line3_type'].append(camera_info.line[3].type)
