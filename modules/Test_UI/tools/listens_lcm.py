import lcm
import threading
from modules.common.data_struct.proto.drivers.camera import mobileye_pb2
from modules.common.data_struct.proto.localization import gps_imu_info_pb2
from modules.common.data_struct.proto.vehicle import chassis_pb2
from modules.common.data_struct.lcm.localization import gps_imu_info_t

class ListensLcmAll:
    def __init__(self):
        self.lcm = lcm.LCM()
        self.lcm.subscribe('abCamera', self.camera_info)
        self.lcm.subscribe('abL10n', self.gps_imu_info)
        self.lcm.subscribe('abChassis', self.chassis_info)
        self.lanes_coeff_dict = {
            "lane_left_most": [0, 0, 0, 0, 0],
            "lane_left_middle": [0, 0, 0, 0, 0],
            "lane_right_middle": [0, 0, 0, 0, 0],
            "lane_right_most": [0, 0, 0, 0, 0],
            "center_line": [0, 0, 0, 0, 0],
            "lane_type": [0, 0, 0, 0]
        }
        self.gps_imu_dict = {
            "header": [0, 0],
            "gps": [0, 0, 0, 0, 0, 0, 0, 0],
            "imu": [0, 0, 0],
        }
        self.chassis_dict = {
            "state": [0, 0, 0, 0, 0, 0, 0, 0]
        }

    def lcm_receiver(self):
        while True:
            self.lcm.handle()

    def start_receiving(self):
        t1 = threading.Thread(target=self.lcm_receiver, name="lcm_receiver")
        t1.setDaemon(True)
        t1.start()

    def camera_info(self, channel, data):
        camera_info = mobileye_pb2.MobileyeInfo()
        camera_info.ParseFromString(data)
        self.lanes_coeff_dict["lane_left_most"][0] = camera_info.line[0].a
        self.lanes_coeff_dict["lane_left_most"][1] = camera_info.line[0].b
        self.lanes_coeff_dict["lane_left_most"][2] = camera_info.line[0].c
        self.lanes_coeff_dict["lane_left_most"][3] = camera_info.line[0].d
        self.lanes_coeff_dict["lane_left_most"][4] = "%.0f" % camera_info.line[0].length
        self.lanes_coeff_dict["lane_left_middle"][0] = camera_info.line[1].a
        self.lanes_coeff_dict["lane_left_middle"][1] = camera_info.line[1].b
        self.lanes_coeff_dict["lane_left_middle"][2] = camera_info.line[1].c
        self.lanes_coeff_dict["lane_left_middle"][3] = camera_info.line[1].d
        self.lanes_coeff_dict["lane_left_middle"][4] = "%.0f" % camera_info.line[1].length
        self.lanes_coeff_dict["lane_right_middle"][0] = camera_info.line[2].a
        self.lanes_coeff_dict["lane_right_middle"][1] = camera_info.line[2].b
        self.lanes_coeff_dict["lane_right_middle"][2] = camera_info.line[2].c
        self.lanes_coeff_dict["lane_right_middle"][3] = camera_info.line[2].d
        self.lanes_coeff_dict["lane_right_middle"][4] = "%.0f" % camera_info.line[2].length
        self.lanes_coeff_dict["lane_right_most"][0] = camera_info.line[3].a
        self.lanes_coeff_dict["lane_right_most"][1] = camera_info.line[3].b
        self.lanes_coeff_dict["lane_right_most"][2] = camera_info.line[3].c
        self.lanes_coeff_dict["lane_right_most"][3] = camera_info.line[3].d
        self.lanes_coeff_dict["lane_right_most"][4] = "%.0f" % camera_info.line[3].length
        self.lanes_coeff_dict["center_line"][0] = "%.2f" % camera_info.center_line.a
        self.lanes_coeff_dict["center_line"][1] = camera_info.center_line.b
        self.lanes_coeff_dict["center_line"][2] = camera_info.center_line.c
        self.lanes_coeff_dict["center_line"][3] = camera_info.center_line.d
        self.lanes_coeff_dict["center_line"][4] = "%.2f" % camera_info.center_line.length
        self.lanes_coeff_dict["lane_type"][0] = camera_info.line[0].type
        self.lanes_coeff_dict["lane_type"][1] = camera_info.line[1].type
        self.lanes_coeff_dict["lane_type"][2] = camera_info.line[2].type
        self.lanes_coeff_dict["lane_type"][3] = camera_info.line[3].type

    def gps_imu_info(self, channel, data):
        gps = gps_imu_info_pb2.gpsImu()
        gps.ParseFromString(data)
        self.gps_imu_dict["header"][0] = gps.header.timestamp_sec
        self.gps_imu_dict["header"][1] = gps.header.sequence_num
        self.gps_imu_dict["gps"][0] = gps.longitude
        self.gps_imu_dict["gps"][1] = gps.latitude
        self.gps_imu_dict["gps"][2] = "%.8f" % gps.yaw
        self.gps_imu_dict["gps"][3] = gps.altitude
        self.gps_imu_dict["gps"][4] = "%.2f" % gps.velocity
        self.gps_imu_dict["gps"][5] = gps.location_status  # 定位模式
        self.gps_imu_dict["gps"][6] = gps.satellite_number  # 卫星数量
        self.gps_imu_dict["gps"][7] = gps.vehicle_speed_enable
        self.gps_imu_dict["imu"][0] = gps.yaw_rate  # 横摆角速度
        self.gps_imu_dict["imu"][1] = gps.acceleration_longitudinal  # 纵向加速度
        self.gps_imu_dict["imu"][2] = gps.acceleration_lateral  # 横向加速度

    def chassis_info(self, channel, data):
        chassis = chassis_pb2.Chassis()
        chassis.ParseFromString(data)
        self.chassis_dict["state"][0] = chassis.driving_mode  # 自驾模式
        self.chassis_dict["state"][1] = chassis.steering_angle  # 方向盘转角
        self.chassis_dict["state"][2] = chassis.steering_rate  # 方向盘转速
        self.chassis_dict["state"][3] = chassis.maximum_user_speed
        self.chassis_dict["state"][4] = "%.2f" % chassis.vehicle_speed.vehicle_speed
        self.chassis_dict["state"][5] = chassis.vehicle_signal.turn_signal  # 拨杆状态
        self.chassis_dict["state"][6] = chassis.vehicle_signal.fog_light  # 换道状态
        self.chassis_dict["state"][7] = chassis.vehicle_signal.epb_sts_epb_sts  # 手刹


class ListensLcmAll_VV6:
    def __init__(self):
        self.lcm = lcm.LCM()
        self.lcm.subscribe('GPS_DATA', self.gps_imu_info_t)
        self.vv6_gps_imu_dict = {
            "gps": [0, 0, 0, 0, 0, 0, 0, 0]
        }

    def lcm_receiver(self):
        while True:
            self.lcm.handle()

    def start_receiving(self):
        t1 = threading.Thread(target=self.lcm_receiver, name="lcm_receiver")
        t1.setDaemon(True)
        t1.start()

    def gps_imu_info_t(self,channel, data):
        gps = gps_imu_info_t.decode(data)
        self.vv6_gps_imu_dict["gps"][0] = gps.longitude
        self.vv6_gps_imu_dict["gps"][1] = gps.latitude
        self.vv6_gps_imu_dict["gps"][2] = "%.8f" % gps.yaw
        self.vv6_gps_imu_dict["gps"][3] = gps.altitude
        self.vv6_gps_imu_dict["gps"][4] = "%.2f" % gps.velocity
        self.vv6_gps_imu_dict["gps"][5] = gps.locationStatus  # 定位模式
        self.vv6_gps_imu_dict["gps"][6] = gps.satelliteNumber  # 卫星数量
