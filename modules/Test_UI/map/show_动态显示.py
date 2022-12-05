from configobj import ConfigObj
import matplotlib.pyplot as plt
from listens_lcm import ListensLcmAll
from pyproj import Transformer
from threading import Thread
import time

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
# 获取监听数据并数值转化

listens = ListensLcmAll()
listens.start_receiving()

transformer = Transformer.from_crs("EPSG:4326", "EPSG:32650")


def run():
    while True:
        global xx
        global yy
        x, y = transformer.transform(listens.gps_imu_dict['gps'][1], listens.gps_imu_dict['gps'][0])
        xx = x - 522149
        yy = y - 4320960
t = Thread(target=run)
t.start()


plt.ion()  # 开启interactive mode 成功的关键函数
plt.figure(1)
for i in range(2000):
    time.sleep(1)
    print(xx, yy)
    plt.clf()
    plt.plot(line_x, line_y)
    plt.plot(line_1x, line_1y,marker=' ', linestyle='--')
    plt.plot(line_2x, line_2y,marker=' ', linestyle='--')
    plt.figure(1, figsize=(xx, yy), dpi=80)
    a = plt.subplot()
    a.set_ylim(yy-50,yy+50)
    a.set_xlim(xx-50,xx+50)
    plt.plot(xx,yy,marker='o',color = 'r')
    plt.pause(0.01)