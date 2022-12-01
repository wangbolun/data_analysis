import math
from pyproj import Transformer
import matplotlib.pyplot as plt
from lcm_utilities import ReadLcmAll
import modules.common.data_struct.proto.drivers.camera.mobileye_pb2 as mobileye_pb2
import modules.common.data_struct.proto.localization.gps_imu_info_pb2 as gps_imu_info_pb2


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
            self.gps_info_dict["UTM_X"].append(x-self.dot_x)
            self.gps_info_dict["UTM_Y"].append(y-self.dot_y)
            # self.gps_info_dict["heding"].append((-gps.yaw) + math.pi / 2 - math.pi / 2)
            # pp = (-gps.yaw + math.pi / 2)
            # aa = (pp + math.pi) % (2 * math.pi)
            # if aa < 0:
            #     aa += 2 * math.pi
            # self.gps_info_dict["heding"].append((aa - math.pi) - math.pi / 2)
            aa = -gps.yaw
            b = aa + math.pi / 2
            c = (b + math.pi) % (2 * math.pi)
            if c < 0.0 :
                c = c + 2 * math.pi
            d = c - math.pi
            self.gps_info_dict["heding"].append(d - math.pi / 2)

            #print(gps.yaw,(aa - math.pi) - math.pi / 2)

        # camera
        channel_starting_time, timestamp, packets = a.unpack_packets(dataframe, "abCamera")  # GPS
        camera_info = mobileye_pb2.MobileyeInfo()
        self.camera_info_dict["utime"].append(timestamp)
        for i, packet in enumerate(packets):
            camera_info.ParseFromString(packet)
            self.camera_info_dict["line_a"].append(camera_info.center_line.a)
            self.camera_info_dict["line1_a"].append(camera_info.line[1].a)
            self.camera_info_dict["line2_a"].append(camera_info.line[2].a)

        # 计算
        gx = []
        gy = []
        gx1 = []
        gy1 = []
        gx2 = []
        gy2 = []
        aa = []
        bb = []
        vv = []
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
                    vv.append(math.sqrt((e * math.cos(f)-(o * math.cos(f)))**2+(e * math.sin(f)-o * math.sin(f))**2))
            # print(vv[-1],gx1[-1],gy1[-1],gx2[-1],gy2[-1])

        plt.figure(None, (12, 13), dpi=95)
        ax = plt.gca()
        ax.set_aspect(1)
        plt.subplot(2, 1, 1)
        plt.plot(gx, gy, marker='.', linestyle=' ')
        plt.plot(gx1, gy1, marker='.', linestyle=' ')
        plt.plot(gx2, gy2, marker='.', linestyle=' ')
        plt.plot(self.gps_info_dict["UTM_X"], self.gps_info_dict["UTM_Y"])

        plt.subplot(2, 1, 2)
        # 绘图数值
        plt.plot(self.gps_info_dict["utime"][0], self.gps_info_dict["yaw"], label="yaw")
        plt.plot(self.gps_info_dict["utime"][0], self.gps_info_dict["heding"], label="heding")
        plt.plot(aa, bb, label="camera")
        plt.plot(aa, vv, label="gy")
        plt.legend()
        while True:
            pos = plt.ginput(2)
            if len(pos) == 2:
                print(pos)
                print(math.sqrt((pos[0][0] - pos[1][0]) ** 2 + ((pos[0][1] - pos[1][1])) ** 2))


if __name__ == '__main__':
    c = Show()
    c.read_lcm()