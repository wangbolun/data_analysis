import math
from pyproj import Transformer
import matplotlib.pyplot as plt
from lcm_utilities import ReadLcmAll
import modules.common.data_struct.proto.drivers.camera.mobileye_pb2 as mobileye_pb2
import modules.common.data_struct.proto.localization.gps_imu_info_pb2 as gps_imu_info_pb2


# 地图生成器

class Show:
    def __init__(self):
        self.dot_x = 522149
        self.dot_y = 4320960

        self.gps_info_dict = {"utime": [],
                              "UTM_X": [],
                              "UTM_Y": [],
                              "yaw": [],
                              "wey4_velocity": [],
                              "heding": [],
                              "max_stime": '',
                              }
        self.camera_info_dict = {"utime": [],
                                 "line_a": [],
                                 "line1_a": [],
                                 "line2_a": [],
                                 }

    def read_lcm(self):
        a = ReadLcmAll()
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32650")
        dataframe = a.get_lcm_dataset(
            '/home/wbl/LingK16.11.31')
        channel_starting_time, timestamp, packets = a.unpack_packets(dataframe, "abL10n")  # GPS
        self.gps_info_dict["utime"].append(timestamp)
        gps = gps_imu_info_pb2.gpsImu()
        for i, packet in enumerate(packets):
            gps.ParseFromString(packet)
            self.gps_info_dict["yaw"].append(gps.yaw)
            x, y = transformer.transform(gps.latitude, gps.longitude)
            self.gps_info_dict["UTM_X"].append(x - self.dot_x)
            self.gps_info_dict["UTM_Y"].append(y - self.dot_y)
            # self.gps_info_dict["heding"].append((-gps.yaw) + math.pi / 2 - math.pi / 2)
            # pp = (-gps.yaw + math.pi / 2)
            # aa = (pp + math.pi) % (2 * math.pi)
            # if aa < 0:
            #     aa += 2 * math.pi
            # self.gps_info_dict["heding"].append((aa - math.pi) - math.pi / 2)
            # 航向转化
            aa = -gps.yaw
            b = aa + math.pi / 2
            c = (b + math.pi) % (2 * math.pi)
            if c < 0.0:
                c = c + 2 * math.pi
            d = c - math.pi
            self.gps_info_dict["heding"].append(d - math.pi / 2)

        # camera
        channel_starting_time, timestamp, packets = a.unpack_packets(dataframe, "abCamera")  # GPS
        camera_info = mobileye_pb2.MobileyeInfo()
        self.camera_info_dict["utime"].append(timestamp)
        for i, packet in enumerate(packets):
            camera_info.ParseFromString(packet)
            self.camera_info_dict["line_a"].append(camera_info.center_line.a)
            self.camera_info_dict["line1_a"].append(camera_info.line[1].a)
            self.camera_info_dict["line2_a"].append(camera_info.line[2].a)

        # 计算大地坐标系下位置
        gx = []
        gy = []
        gx1 = []
        gy1 = []
        gx2 = []
        gy2 = []
        aa = []
        bb = []
        vv = []
        cxx = []
        cyy = []
        for a, x, y, f in zip(self.gps_info_dict["utime"][0], self.gps_info_dict["UTM_X"], self.gps_info_dict["UTM_Y"],
                              self.gps_info_dict["heding"]):
            for p, d, e, o in zip(self.camera_info_dict["utime"][0], self.camera_info_dict["line_a"],
                                  self.camera_info_dict["line1_a"], self.camera_info_dict["line2_a"]):
                if "%.2f" % a == "%.2f" % p:
                    gx.append(d * math.cos(f) + x)
                    gy.append(d * math.sin(f) + y)

                    gx1.append(e * math.cos(f) + x)
                    gy1.append(e * math.sin(f) + y)

                    gx2.append(o * math.cos(f) + x)
                    gy2.append(o * math.sin(f) + y)

                    aa.append(a)
                    bb.append(-(e - o))
                    # vv.append(e * math.sin(f) - o * math.sin(f))
                    # 显示使用
                    vv.append(math.sqrt(
                        (e * math.cos(f) - (o * math.cos(f))) ** 2 + (e * math.sin(f) - o * math.sin(f)) ** 2))

                    # 验证大地坐标系转车辆坐标系(成功)
                    x1 = (o * math.cos(f))
                    x2 = (o * math.sin(f))
                    cx = (x1 * math.cos(-f) - (x2 * math.sin(-f)))
                    cy = (x1 * math.sin(-f) + (x2 * math.cos(-f)))
                    # 验证大地转车辆坐标系（成功）
                    x1 = (o * math.cos(f) + x)
                    x2 = (o * math.sin(f) + y)
                    cxx.append((x1 * math.cos(-f) - (x2 * math.sin(-f))) - x)
                    cyy.append((x1 * math.sin(-f) + (x2 * math.cos(-f))) - y)

        # 将数组写入配置文件
        from configobj import ConfigObj
        config = ConfigObj()
        config.filename = './map.ini'
        config['line_map'] = {}
        config['line_map']['line-'] = gx
        config['line_map']['line+'] = gy
        config['line_map']['line1-'] = gx1
        config['line_map']['line1+'] = gy1
        config['line_map']['line2-'] = gx2
        config['line_map']['line2+'] = gy2
        config.write()

        # 画图展示
        plt.figure(None, (12, 13), dpi=95)
        ax = plt.gca()
        ax.set_aspect(1)
        plt.subplot(2, 1, 1)
        plt.plot(gx, gy, marker='.', linestyle=' ', label="line_a")
        plt.plot(gx1, gy1, marker='.', linestyle=' ', label="line1_a")
        plt.plot(gx2, gy2, marker='.', linestyle=' ', label="line2_a")
        plt.plot(self.gps_info_dict["UTM_X"], self.gps_info_dict["UTM_Y"], label="GPS")
        plt.legend()

        plt.subplot(2, 1, 2)
        # 绘图数值
        plt.plot(self.gps_info_dict["utime"][0], self.gps_info_dict["yaw"], label="yaw")
        # plt.plot(self.gps_info_dict["utime"][0], self.gps_info_dict["heding"], label="heding")
        plt.plot(aa, bb, label="camera")
        plt.plot(aa, vv, label="gy")
        plt.legend()
        plt.show()

if __name__ == '__main__':
    c = Show()
    c.read_lcm()
