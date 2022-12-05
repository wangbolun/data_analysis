from read_lcm import ReadLcmAll
from configobj import ConfigObj
import matplotlib.pyplot as plt
import numpy as np
import math

# 读取配置文件，并赋值给制定位置
line_x = []
line_y = []
line_1x = []
line_1y = []
line_2x = []
line_2y = []
config = ConfigObj('/home/wbl/2CAR/data_analysis/modules/control/LingK/Test_UI/tools/map.ini')
value1 = config['line_map']['line-']
value2 = config['line_map']['line+']
value3 = config['line_map']['line1-']
value4 = config['line_map']['line1+']
value5 = config['line_map']['line2-']
value6 = config['line_map']['line2+']

for a, b, c, d, e, f in zip(value1, value2, value3, value4, value5, value6):
    line_x.append(float(a))
    line_y.append(float(b))
    line_1x.append(float(c))
    line_1y.append(float(d))
    line_2x.append(float(e))
    line_2y.append(float(f))

# 读取数据并转化坐标系
data = ReadLcmAll('/home/wbl/LingK16.11.31')
data.read_lcm()

while True:
    a = int(input('请输入一个数值'))
    heding = (data.gps_imu_dict['heding'][a])
    # 转换车辆坐标系
    gx1 = []
    gy1 = []
    gx2 = []
    gy2 = []
    for p, b, c, d, e, f in zip(value1, value2, value3, value4, value5, value6):
        line_x.append(float(p))
        line_y.append(float(b))
        line_1x.append(float(c))
        line_1y.append(float(d))
        line_2x.append(float(e))
        line_2y.append(float(f))
        print(float(c),(float(d)),(data.gps_imu_dict['UTM_X'][a]))
        gx1.append((float(c) * math.cos(-heding) - (float(d) * math.sin(-heding))) - (data.gps_imu_dict['UTM_X'][a]))
        gy1.append((float(c) * math.sin(-heding) + (float(d) * math.cos(-heding))) - (data.gps_imu_dict['UTM_Y'][a]))
        gx2.append((float(e) * math.cos(-heding) - (float(f) * math.sin(-heding))) - (data.gps_imu_dict['UTM_X'][a]))
        gy2.append((float(e) * math.sin(-heding) + (float(f) * math.cos(-heding))) - (data.gps_imu_dict['UTM_Y'][a]))


    y = np.linspace(-data.camera_info_dict['line1_length'][a], data.camera_info_dict['line1_length'][a], 100)
    x = data.camera_info_dict['line1_a'][a] + data.camera_info_dict['line1_b'][a] * y + \
        data.camera_info_dict['line1_c'][a] * y ** 2 + data.camera_info_dict['line1_d'][a] * y ** 3
    y1 = np.linspace(-data.camera_info_dict['line2_length'][a], data.camera_info_dict['line2_length'][a], 100)
    x1 = data.camera_info_dict['line2_a'][a] + data.camera_info_dict['line2_b'][a] * y + \
         data.camera_info_dict['line2_c'][a] * y ** 2 + data.camera_info_dict['line2_d'][a] * y ** 3
    ax1 = plt.subplot()
    ax1.clear()
    ax1.set_ylim(ymax=180)
    ax1.set_xlim(xmin=-40, xmax=40)
    plt.plot(x, y, marker='.', linestyle=' ', color='red')
    plt.plot(x1, y1, marker='.', linestyle=' ', color='red')
    plt.plot(gx1,gy1)
    plt.plot(gx2,gy2)
    # plt.plot([2,-1],[2,1],[-2,-1],[2,-1],color='red')
    plt.show()
