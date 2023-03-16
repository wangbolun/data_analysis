import os
import time
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from static.lcm import lca_debug_pb2
from static.lcm import gps_imu_info_pb2
from tools.connect_lcm import PushLcmState
from tools.connect_lcm import PullLcmName
from tools.lcm_utilities import ReadLcmAll
from tools.lcm_utilities_old import unpack_packets  # 解包工具
import mpl_toolkits.axisartist as axisartist

# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit
# app = QApplication([])

zdhq=os.path.join(os.getcwd(),'pic/')

def BSD_gongneng(ttrs):
    APP = ReadLcmAll()  # 实例化
    lcmlog_dataframe=APP.get_lcm_dataset(
        ttrs)
    lookup = APP.lookup_data()
    # print(APP.gps_info_dict)
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']

    channel_starting_time, timestamp, packets = unpack_packets(lcmlog_dataframe, "abLcaDebug")
    bsd = lca_debug_pb2.LCADebug()
    r = []
    l = []
    ddd = []
    ztj = []
    reason=[]
    turnsignals=[]
    for i, packet in enumerate(packets):
        bsd.ParseFromString(packet)
        #print(bsd.debug_analy_chassis.turnsignal)
        xxx = (bsd.debug_analy_obstacles.obstacle_info)
        r.append(bsd.bsd_warn_right)
        l.append(bsd.bsd_warn_left)
        turnsignals.append(bsd.debug_analy_chassis.turnsignal)
        ddd.append(xxx)
        ztj.append(bsd.bsd_state_machine)
        reason.append(bsd.bsd_inhibit_reason)
        # print(turnsignals)
        # print(reason)
        # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        velocitys = []
        longitudes = []
        latitudes = []
        channel_starting_time1, timestamp1, packets1 = unpack_packets(lcmlog_dataframe, "abL10n")
        gps = gps_imu_info_pb2.gpsImu()
        for i, packet in enumerate(packets1):
            gps.ParseFromString(packet)
            velocitys.append(gps.velocity * 3.6)
            longitudes.append(gps.longitude)
            latitudes.append(gps.latitude)

    z1 = []
    z2 = []
    Tutime = []
    Ttimestamp = []
    yjl = []
    xjl = []
    zbj = []
    ybj = []
    ztj1 = []
    Tturnsignal=[]
    for a, b, c, w, h, y, n, m, o,p in zip(velocitys, wey4_velocity, UTM_X, timestamp1, utime, UTM_Y, l, r, ztj,turnsignals):
        w1 = round(w, 2)
        h1 = round(h, 2)
        if h1 == w1:
            Tutime.append(h)
            Ttimestamp.append(w)
            z1.append(a)
            z2.append(b)
            yjl.append(y)
            xjl.append(c)
            zbj.append(n)
            ybj.append(m)
            ztj1.append(o)
            Tturnsignal.append(p)
    for a,b,c,d,e in zip(z2,z1,Tutime,xjl,yjl):
        if a == max(z2):
            pv1=a
            pv1t=c
        elif a == min(z2):
            pv2=a
            pv2t=c
        if b == max(z1):
            mv1=b
            mv1t=c
        elif b == min(z1):
            mv2=b
            mv2t=c
        if d == max(xjl):
            xd1=d
            xd1t=c
        elif d == min(xjl):
            xd2=d
            xd2t=c
        if e == max(yjl):
            yd1=e
            yd1t=c
        elif e == min(yjl):
            yd2=e
            yd2t=c




    gv1=max(z2)    #
    gv2=min(z2)

    total=sum(z2)       #平均速度
    vp1=total / len(z2)    #配合车平均速度
    total1=sum(z1)
    vp2=total1 / len(z1)   #测试车平均速度

    totalx=sum(xjl)
    xp1=totalx / len(xjl) #配合车平均X
    totaly=sum(yjl)
    xp2=totaly / len(yjl)  #配合车平均Y



    bj = []
    if xjl[0]<0:
        bj=zbj
    elif xjl[0]>0 :
        bj=ybj



    xx1 = [a - b for a, b in zip(z2, z1)]

    tt = []
    bnm = []
    for i in xx1:
        tt.append(i / 3.6)
    for i in yjl:
        bnm.append(i - 4.5)
    xx2 = [e / f for e, f in zip(bnm, tt)]  # 利用该语句实现
    xx3 = []
    for a in xx2:
        xx3.append(abs(a))

    ww1 = []
    xwz = []
    ywz = []
    zsd = []
    ttcc = []
    ts=[]
    for a, b, c, d, e, f in zip(bj, Tutime, xjl, yjl, z2, xx3):
        if a == 1 or a == 2:
            ts.append(a)
            ww1.append(b)
            xwz.append(c)
            ywz.append(d)
            zsd.append(e)
            ttcc.append(f)

    for a, b, c, d, e in zip(xwz, ywz, ww1, zsd, ttcc):
        if a == xwz[len(xwz) // 2]:
            xzd = a
            yzd = b
            tt3 = c
            vv3 = d
            ttc3 = e

    for a, b, c, d in zip(Tutime, xjl, yjl, z2):
        if a == min(ww1):

            ww2 = b
            ww3 = c
            tt1 = min(ww1)
            vv1 = d
            ttc1 = e
        elif a == max(ww1):
            tt2 = max(ww1)

            ww4 = b
            ww5 = c
            vv2 = d
            ttc2 = e
        elif a == 0:

            tt4 = a
            ww6 = b
            ww7 = c
            vv4 = d
            ttc4 = e
        elif a == Tutime[-1]:


            tt5 = a

            ww8 = b
            ww9 = c
            vv5 = d
            ttc5 = e
    bjjd=[]
    bjjdt=[]
    for a,b in zip (bj,Tutime):
        if min(ww1) <= b <= max(ww1):
            bjjd.append(a)
            bjjdt.append(b)
    # print(bjjd)
    mm1=[]
    mm2=[]
    for a in bjjd:
        if a == 1:
            mm1.append(a)
            if len(mm1) == len(bjjd):
                qqc = "本次测试的报警方式为一阶段报警。"
            elif bjjd[0]>bjjd[-1]:
                qqc = "本次测试的报警方式为二阶段跳一阶段报警。"
            elif bjjd[0]<bjjd[-1]:
                qqc = "本次测试的报警方式为一阶段跳二阶段报警。"

        elif a == 2:
            mm2.append(a)
            if len(mm2) == len(bjjd):
                qqc = "本次测试的报警方式为二阶段报警。"

    # if all(el==1 for el in bjjd):
    #     print('11111111111111')
    #     qqc="本次测试为一阶段报警"
    #     print("纯一阶段报警")
    # elif all(el==2 for el in bjjd):
    #     qqc = "本次测试为二阶段报警"
    #     print("纯二阶段报警")
    # else:
    #     if bjjd[0] >  bjjd[-1]:
    #         qqc = "本次测试为二阶段跳一阶段报警"
    #         print("二阶段跳一阶段")
    #     else:
    #         qqc = "本次测试为一阶段跳二阶段报警"
    #         print("一阶段跳二阶段")

    for a,b in zip (bjjd,bjjdt):
        if a == 0 :
            cw = a
            cwt=b
            mark="如上图红叉标注位置，在报警区间，出现报警信号中断，不符合场景，所以不通过"
            break
        else:
            cwt=None
            cw=None
            mark=""
    # 车速匹配
    sp=APP.case_info_dict['key']
    if sp[2] - 0.3 * sp[2] <= vp2 <= sp[2] + 0.3 * sp[2] :
        print('被测车速度匹配正常')
        if sp[7] - 0.3 * sp[7] <= vp1 <= sp[7] + 0.3 * sp[7]:
            print('配合车速度匹配正常')
            pps="本次测试被测车平均车速为：%0.1f" % vp2 +'km/h'+ ",测试用例场景所需车速为：%0.1f" % sp[2]+'km/h \n' \
            "本次测试配合车平均车速为：%0.1f" % vp1+'km/h' + ",测试用例场景所需车速为：%0.1f" % sp[7]+'km/h \n' \
            '通过分析，两车速度均在测试用例允许误差范围内，速度匹配正常。'

        else:
            print('配合车速度匹配失败')
            pps="本次测试被测车平均车速为：%0.1f" % vp2 +'km/h'+ ",测试用例场景所需车速为：%0.1f" % sp[2]+'km/h \n' \
            "本次测试配合车平均车速为：%0.1f" % vp1+'km/h' + ",测试用例场景所需车速为：%0.1f" % sp[7]+'km/h \n' \
            '通过分析，两车速度不在测试用例允许误差范围内，速度匹配失败。'

    else:
        print('被测车速度匹配失败')

    # print(pps)




    cd=[]
    cd2=[]
    warn_x = [ww2, xzd, ww4]
    warn_y = [ww3, yzd, ww5]

    if a != 0 in bj:
        pr = '在测试场景下存在报警功能，测试通过，该用例通过。'
    else:
        pr = '在测试场景下不存在报警功能，测试不通过，该用例不通过。'

    # ----------------------1.创建画布并引入axisartist工具------------------
    fig = plt.figure(figsize=(18, 12))  # 创建画布
    # 使用axisartist.Subplot方法创建一个绘图区对象ax
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中

    # ----------2. 绘制带箭头的x-y坐标轴#通过set_visible方法设置绘图区所有坐标轴隐藏-------
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    # ax.new_floating_axis代表添加新的坐标轴
    ax.axis["x"] = ax.new_floating_axis(0, 0)
    ax.axis["x"].set_axisline_style("->", size=1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1, 0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size=1.0)
    # 设置x、y轴上刻度显示方向
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")

    # -----------3. 在带箭头的x-y坐标轴背景下，绘制函数图像#生成x步长为0.1的列表数据----------
    x = np.arange(-15, 15, 0.1)
    y = 1 / (1 + np.exp(-x))  # 生成sigmiod形式的y数据
    # 设置x、y坐标轴的范围
    plt.ylim(-40, 40)
    plt.xlim(-40, 40)
    plt.axvline(x=-1.875, ls='--' ,c='k')      #车道线
    plt.axvline(x=-5.625, ls='--' ,c='k')
    plt.axvline(x=1.875, ls='--' ,c='k')
    plt.axvline(x=5.625, ls='--' ,c='k')
    #plt.axhline(y=10, ls='--', c='blue') # 添加水平线    平行于x轴
    # 左报警区间
    plt.plot([-1.4, -3.9, -1.4, -1.4, -1.4, -3.9, -3.9, -3.9], [1.315, 1.315, 1.315, -6, -6, -6, 1.315, -6], 'r:')
    # 右报警区间
    plt.plot([1.4, 3.9, 1.4, 1.4, 1.4, 3.9, 3.9, 3.9], [1.315, 1.315, 1.315, -6, -6, -6, 1.315, -6], 'r:')

    plt.plot(ww6, ww7, ".")  # 时间开始时刻（t=0）
    plt.plot([ww6 - 0.9, ww6 + 0.9, ww6 - 0.9, ww6 - 0.9, ww6 - 0.9, ww6 + 0.9, ww6 + 0.9, ww6 + 0.9],
             [ww7 - 0.9, ww7 - 0.9, ww7 - 0.9, ww7 + 3.7, ww7 + 3.7, ww7 + 3.7, ww7 + 3.7, ww7 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt4 + ' s', xy=(ww6, ww7), xytext=((ww6 - 10), ww7),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv4 + ' km/h', xy=(ww6, ww7), xytext=((ww6 - 10), (ww7 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc4 + ' s', xy=(ww6, ww7), xytext=((ww6 - 10), (ww7 + 2)),
    #              color="b")

    plt.plot(ww8, ww9, ".")  # 时间结束时刻（t=最后一秒）
    plt.plot([ww8 - 0.9, ww8 + 0.9, ww8 - 0.9, ww8 - 0.9, ww8 - 0.9, ww8 + 0.9, ww8 + 0.9, ww8 + 0.9],
             [ww9 - 0.9, ww9 - 0.9, ww9 - 0.9, ww9 + 3.7, ww9 + 3.7, ww9 + 3.7, ww9 + 3.7, ww9 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt5 + ' s', xy=(ww8, ww9), xytext=((ww8 - 10), ww9),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv5 + ' km/h', xy=(ww8, ww9), xytext=((ww8 - 10), (ww9 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc5 + ' s', xy=(ww8, ww9), xytext=((ww8 - 10), (ww9 + 2)),
    #              color="b")

    plt.plot(ww2, ww3, ".")  # 开始报警时刻
    plt.plot([ww2 - 0.9, ww2 + 0.9, ww2 - 0.9, ww2 - 0.9, ww2 - 0.9, ww2 + 0.9, ww2 + 0.9, ww2 + 0.9],
             [ww3 - 0.9, ww3 - 0.9, ww3 - 0.9, ww3 + 3.7, ww3 + 3.7, ww3 + 3.7, ww3 + 3.7, ww3 - 0.9], 'green')
    # plt.plot([ww2-0.9,ww2+0.9],[ww3-0.9,ww3-0.9])      #最下面的一行
    # plt.plot([ww2-0.9,ww2-0.9],[ww3-0.9,ww3+3.7])    #左
    # plt.plot([ww2-0.9,ww2+0.9],[ww3+3.7,ww3+3.7])    #上
    # plt.plot([ww2+0.9,ww2+0.9],[ww3+3.7,ww3-0.9])      #右
    plt.annotate('time=''%.1f' % tt1 + ' s', xy=(ww2, ww3), xytext=((ww2 - 10), ww3),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv1 + ' km/h', xy=(ww2, ww3), xytext=((ww2 - 10), (ww3 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc1 + ' s', xy=(ww2, ww3), xytext=((ww2 - 10), (ww3 + 2)),
    #              color="b")

    plt.plot(ww4, ww5, "b.")  # 报警结束时刻
    plt.plot([ww4 - 0.9, ww4 + 0.9, ww4 - 0.9, ww4 - 0.9, ww4 - 0.9, ww4 + 0.9, ww4 + 0.9, ww4 + 0.9],
             [ww5 - 0.9, ww5 - 0.9, ww5 - 0.9, ww5 + 3.7, ww5 + 3.7, ww5 + 3.7, ww5 + 3.7, ww5 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt2 + ' s', xy=(ww4, ww5), xytext=((ww4 - 10), ww5),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv2 + ' km/h', xy=(ww4, ww5), xytext=((ww4 - 10), (ww5 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc2 + ' s', xy=(ww4, ww5), xytext=((ww4 - 10), (ww5 + 2)),
    #              color="b")

    plt.plot(xzd, yzd, "b.")  # 报警中间时刻
    plt.plot([xzd - 0.9, xzd + 0.9, xzd - 0.9, xzd - 0.9, xzd - 0.9, xzd + 0.9, xzd + 0.9, xzd + 0.9],
             [yzd - 0.9, yzd - 0.9, yzd - 0.9, yzd + 3.7, yzd + 3.7, yzd + 3.7, yzd + 3.7, yzd - 0.9], 'green')
    plt.annotate('time=''%.1f' % tt3 + ' s', xy=(xzd, yzd), xytext=((xzd - 10), yzd),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv3 + ' km/h', xy=(xzd, yzd), xytext=((xzd - 10), (yzd + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc3 + ' s', xy=(xzd, yzd), xytext=((xzd - 10), (yzd + 2)),
    #              color="b")

    plt.plot(0, 0, "r.")
    plt.plot([-0.9, 0.9, -0.9, -0.9, -0.9, 0.9, 0.9, 0.9], [-1, -1, -1, 3.6, 3.6, 3.6, -1, 3.6], 'purple')  # 被测车坐标位置

    plt.legend(loc=0)
    # plt.show()
    name = zdhq + APP.lcmlog_dict['filename'] + 'p1'
    plt.savefig(name + '.jpg', bbox_inches='tight')


    x = np.linspace(0, 2, 200)
    # fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(4, 1, 1)
    # linestyle=":"
    plt.plot(Tutime, z1, label='VUT_V')
    plt.plot(Tutime, z2, label="GVT_V")

    plt.annotate('GVT_V(max)=''%.1f' % pv1 + ' km/h', xy=(pv1t,pv1 ), xytext=((pv1t - 2), pv1+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('GVT_V(min)=''%.1f' % pv2 + ' km/h', xy=(pv2t,pv2 ), xytext=((pv2t - 2), pv2+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('GVT_V(average)=''%.1f' % vp1 + ' km/h', xy=(Tutime[len(Tutime)//2],vp1 ), xytext=(Tutime[len(Tutime)//2], vp1-1),  # 标注数据
                 color="b")

    plt.annotate('VUT_V(max)=''%.1f' % mv1 + ' km/h', xy=(mv1t,mv1 ), xytext=((mv1t - 2), mv1+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('VUT_V(min)=''%.1f' % mv2 + ' km/h', xy=(mv2t,mv2 ), xytext=((mv2t - 2), mv2+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('VUT_V(average)=''%.1f' % vp2 + ' km/h', xy=(Tutime[len(Tutime)//2],vp2 ), xytext=(Tutime[len(Tutime)//2], vp2+1),  # 标注数据
                 color="b")


    plt.xlabel('time    (s)')
    plt.ylabel('  (km/h)')
    # plt.plot(utime,xx3,label="ttc")
    plt.legend(loc=0)

    plt.subplot(4, 1, 2)  # Add a subplot to the current figure
    # plt.plot(ccc, aaa, ".",color='pink', label='position_x')  # 绘制第一个子图
    plt.plot(Tutime, xjl, label="real_X")
    # plt.plot(Tutime, yjl, label="real_Y")

    plt.annotate('real_X(max)=''%.1f' % xd1 + ' m', xy=(xd1t,xd1 ), xytext=((xd1t - 2), xd1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_X(min)=''%.1f' % xd2 + ' m', xy=(xd2t,xd2 ), xytext=((xd2t - 4), xd2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_X(average)=''%.1f' % xp1 + ' m', xy=(Tutime[len(Tutime)//2],xp1 ), xytext=(Tutime[len(Tutime)//2], xp1),  # 标注数据
                 color="b")



    plt.suptitle('BSD', fontsize=20)
    plt.legend(loc=0)
    plt.xlabel('time    (s)')
    plt.ylabel('  (m)')

    plt.subplot(4, 1, 3)
    # plt.plot(ccc, zzz,'.', color='green', label='y.distance')  # 绘制第三个子图
    # plt.plot(Tutime, xx3, label="ttc")
    plt.plot(Tutime, yjl, label="real_Y")
    plt.annotate('real_Y(max)=''%.1f' % yd1 + ' m', xy=(yd1t,yd1 ), xytext=((yd1t - 2), yd1+2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_Y(min)=''%.1f' % yd2 + ' m', xy=(yd2t,yd2 ), xytext=((yd2t - 2), yd2+2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_Y(average)=''%.1f' % xp2 + ' m', xy=(Tutime[len(Tutime)//2] ,xp2 ), xytext=(Tutime[len(Tutime)//2  ], xp2),  # 标注数据
                 color="b")

    plt.legend(loc=0)
    plt.xlabel('time    (s)')
    plt.ylabel(' (m)')
    # plt.subplots_adjust(hspace=0.6)

    name2= zdhq + APP.lcmlog_dict['filename'] + 'p2'
    plt.savefig(name2+'.jpg',bbox_inches='tight')


    plt.figure(figsize=(18, 12))
    plt.subplot(4, 1, 4)
    plt.plot(Tutime, ybj, color='red', label='warn_right')  # 绘制第四个子图
    plt.plot(Tutime, zbj, label='warn_left')
    if cwt != None:
        plt.plot(cwt,cw,'x',markersize=12,c='r')
    else:
        pass
    plt.plot(Tutime, ztj1, label='state_machine')
    plt.plot(Tutime, Tturnsignal, label='turnsignal')
    plt.legend(loc=0)
    # plt.ylabel('level')
    plt.xlabel('time    (s)')
    # plt.plot(aaa,color="red",linestyle="-",label='tuli')

    # 报警阶段标注
    if 1 in bj:
        plt.annotate('time=''%.1f' % tt1 + ' s', xy=(tt1, 1), xytext=((tt1 - 2), 1),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('start_warn', xy=(tt1, 1), xytext=((tt1 - 2), 2),  # 标注数据
                     color="b")

        plt.annotate('time=''%.1f' % tt2 + ' s', xy=(tt2, 1), xytext=((tt2 + 1), 1),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('end_warn', xy=(tt2, 1), xytext=((tt2 + 1), 2),  # 标注数据
                     color="b")
    elif 2 in bj:
        plt.annotate('time=''%.1f' % tt1 + ' s', xy=(tt1, 2), xytext=((tt1 - 2), 2),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('start_warn', xy=(tt1, 2), xytext=((tt1 - 2), 3),  # 标注数据
                     color="b")

        plt.annotate('time=''%.1f' % tt2 + ' s', xy=(tt2, 2), xytext=((tt2 + 1), 2),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('end_warn', xy=(tt2, 2), xytext=((tt2 + 1), 3),  # 标注数据
                     color="b")
    # 报警阶段标注

    #plt.show()

    #图片导入报告
    name3= zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name3+'.jpg',bbox_inches='tight')
    result="测试车最大车速为：%0.1f" % max(z1)+ ' km/h' + "，测试车最小车速为：%0.1f" % min(z1)+ ' km/h'\
    "，测试车平均车速为：%0.1f" % vp2+ ' km/h \n' + "配合车最大车速为：%0.1f" % max(z2)+ ' km/h' \
    ",配合车最小车速为：%0.1f" % min(z2)+ ' km/h' + ",配合车平均车速为：%0.1f" % vp1+ ' km/h \n'    \
    "两车最大横向距离为：%0.1f" % xd1 + ' m' + ",两车最小横向距离为：%0.1f" % xd2+ ' m '   \
    ",两车平均横向距离为：%0.1f" % xp1 + ' m \n' + "两车最大纵向距离为：%0.1f" % yd1 + ' m' \
    ",两车最小纵向距离为：%0.1f" % yd2 + ' m' + ",两车平均纵向距离为：%0.1f" % xp2 + ' m \n' \
    +pps
    jsss=max(ww1) - min(ww1)
    ms="报警开始时刻为：%0.1f" % min(ww1)+' s'+"，报警结束时刻为：%0.1f" % max(ww1)+' s' \
    "，报警持续时间为：%0.1f" % jsss + ' s'
    result2= qqc + "\n" + pr + "\n" \
    + ms+ "\n" + mark
    global mysql_status
    mysql_status = APP.word_docx(name2 + '.jpg',result,
                      name + '.jpg'
                      ,name3 + '.jpg'
                      ,result2)


def BSD_xingneng(ttrs):
    APP = ReadLcmAll()  # 实例化
    lcmlog_dataframe=APP.get_lcm_dataset(
        ttrs)
    lookup = APP.lookup_data()
    # print(APP.gps_info_dict)
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']

    channel_starting_time, timestamp, packets = unpack_packets(lcmlog_dataframe, "abLcaDebug")
    bsd = lca_debug_pb2.LCADebug()
    r = []
    l = []
    ddd = []
    ztj = []
    reason=[]
    turnsignals=[]
    for i, packet in enumerate(packets):
        bsd.ParseFromString(packet)
        #print(bsd.debug_analy_chassis.turnsignal)
        xxx = (bsd.debug_analy_obstacles.obstacle_info)
        r.append(bsd.bsd_warn_right)
        l.append(bsd.bsd_warn_left)
        turnsignals.append(bsd.debug_analy_chassis.turnsignal)
        ddd.append(xxx)
        ztj.append(bsd.bsd_state_machine)
        reason.append(bsd.bsd_inhibit_reason)
    # print(turnsignals)
    # print(reason)
    # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    velocitys = []
    longitudes = []
    latitudes = []
    channel_starting_time1, timestamp1, packets1 = unpack_packets(lcmlog_dataframe, "abL10n")
    gps = gps_imu_info_pb2.gpsImu()
    for i, packet in enumerate(packets1):
        gps.ParseFromString(packet)
        velocitys.append(gps.velocity * 3.6)
        longitudes.append(gps.longitude)
        latitudes.append(gps.latitude)

    z1 = []
    z2 = []
    Tutime = []
    Ttimestamp = []
    yjl = []
    xjl = []
    zbj = []
    ybj = []
    ztj1 = []
    Tturnsignal=[]
    for a, b, c, w, h, y, n, m, o,p in zip(velocitys, wey4_velocity, UTM_X, timestamp1, utime, UTM_Y, l, r, ztj,turnsignals):
        w1 = round(w, 2)
        h1 = round(h, 2)
        if h1 == w1:
            Tutime.append(h)
            Ttimestamp.append(w)
            z1.append(a)
            z2.append(b)
            yjl.append(y)
            xjl.append(c)
            zbj.append(n)
            ybj.append(m)
            ztj1.append(o)
            Tturnsignal.append(p)
    for a,b,c,d,e in zip(z2,z1,Tutime,xjl,yjl):
        if a == max(z2):
            pv1=a
            pv1t=c
        elif a == min(z2):
            pv2=a
            pv2t=c
        if b == max(z1):
            mv1=b
            mv1t=c
        elif b == min(z1):
            mv2=b
            mv2t=c
        if d == max(xjl):
            xd1=d
            xd1t=c
        elif d == min(xjl):
            xd2=d
            xd2t=c
        if e == max(yjl):
            yd1=e
            yd1t=c
        elif e == min(yjl):
            yd2=e
            yd2t=c




    gv1=max(z2)    #
    gv2=min(z2)

    total=sum(z2)       #平均速度
    vp1=total / len(z2)    #配合车平均速度
    total1=sum(z1)
    vp2=total1 / len(z1)   #测试车平均速度

    totalx=sum(xjl)
    xp1=totalx / len(xjl) #配合车平均X
    totaly=sum(yjl)
    xp2=totaly / len(yjl)  #配合车平均Y



    bj = []
    if xjl[0]<0:
        bj=zbj
    elif xjl[0]>0 :
        bj=ybj



    xx1 = [a - b for a, b in zip(z2, z1)]

    tt = []
    bnm = []
    for i in xx1:
        tt.append(i / 3.6)
    for i in yjl:
        bnm.append(i - 4.5)
    xx2 = [e / f for e, f in zip(bnm, tt)]  # 利用该语句实现
    xx3 = []
    for a in xx2:
        xx3.append(abs(a))

    ww1 = []
    xwz = []
    ywz = []
    zsd = []
    ttcc = []
    ts=[]
    for a, b, c, d, e, f in zip(bj, Tutime, xjl, yjl, z2, xx3):
        if a == 1 or a == 2:
            ts.append(a)
            ww1.append(b)
            xwz.append(c)
            ywz.append(d)
            zsd.append(e)
            ttcc.append(f)

    for a, b, c, d, e in zip(xwz, ywz, ww1, zsd, ttcc):
        if a == xwz[len(xwz) // 2]:
            xzd = a
            yzd = b
            tt3 = c
            vv3 = d
            ttc3 = e

    for a, b, c, d in zip(Tutime, xjl, yjl, z2):
        if a == min(ww1):
            ww2 = b
            ww3 = c
            tt1 = min(ww1)
            vv1 = d
            ttc1 = e
        elif a == max(ww1):
            tt2 = max(ww1)
            ww4 = b
            ww5 = c
            vv2 = d
            ttc2 = e
        elif a == 0:
            tt4 = a
            ww6 = b
            ww7 = c
            vv4 = d
            ttc4 = e
        elif a == Tutime[-1]:
            tt5 = a
            ww8 = b
            ww9 = c
            vv5 = d
            ttc5 = e
    bjjd=[]
    bjjdt=[]
    for a,b in zip (bj,Tutime):
        if min(ww1) <= b <= max(ww1):
            bjjd.append(a)
            bjjdt.append(b)
    print(bjjd)
    mm1=[]
    mm2=[]
    for a in bjjd:
        if a == 1:
            mm1.append(a)
            if len(mm1) == len(bjjd):
                qqc = "本次测试的报警方式为一阶段报警。"
            elif bjjd[0]>bjjd[-1]:
                qqc = "本次测试的报警方式为二阶段跳一阶段报警。"
            elif bjjd[0]<bjjd[-1]:
                qqc = "本次测试的报警方式为一阶段跳二阶段报警。"

        elif a == 2:
            mm2.append(a)
            if len(mm2) == len(bjjd):
                qqc = "本次测试的报警方式为二阶段报警。"

    # if all(el==1 for el in bjjd):
    #     print('11111111111111')
    #     qqc="本次测试为一阶段报警"
    #     print("纯一阶段报警")
    # elif all(el==2 for el in bjjd):
    #     qqc = "本次测试为二阶段报警"
    #     print("纯二阶段报警")
    # else:
    #     if bjjd[0] >  bjjd[-1]:
    #         qqc = "本次测试为二阶段跳一阶段报警"
    #         print("二阶段跳一阶段")
    #     else:
    #         qqc = "本次测试为一阶段跳二阶段报警"
    #         print("一阶段跳二阶段")

    for a,b in zip (bjjd,bjjdt):
        if a == 0 :
            cw = a
            cwt=b
            mark="如上图红叉标注位置，在报警区间，出现报警信号中断，不符合场景，所以不通过"
            break
        else:
            cwt=None
            cw=None
            mark=""
    # 车速匹配
    sp=APP.case_info_dict['key']
    if sp[2] - 0.3 * sp[2] <= vp2 <= sp[2] + 0.3 * sp[2] :
        print('被测车速度匹配正常')
        if sp[7] - 0.3 * sp[7] <= vp1 <= sp[7] + 0.3 * sp[7]:
            print('配合车速度匹配正常')
            pps="本次测试被测车平均车速为：%0.1f" % vp2 +'km/h'+ ",测试用例场景所需车速为：%0.1f" % sp[2]+'km/h \n' \
            "本次测试配合车平均车速为：%0.1f" % vp1+'km/h' + ",测试用例场景所需车速为：%0.1f" % sp[7]+'km/h \n' \
            '通过分析，两车速度均在测试用例允许误差范围内，速度匹配正常。'

        else:
            print('配合车速度匹配失败')
            pps="本次测试被测车平均车速为：%0.1f" % vp2 +'km/h'+ ",测试用例场景所需车速为：%0.1f" % sp[2]+'km/h \n' \
            "本次测试配合车平均车速为：%0.1f" % vp1+'km/h' + ",测试用例场景所需车速为：%0.1f" % sp[7]+'km/h \n' \
            '通过分析，两车速度不在测试用例允许误差范围内，速度匹配失败。'

    else:
        print('被测车速度匹配失败')






    cd=[]
    cd2=[]
    warn_x = [ww2, xzd, ww4]
    warn_y = [ww3, yzd, ww5]

    if yjl[0] > 0:
        AtoB="自车超车"
        for a, b in zip(warn_x, warn_y):

            if a < 0:
                fx="左侧"
                if -3 <= a + 0.9 <= -0.5 and -6 <= b + 3.7 <= 1.315:
                    cd.append(a)
                    if len(cd) == len(warn_x):
                        pr="在报警时刻，配合车全部位于该报警的区域，所以该用例通过"
                    else:
                        pr = "在报警时刻，存在配合车位于非报警的区域，所以该用例不通过"
                    print('左侧测试通过')
                else:
                    print('左侧测试失败')
            elif a > 0:
                fx = "右侧"
                if 0.5 <= a - 0.9 <= 3 and -6 <= b + 3.7 <= 1.315:
                    cd2.append(a)
                    if len(cd2) == len(warn_x):
                        pr = "在报警时刻，配合车全部位于该报警的区域，符合规范要求，该用例通过。"
                    else:
                        pr = "在报警时刻，存在配合车位于非报警的区域，不符合规范要求，该用例不通过。"
                    print('右侧测试通过')
                else:
                    print('右侧测试失败')
            else:
                print('测试失败')
    elif yjl[0] < 0:
        AtoB="目标车超车"
        for a, b in zip(warn_x, warn_y):

            if a < 0:
                if -3 <= a + 0.9 <= -0.5 and -9.7 <= b <= 2.215:
                    cd.append(a)
                    if len(cd) == len(warn_x):
                        pr = "在报警时刻，配合车全部位于该报警的区域，所以该用例通过"
                    else:
                        pr = "在报警时刻，存在配合车位于非报警的区域，所以该用例不通过"
                    print('左侧测试通过')
                else:
                    print('左侧测试失败')

            elif a > 0:
                if 0.5 <= a - 0.9 <= 3 and -9.7 <= b <= 2.215:
                    cd2.append(a)

                    if len(cd2) == len(warn_x):
                        pr = "在报警时刻，配合车全部位于该报警的区域，符合规范要求，该用例通过。"
                    else:
                        pr = "在报警时刻，存在配合车位于非报警的区域，不符合规范要求，该用例不通过。"
                    print('右侧测试通过')
                else:
                    print('右侧测试失败')
            else:
                print('测试失败')


    # ----------------------1.创建画布并引入axisartist工具------------------
    fig = plt.figure(figsize=(18, 12))  # 创建画布
    # 使用axisartist.Subplot方法创建一个绘图区对象ax
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中

    # ----------2. 绘制带箭头的x-y坐标轴#通过set_visible方法设置绘图区所有坐标轴隐藏-------
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    # ax.new_floating_axis代表添加新的坐标轴
    ax.axis["x"] = ax.new_floating_axis(0, 0)
    ax.axis["x"].set_axisline_style("->", size=1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1, 0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size=1.0)
    # 设置x、y轴上刻度显示方向
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")

    # -----------3. 在带箭头的x-y坐标轴背景下，绘制函数图像#生成x步长为0.1的列表数据----------
    x = np.arange(-15, 15, 0.1)
    y = 1 / (1 + np.exp(-x))  # 生成sigmiod形式的y数据
    # 设置x、y坐标轴的范围
    plt.ylim(-40, 40)
    plt.xlim(-40, 40)
    plt.axvline(x=-1.875, ls='--' ,c='k')      #车道线
    plt.axvline(x=-5.625, ls='--' ,c='k')
    plt.axvline(x=1.875, ls='--' ,c='k')
    plt.axvline(x=5.625, ls='--' ,c='k')
    #plt.axhline(y=10, ls='--', c='blue') # 添加水平线    平行于x轴
    # 左报警区间
    plt.plot([-1.4, -3.9, -1.4, -1.4, -1.4, -3.9, -3.9, -3.9], [1.315, 1.315, 1.315, -6, -6, -6, 1.315, -6], 'r:')
    # 右报警区间
    plt.plot([1.4, 3.9, 1.4, 1.4, 1.4, 3.9, 3.9, 3.9], [1.315, 1.315, 1.315, -6, -6, -6, 1.315, -6], 'r:')

    plt.plot(ww6, ww7, ".")  # 时间开始时刻（t=0）
    plt.plot([ww6 - 0.9, ww6 + 0.9, ww6 - 0.9, ww6 - 0.9, ww6 - 0.9, ww6 + 0.9, ww6 + 0.9, ww6 + 0.9],
             [ww7 - 0.9, ww7 - 0.9, ww7 - 0.9, ww7 + 3.7, ww7 + 3.7, ww7 + 3.7, ww7 + 3.7, ww7 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt4 + ' s', xy=(ww6, ww7), xytext=((ww6 - 10), ww7),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv4 + ' km/h', xy=(ww6, ww7), xytext=((ww6 - 10), (ww7 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc4 + ' s', xy=(ww6, ww7), xytext=((ww6 - 10), (ww7 + 2)),
    #              color="b")

    plt.plot(ww8, ww9, ".")  # 时间结束时刻（t=最后一秒）
    plt.plot([ww8 - 0.9, ww8 + 0.9, ww8 - 0.9, ww8 - 0.9, ww8 - 0.9, ww8 + 0.9, ww8 + 0.9, ww8 + 0.9],
             [ww9 - 0.9, ww9 - 0.9, ww9 - 0.9, ww9 + 3.7, ww9 + 3.7, ww9 + 3.7, ww9 + 3.7, ww9 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt5 + ' s', xy=(ww8, ww9), xytext=((ww8 - 10), ww9),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv5 + ' km/h', xy=(ww8, ww9), xytext=((ww8 - 10), (ww9 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc5 + ' s', xy=(ww8, ww9), xytext=((ww8 - 10), (ww9 + 2)),
    #              color="b")

    plt.plot(ww2, ww3, ".")  # 开始报警时刻
    plt.plot([ww2 - 0.9, ww2 + 0.9, ww2 - 0.9, ww2 - 0.9, ww2 - 0.9, ww2 + 0.9, ww2 + 0.9, ww2 + 0.9],
             [ww3 - 0.9, ww3 - 0.9, ww3 - 0.9, ww3 + 3.7, ww3 + 3.7, ww3 + 3.7, ww3 + 3.7, ww3 - 0.9], 'green')
    # plt.plot([ww2-0.9,ww2+0.9],[ww3-0.9,ww3-0.9])      #最下面的一行
    # plt.plot([ww2-0.9,ww2-0.9],[ww3-0.9,ww3+3.7])    #左
    # plt.plot([ww2-0.9,ww2+0.9],[ww3+3.7,ww3+3.7])    #上
    # plt.plot([ww2+0.9,ww2+0.9],[ww3+3.7,ww3-0.9])      #右
    plt.annotate('time=''%.1f' % tt1 + ' s', xy=(ww2, ww3), xytext=((ww2 - 10), ww3),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv1 + ' km/h', xy=(ww2, ww3), xytext=((ww2 - 10), (ww3 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc1 + ' s', xy=(ww2, ww3), xytext=((ww2 - 10), (ww3 + 2)),
    #              color="b")

    plt.plot(ww4, ww5, "b.")  # 报警结束时刻
    plt.plot([ww4 - 0.9, ww4 + 0.9, ww4 - 0.9, ww4 - 0.9, ww4 - 0.9, ww4 + 0.9, ww4 + 0.9, ww4 + 0.9],
             [ww5 - 0.9, ww5 - 0.9, ww5 - 0.9, ww5 + 3.7, ww5 + 3.7, ww5 + 3.7, ww5 + 3.7, ww5 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt2 + ' s', xy=(ww4, ww5), xytext=((ww4 - 10), ww5),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv2 + ' km/h', xy=(ww4, ww5), xytext=((ww4 - 10), (ww5 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc2 + ' s', xy=(ww4, ww5), xytext=((ww4 - 10), (ww5 + 2)),
    #              color="b")

    plt.plot(xzd, yzd, "b.")  # 报警中间时刻
    plt.plot([xzd - 0.9, xzd + 0.9, xzd - 0.9, xzd - 0.9, xzd - 0.9, xzd + 0.9, xzd + 0.9, xzd + 0.9],
             [yzd - 0.9, yzd - 0.9, yzd - 0.9, yzd + 3.7, yzd + 3.7, yzd + 3.7, yzd + 3.7, yzd - 0.9], 'green')
    plt.annotate('time=''%.1f' % tt3 + ' s', xy=(xzd, yzd), xytext=((xzd - 10), yzd),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv3 + ' km/h', xy=(xzd, yzd), xytext=((xzd - 10), (yzd + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc3 + ' s', xy=(xzd, yzd), xytext=((xzd - 10), (yzd + 2)),
    #              color="b")

    plt.plot(0, 0, "r.")
    plt.plot([-0.9, 0.9, -0.9, -0.9, -0.9, 0.9, 0.9, 0.9], [-1, -1, -1, 3.6, 3.6, 3.6, -1, 3.6], 'purple')  # 被测车坐标位置

    plt.legend(loc=0)
    # plt.show()
    name = zdhq + APP.lcmlog_dict['filename'] + 'p1'
    plt.savefig(name + '.jpg', bbox_inches='tight')


    x = np.linspace(0, 2, 200)
    # fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(4, 1, 1)
    # linestyle=":"
    plt.plot(Tutime, z1, label='VUT_V')
    plt.plot(Tutime, z2, label="GVT_V")

    plt.annotate('GVT_V(max)=''%.1f' % pv1 + ' km/h', xy=(pv1t,pv1 ), xytext=((pv1t - 2), pv1+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('GVT_V(min)=''%.1f' % pv2 + ' km/h', xy=(pv2t,pv2 ), xytext=((pv2t - 2), pv2+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('GVT_V(average)=''%.1f' % vp1 + ' km/h', xy=(Tutime[len(Tutime)//2],vp1 ), xytext=(Tutime[len(Tutime)//2], vp1-1),  # 标注数据
                 color="b")

    plt.annotate('VUT_V(max)=''%.1f' % mv1 + ' km/h', xy=(mv1t,mv1 ), xytext=((mv1t - 2), mv1+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('VUT_V(min)=''%.1f' % mv2 + ' km/h', xy=(mv2t,mv2 ), xytext=((mv2t - 2), mv2+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('VUT_V(average)=''%.1f' % vp2 + ' km/h', xy=(Tutime[len(Tutime)//2],vp2 ), xytext=(Tutime[len(Tutime)//2], vp2+1),  # 标注数据
                 color="b")


    plt.xlabel('time    (s)')
    plt.ylabel('  (km/h)')
    # plt.plot(utime,xx3,label="ttc")
    plt.legend(loc=0)

    plt.subplot(4, 1, 2)  # Add a subplot to the current figure
    # plt.plot(ccc, aaa, ".",color='pink', label='position_x')  # 绘制第一个子图
    plt.plot(Tutime, xjl, label="real_X")
    # plt.plot(Tutime, yjl, label="real_Y")

    plt.annotate('real_X(max)=''%.1f' % xd1 + ' m', xy=(xd1t,xd1 ), xytext=((xd1t - 2), xd1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_X(min)=''%.1f' % xd2 + ' m', xy=(xd2t,xd2 ), xytext=((xd2t - 4), xd2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_X(average)=''%.1f' % xp1 + ' m', xy=(Tutime[len(Tutime)//2],xp1 ), xytext=(Tutime[len(Tutime)//2], xp1),  # 标注数据
                 color="b")



    plt.suptitle('BSD', fontsize=20)
    plt.legend(loc=0)
    plt.xlabel('time    (s)')
    plt.ylabel('  (m)')

    plt.subplot(4, 1, 3)
    # plt.plot(ccc, zzz,'.', color='green', label='y.distance')  # 绘制第三个子图
    # plt.plot(Tutime, xx3, label="ttc")
    plt.plot(Tutime, yjl, label="real_Y")
    plt.annotate('real_Y(max)=''%.1f' % yd1 + ' m', xy=(yd1t,yd1 ), xytext=((yd1t - 2), yd1+2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_Y(min)=''%.1f' % yd2 + ' m', xy=(yd2t,yd2 ), xytext=((yd2t - 2), yd2+2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_Y(average)=''%.1f' % xp2 + ' m', xy=(Tutime[len(Tutime)//2] ,xp2 ), xytext=(Tutime[len(Tutime)//2  ], xp2),  # 标注数据
                 color="b")

    plt.legend(loc=0)
    plt.xlabel('time    (s)')
    plt.ylabel(' (m)')
    # plt.subplots_adjust(hspace=0.6)

    name2= zdhq + APP.lcmlog_dict['filename'] + 'p2'
    plt.savefig(name2+'.jpg',bbox_inches='tight')


    plt.figure(figsize=(18, 12))
    plt.subplot(4, 1, 4)
    plt.plot(Tutime, ybj, color='red', label='warn_right')  # 绘制第四个子图
    plt.plot(Tutime, zbj, label='warn_left')
    if cwt != None:
        plt.plot(cwt,cw,'x',markersize=12,c='r')
    else:
        pass
    plt.plot(Tutime, ztj1, label='state_machine')
    plt.plot(Tutime, Tturnsignal, label='turnsignal')
    plt.legend(loc=0)
    # plt.ylabel('level')
    plt.xlabel('time    (s)')
    # plt.plot(aaa,color="red",linestyle="-",label='tuli')

    # 报警阶段标注
    if 1 in bj:
        plt.annotate('time=''%.1f' % tt1 + ' s', xy=(tt1, 1), xytext=((tt1 - 2), 1),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('start_warn', xy=(tt1, 1), xytext=((tt1 - 2), 2),  # 标注数据
                     color="b")

        plt.annotate('time=''%.1f' % tt2 + ' s', xy=(tt2, 1), xytext=((tt2 + 1), 1),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('end_warn', xy=(tt2, 1), xytext=((tt2 + 1), 2),  # 标注数据
                     color="b")
    elif 2 in bj:
        plt.annotate('time=''%.1f' % tt1 + ' s', xy=(tt1, 2), xytext=((tt1 - 2), 2),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('start_warn', xy=(tt1, 2), xytext=((tt1 - 2), 3),  # 标注数据
                     color="b")

        plt.annotate('time=''%.1f' % tt2 + ' s', xy=(tt2, 2), xytext=((tt2 + 1), 2),  # 标注数据
                     color="b",
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        plt.annotate('end_warn', xy=(tt2, 2), xytext=((tt2 + 1), 3),  # 标注数据
                     color="b")
    # 报警阶段标注

    #plt.show()

    #图片导入报告
    name3= zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name3+'.jpg',bbox_inches='tight')
    result="测试车最大车速为：%0.1f" % max(z1)+ ' km/h' + "，测试车最小车速为：%0.1f" % min(z1)+ ' km/h'\
    "，测试车平均车速为：%0.1f" % vp2+ ' km/h \n' + "配合车最大车速为：%0.1f" % max(z2)+ ' km/h' \
    ",配合车最小车速为：%0.1f" % min(z2)+ ' km/h' + ",配合车平均车速为：%0.1f" % vp1+ ' km/h \n'    \
    "两车最大横向距离为：%0.1f" % xd1 + ' m' + ",两车最小横向距离为：%0.1f" % xd2+ ' m '   \
    ",两车平均横向距离为：%0.1f" % xp1 + ' m \n' + "两车最大纵向距离为：%0.1f" % yd1 + ' m' \
    ",两车最小纵向距离为：%0.1f" % yd2 + ' m' + ",两车平均纵向距离为：%0.1f" % xp2 + ' m \n' \
    +pps
    jsss = max(ww1) - min(ww1)
    ms = "报警开始时刻为：%0.1f" % min(ww1) + ' s' + "，报警结束时刻为：%0.1f" % max(ww1) + ' s' \
    "，报警持续时间为：%0.1f" % jsss + ' s'
    result2 = qqc + "\n" + pr + "\n" \
              + ms + "\n" + mark
    global mysql_status
    mysql_status = APP.word_docx(name2 + '.jpg',result,
                      name + '.jpg'
                      ,name3 + '.jpg'
                      ,result2)


def BSD_yizhi(ttrs):

    APP = ReadLcmAll()  # 实例化
    lcmlog_dataframe=APP.get_lcm_dataset(
        ttrs)

    lookup = APP.lookup_data()
    # print(APP.gps_info_dict)
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']

    channel_starting_time, timestamp, packets = unpack_packets(lcmlog_dataframe, "abLcaDebug")
    bsd = lca_debug_pb2.LCADebug()
    r = []
    l = []
    ddd = []
    ztj = []
    reason=[]
    turnsignals=[]
    for i, packet in enumerate(packets):
        bsd.ParseFromString(packet)
        #print(bsd.debug_analy_chassis.turnsignal)
        xxx = (bsd.debug_analy_obstacles.obstacle_info)
        r.append(bsd.bsd_warn_right)
        l.append(bsd.bsd_warn_left)
        turnsignals.append(bsd.debug_analy_chassis.turnsignal)
        ddd.append(xxx)
        ztj.append(bsd.bsd_state_machine)
        reason.append(bsd.bsd_inhibit_reason)
    velocitys = []
    longitudes = []
    latitudes = []
    # print(reason)
    # print(111111111111111)
    channel_starting_time1, timestamp1, packets1 = unpack_packets(lcmlog_dataframe, "abL10n")
    gps = gps_imu_info_pb2.gpsImu()
    for i, packet in enumerate(packets1):
        gps.ParseFromString(packet)
        velocitys.append(gps.velocity * 3.6)
        longitudes.append(gps.longitude)
        latitudes.append(gps.latitude)

    z1 = []
    z2 = []
    Tutime = []
    Ttimestamp = []
    yjl = []
    xjl = []
    zbj = []
    ybj = []
    ztj1 = []
    Tturnsignal=[]
    for a, b, c, w, h, y, n, m, o,p in zip(velocitys, wey4_velocity, UTM_X, timestamp1, utime, UTM_Y, l, r, ztj,turnsignals):
        w1 = round(w, 2)
        h1 = round(h, 2)
        if h1 == w1:
            Tutime.append(h)
            Ttimestamp.append(w)
            z1.append(a)
            z2.append(b)
            yjl.append(y)
            xjl.append(c)
            zbj.append(n)
            ybj.append(m)
            ztj1.append(o)
            Tturnsignal.append(p)

    for a,b,c,d,e in zip(z2,z1,Tutime,xjl,yjl):
        if a == max(z2):
            pv1=a
            pv1t=c
        elif a == min(z2):
            pv2=a
            pv2t=c
        if b == max(z1):
            mv1=b
            mv1t=c
        elif b == min(z1):
            mv2=b
            mv2t=c
        if d == max(xjl):
            xd1=d
            xd1t=c
        elif d == min(xjl):
            xd2=d
            xd2t=c
        if e == max(yjl):
            yd1=e
            yd1t=c
        elif e == min(yjl):
            yd2=e
            yd2t=c

    gv1=max(z2)    #
    gv2=min(z2)

    total=sum(z2)       #平均速度
    vp1=total / len(z2)    #配合车平均速度
    total1=sum(z1)
    vp2=total1 / len(z1)   #测试车平均速度

    totalx=sum(xjl)
    xp1=totalx / len(xjl) #配合车平均X
    totaly=sum(yjl)
    xp2=totaly / len(yjl)  #配合车平均Y

    bj = []
    if xjl[0]<0:
        bj=zbj
    elif xjl[0]>0 :
        bj=ybj

    xx1 = [a - b for a, b in zip(z2, z1)]

    tt = []
    bnm = []
    for i in xx1:
        tt.append(i / 3.6)
    for i in yjl:
        bnm.append(i - 4.5)
    xx2 = [e / f for e, f in zip(bnm, tt)]  # 利用该语句实现
    xx3 = []
    for a in xx2:
        xx3.append(abs(a))

    ww1 = []
    xwz = []
    ywz = []
    zsd = []
    ttcc = []
    ts=[]
    for a, b, c, d, e, f in zip(ztj1, Tutime, xjl, yjl, z2, xx3):
        if a == 3 or a == 4 or a == 6 or a == 7:
            ts.append(a)
            ww1.append(b)
            xwz.append(c)
            ywz.append(d)
            zsd.append(e)
            ttcc.append(f)

    for a, b, c, d, e in zip(xwz, ywz, ww1, zsd, ttcc):
        if a == xwz[len(xwz) // 2]:
            xzd = a
            yzd = b
            tt3 = c
            vv3 = d
            ttc3 = e

    for a, b, c, d in zip(Tutime, xjl, yjl, z2):
        if a == min(ww1):
            ww2 = b
            ww3 = c
            tt1 = min(ww1)
            vv1 = d
            ttc1 = e
        elif a == max(ww1):
            tt2 = max(ww1)
            ww4 = b
            ww5 = c
            vv2 = d
            ttc2 = e
        elif a == 0:
            tt4 = a
            ww6 = b
            ww7 = c
            vv4 = d
            ttc4 = e
        elif a == Tutime[-1]:
            tt5 = a
            ww8 = b
            ww9 = c
            vv5 = d
            ttc5 = e

    sp=APP.case_info_dict['key']
    if sp[2] - 0.3 * sp[2] <= vp2 <= sp[2] + 0.3 * sp[2] :
        print('被测车速度匹配正常')
        if sp[7] - 0.3 * sp[7] <= vp1 <= sp[7] + 0.3 * sp[7]:
            print('配合车速度匹配正常')
            pps="本次测试被测车平均车速为：%0.1f" % vp2 +'km/h'+ ",测试用例场景所需车速为：%0.1f" % sp[2]+'km/h \n' \
            "本次测试配合车平均车速为：%0.1f" % vp1+'km/h' + ",测试用例场景所需车速为：%0.1f" % sp[7]+'km/h \n' \
            '通过分析，两车速度均在测试用例允许误差范围内，速度匹配正常。'

        else:
            print('配合车速度匹配失败')
            pps="本次测试被测车平均车速为：%0.1f" % vp2 +'km/h'+ ",测试用例场景所需车速为：%0.1f" % sp[2]+'km/h \n' \
            "本次测试配合车平均车速为：%0.1f" % vp1+'km/h' + ",测试用例场景所需车速为：%0.1f" % sp[7]+'km/h \n' \
            '通过分析，两车速度不在测试用例允许误差范围内，速度匹配失败。'

    else:
        print('被测车速度匹配失败')
    # print(pps)

    reason0=[]
    reason1=[]
    reason2=[]
    for n in bj:
        if n != 0 in bj:
            for a in reason:
                if a == 0:
                    reason0.append(a)
                    if len(reason0) == len(reason):
                        src = "本次测试场景为抑制测试，但是系统未出现抑制，所以测试不通过。"

                elif a == 2:
                    reason2.append(a)
                    if len(reason) == len(reason2):
                        src = '本次测试时间内抑制通道全部发出速度抑制信号，但是却有报警信号发出，二者相悖，不符合测试场景，测试不通过。'

                elif a == 1:
                    reason1.append(a)
                    if len(reason1) == len(reason):
                        src = '本次测试时间内抑制通道全部发出档位抑制信号，但是却有报警信号发出，二者相悖，不符合测试场景，测试不通过。'
                elif a == 1 and a == 2 in reason:
                    src = "本次测试抑制原因不唯一，测试失败。"

                elif a ==1 and a ==2 and a == 0 in reason:
                    src = "本次测试状态间激活转抑制抑制原因不唯一，测试失败。"
                elif a == 0 and a == 2 in reason:
                    src ='本次测试为系统由激活状态转为抑制状态，抑制原因为速度抑制，符合场景，测试通过'
                elif a == 0 and a == 1 in reason:
                    src ='本次测试为系统由激活状态转为抑制状态，抑制原因为档位抑制，符合场景，测试通过'

        else:
            for a in reason:
                if a == 0:
                    reason0.append(a)
                    if len(reason0) == len(reason):
                        src = "本次测试场景为抑制测试，但是系统未出现抑制，所以测试不通过。"
                    else:
                        src = "在抑制测试场景中，出现系统不抑制的情况，测试不通过。"
                elif a == 2:
                    reason2.append(a)
                    if len(reason) == len(reason2):
                        if vp2 == sp[2] == 0:
                            src = "本次测试场景为速度抑制，测试时被测车平均速度为：%0.1f" % vp2 + 'km/h' \
                                  + ",测试用例场景所需车速为：%0.1f" % sp[2] + 'km/h \n' \
                                                                   '通过分析符合本次抑制测试，测试通过。'
                        elif vp2 > 130 or vp2 < 12 :
                            src ='本次测试场景为速度抑制，测试时被测车的速度为：%0.1f' % vp2 + 'km/h' \
                                 + ',符合车速大于130km/h或小于12km/h的抑制条件 \n'\
                                ',通过分析符合本次抑制测试，测试通过。'
                        elif abs(vp2 - vp1) > 15:
                            if yjl[0] > 0:
                                src = '本次被测车车速为：%0.1f'% vp2 + 'km/h' \
                                + '，本次配合车车速为：%0.1f'% vp1 + 'km/h' \
                                +'，两车速度差为：%0.1f'% abs(vp2 - vp1) + 'km/h' \
                                '，且场景为自车超车，测试场景符合抑制条件，测试通过。'

                        else:
                            src = "本次测试场景为速度抑制，测试时被测车平均速度为：%0.1f" % vp2 + 'km/h' \
                                  + ",测试用例场景所需车速为：%0.1f" % sp[2] + 'km/h \n' \
                                        '通过分析不符合本次抑制测试，测试不通过。'

                elif a == 1:
                    reason1.append(a)
                    if len(reason1) == len(reason):
                        src = '本次测试场景为档位抑制，测试通过。'
                elif a == 1 and a == 2 in reason:
                    src = "本次测试抑制原因不唯一，测试失败。"







    # reason0=[]
    # reason1=[]
    # reason2=[]
    # for a in reason:
    #     if a == 0:
    #         reason0.append(a)
    #         if len(reason0) == len(reason):
    #             src = "本次测试场景为抑制测试，但是系统未出现抑制，所以测试不通过。"
    #         else:
    #             src = "在抑制测试场景中，出现系统不抑制的情况，测试不通过。"
    #     elif a == 2:
    #         reason2.append(a)
    #         if len(reason) == len(reason2):
    #             if vp2 == sp[2] == 0:
    #                 src = "本次测试场景为速度抑制，测试时被测车平均速度为：%0.1f" % vp2 + 'km/h' \
    #                       + ",测试用例场景所需车速为：%0.1f" % sp[2] + 'km/h \n' \
    #                         '通过分析符合本次抑制测试，测试通过。'
    #             else:
    #                 src = "本次测试场景为速度抑制，测试时被测车平均速度为：%0.1f" % vp2 + 'km/h' \
    #                       + ",测试用例场景所需车速为：%0.1f" % sp[2] + 'km/h \n' \
    #                         '通过分析不符合本次抑制测试，测试不通过。'
    #
    #     elif a == 1:
    #         reason1.append(a)
    #         if len(reason1) == len(reason):
    #             src='本次测试场景为档位抑制，测试通过。'
    #     elif a == 1 and a == 2 in reason:
    #         src="本次测试抑制原因不唯一，测试失败。"

    # print(src)

    # ----------------------1.创建画布并引入axisartist工具------------------
    fig = plt.figure(figsize=(18, 12))  # 创建画布
    # 使用axisartist.Subplot方法创建一个绘图区对象ax
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中

    # ----------2. 绘制带箭头的x-y坐标轴#通过set_visible方法设置绘图区所有坐标轴隐藏-------
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    # ax.new_floating_axis代表添加新的坐标轴
    ax.axis["x"] = ax.new_floating_axis(0, 0)
    ax.axis["x"].set_axisline_style("->", size=1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1, 0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size=1.0)
    # 设置x、y轴上刻度显示方向
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")

    # -----------3. 在带箭头的x-y坐标轴背景下，绘制函数图像#生成x步长为0.1的列表数据----------
    x = np.arange(-15, 15, 0.1)
    y = 1 / (1 + np.exp(-x))  # 生成sigmiod形式的y数据
    # 设置x、y坐标轴的范围
    plt.ylim(-60, 60)
    plt.xlim(-60, 60)
    plt.axvline(x=-1.875, ls='--' ,c='k')      #车道线
    plt.axvline(x=-5.625, ls='--' ,c='k')
    plt.axvline(x=1.875, ls='--' ,c='k')
    plt.axvline(x=5.625, ls='--' ,c='k')
    #plt.axhline(y=10, ls='--', c='blue') # 添加水平线    平行于x轴
    # 左报警区间
    plt.plot([-1.4, -3.9, -1.4, -1.4, -1.4, -3.9, -3.9, -3.9], [1.315, 1.315, 1.315, -6, -6, -6, 1.315, -6], 'r:')
    # 右报警区间
    plt.plot([1.4, 3.9, 1.4, 1.4, 1.4, 3.9, 3.9, 3.9], [1.315, 1.315, 1.315, -6, -6, -6, 1.315, -6], 'r:')

    # plt.plot(ww6, ww7, ".")  # 时间开始时刻（t=0）
    # plt.plot([ww6 - 0.9, ww6 + 0.9, ww6 - 0.9, ww6 - 0.9, ww6 - 0.9, ww6 + 0.9, ww6 + 0.9, ww6 + 0.9],
    #          [ww7 - 0.9, ww7 - 0.9, ww7 - 0.9, ww7 + 3.7, ww7 + 3.7, ww7 + 3.7, ww7 + 3.7, ww7 - 0.9], 'green')
    #
    # plt.annotate('time=''%.1f' % tt4 + ' s', xy=(ww6, ww7), xytext=((ww6 - 10), ww7),  # 标注数据
    #              color="b",
    #              arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate('velocity=''%.1f' % vv4 + ' km/h', xy=(ww6, ww7), xytext=((ww6 - 10), (ww7 + 1)),
    #              color="b")


    # plt.plot(ww8, ww9, ".")  # 时间结束时刻（t=最后一秒）
    # plt.plot([ww8 - 0.9, ww8 + 0.9, ww8 - 0.9, ww8 - 0.9, ww8 - 0.9, ww8 + 0.9, ww8 + 0.9, ww8 + 0.9],
    #          [ww9 - 0.9, ww9 - 0.9, ww9 - 0.9, ww9 + 3.7, ww9 + 3.7, ww9 + 3.7, ww9 + 3.7, ww9 - 0.9], 'green')
    #
    # plt.annotate('time=''%.1f' % tt5 + ' s', xy=(ww8, ww9), xytext=((ww8 - 10), ww9),  # 标注数据
    #              color="b",
    #              arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate('velocity=''%.1f' % vv5 + ' km/h', xy=(ww8, ww9), xytext=((ww8 - 10), (ww9 + 1)),
    #              color="b")


    plt.plot(ww2, ww3, ".")  # 开始报警时刻
    plt.plot([ww2 - 0.9, ww2 + 0.9, ww2 - 0.9, ww2 - 0.9, ww2 - 0.9, ww2 + 0.9, ww2 + 0.9, ww2 + 0.9],
             [ww3 - 0.9, ww3 - 0.9, ww3 - 0.9, ww3 + 3.7, ww3 + 3.7, ww3 + 3.7, ww3 + 3.7, ww3 - 0.9], 'green')
    # plt.plot([ww2-0.9,ww2+0.9],[ww3-0.9,ww3-0.9])      #最下面的一行
    # plt.plot([ww2-0.9,ww2-0.9],[ww3-0.9,ww3+3.7])    #左
    # plt.plot([ww2-0.9,ww2+0.9],[ww3+3.7,ww3+3.7])    #上
    # plt.plot([ww2+0.9,ww2+0.9],[ww3+3.7,ww3-0.9])      #右
    plt.annotate('time=''%.1f' % tt1 + ' s', xy=(ww2, ww3), xytext=((ww2 - 10), ww3),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv1 + ' km/h', xy=(ww2, ww3), xytext=((ww2 - 10), (ww3 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc1 + ' s', xy=(ww2, ww3), xytext=((ww2 - 10), (ww3 + 2)),
    #              color="b")

    plt.plot(ww4, ww5, "b.")  # 报警结束时刻
    plt.plot([ww4 - 0.9, ww4 + 0.9, ww4 - 0.9, ww4 - 0.9, ww4 - 0.9, ww4 + 0.9, ww4 + 0.9, ww4 + 0.9],
             [ww5 - 0.9, ww5 - 0.9, ww5 - 0.9, ww5 + 3.7, ww5 + 3.7, ww5 + 3.7, ww5 + 3.7, ww5 - 0.9], 'green')

    plt.annotate('time=''%.1f' % tt2 + ' s', xy=(ww4, ww5), xytext=((ww4 - 10), ww5),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv2 + ' km/h', xy=(ww4, ww5), xytext=((ww4 - 10), (ww5 + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc2 + ' s', xy=(ww4, ww5), xytext=((ww4 - 10), (ww5 + 2)),
    #              color="b")

    plt.plot(xzd, yzd, "b.")  # 报警中间时刻
    plt.plot([xzd - 0.9, xzd + 0.9, xzd - 0.9, xzd - 0.9, xzd - 0.9, xzd + 0.9, xzd + 0.9, xzd + 0.9],
             [yzd - 0.9, yzd - 0.9, yzd - 0.9, yzd + 3.7, yzd + 3.7, yzd + 3.7, yzd + 3.7, yzd - 0.9], 'green')
    plt.annotate('time=''%.1f' % tt3 + ' s', xy=(xzd, yzd), xytext=((xzd - 10), yzd),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('velocity=''%.1f' % vv3 + ' km/h', xy=(xzd, yzd), xytext=((xzd - 10), (yzd + 1)),
                 color="b")
    # plt.annotate('ttc=''%.1f' % ttc3 + ' s', xy=(xzd, yzd), xytext=((xzd - 10), (yzd + 2)),
    #              color="b")

    plt.plot(0, 0, "r.")
    plt.plot([-0.9, 0.9, -0.9, -0.9, -0.9, 0.9, 0.9, 0.9], [-1, -1, -1, 3.6, 3.6, 3.6, -1, 3.6], 'purple')  # 被测车坐标位置

    plt.legend(loc=0)
    #plt.show()
    name = zdhq + APP.lcmlog_dict['filename'] + 'p1'
    plt.savefig(name + '.jpg', bbox_inches='tight')

    x = np.linspace(0, 2, 200)
    # fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(4, 1, 1)
    # linestyle=":"
    plt.plot(Tutime, z1, label='VUT_V')
    plt.plot(Tutime, z2, label="GVT_V")

    plt.annotate('GVT_V(max)=''%.1f' % pv1 + ' km/h', xy=(pv1t,pv1 ), xytext=((pv1t - 2), pv1+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('GVT_V(min)=''%.1f' % pv2 + ' km/h', xy=(pv2t,pv2 ), xytext=((pv2t - 1), pv2+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('GVT_V(average)=''%.1f' % vp1 + ' km/h', xy=(Tutime[len(Tutime)//2],vp1 ), xytext=(Tutime[len(Tutime)//2], vp1-1),  # 标注数据
                 color="b")

    plt.annotate('VUT_V(max)=''%.1f' % mv1 + ' km/h', xy=(mv1t,mv1 ), xytext=((mv1t - 2), mv1+1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate('VUT_V(min)=''%.1f' % mv2 + ' km/h', xy=(mv2t,mv2 ), xytext=((mv2t - 2), mv2+1),  # 标注数据
    #              color="b",
    #              arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('VUT_V(average)=''%.1f' % vp2 + ' km/h', xy=(Tutime[len(Tutime)//2],vp2 ), xytext=(Tutime[len(Tutime)//2], vp2+1),  # 标注数据
                 color="b")


    plt.xlabel('time    (s)')
    plt.ylabel('  (km/h)')
    # plt.plot(utime,xx3,label="ttc")
    plt.legend(loc=0)

    plt.subplot(4, 1, 2)  # Add a subplot to the current figure
    # plt.plot(ccc, aaa, ".",color='pink', label='position_x')  # 绘制第一个子图
    plt.plot(Tutime, xjl, label="real_X")
    # plt.plot(Tutime, yjl, label="real_Y")

    plt.annotate('real_X(max)=''%.1f' % xd1 + ' m', xy=(xd1t,xd1 ), xytext=((xd1t - 1), xd1),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_X(min)=''%.1f' % xd2 + ' m', xy=(xd2t,xd2 ), xytext=((xd2t - 1), xd2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_X(average)=''%.1f' % xp1 + ' m', xy=(Tutime[len(Tutime)//2],xp1 ), xytext=(Tutime[len(Tutime)//2], xp1),  # 标注数据
                 color="b")



    plt.suptitle('BSD', fontsize=20)
    plt.legend(loc=0)
    plt.xlabel('time    (s)')
    plt.ylabel('  (m)')

    plt.subplot(4, 1, 3)
    # plt.plot(ccc, zzz,'.', color='green', label='y.distance')  # 绘制第三个子图
    # plt.plot(Tutime, xx3, label="ttc")
    plt.plot(Tutime, yjl, label="real_Y")
    plt.annotate('real_Y(max)=''%.1f' % yd1 + ' m', xy=(yd1t,yd1 ), xytext=((yd1t - 2), yd1+2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_Y(min)=''%.1f' % yd2 + ' m', xy=(yd2t,yd2 ), xytext=((yd2t - 1), yd2+2),  # 标注数据
                 color="b",
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate('real_Y(average)=''%.1f' % xp2 + ' m', xy=(Tutime[len(Tutime)//2] ,xp2 ), xytext=(Tutime[len(Tutime)//2  ], xp2),  # 标注数据
                 color="b")

    plt.legend(loc=0)
    plt.xlabel('time    (s)')
    plt.ylabel(' (m)')
    # plt.subplots_adjust(hspace=0.6)

    name2= zdhq + APP.lcmlog_dict['filename'] + 'p2'
    plt.savefig(name2+'.jpg',bbox_inches='tight')

    plt.figure(figsize=(18, 12))
    plt.subplot(4, 1, 4)
    plt.plot(Tutime, ybj, color='red', label='warn_right')  # 绘制第四个子图
    plt.plot(Tutime, zbj, label='warn_left')
    plt.plot(Tutime, ztj1, label='state_machine')
    plt.plot(Tutime, Tturnsignal, label='turnsignal')
    plt.legend(loc=0)
    # plt.ylabel('level')
    plt.xlabel('time    (s)')
    # plt.plot(aaa,color="red",linestyle="-",label='tuli')

    #plt.show()

    #图片导入报告
    name3= zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name3+'.jpg',bbox_inches='tight')
    result="测试车最大车速为：%0.1f" % max(z1)+ ' km/h' + "，测试车最小车速为：%0.1f" % min(z1)+ ' km/h'\
    "，测试车平均车速为：%0.1f" % vp2+ ' km/h \n' + "配合车最大车速为：%0.1f" % max(z2)+ ' km/h' \
    ",配合车最小车速为：%0.1f" % min(z2)+ ' km/h' + ",配合车平均车速为：%0.1f" % vp1+ ' km/h \n'    \
    "两车最大横向距离为：%0.1f" % xd1 + ' m' + ",两车最小横向距离为：%0.1f" % xd2+ ' m '   \
    ",两车平均横向距离为：%0.1f" % xp1 + ' m \n' + "两车最大纵向距离为：%0.1f" % yd1 + ' m' \
    ",两车最小纵向距离为：%0.1f" % yd2 + ' m' + ",两车平均纵向距离为：%0.1f" % xp2 + ' m \n' \
    +pps
    result2=  src


    # print(result)
    # print(result2)
    # print(APP.case_info_dict['key'] )
    global mysql_status
    mysql_status = APP.word_docx(name2 + '.jpg',result,
                      name + '.jpg'
                      ,name3 + '.jpg'
                      ,result2)


def lca_fun_I_II(hjyx):
    warn_rights = []         #右侧报警等级
    warn_lefts = []         #左侧报警等级
    state_machines = []         #处于状态机的哪个状态
    x = []
    y = []
    turnsignals = []
    ttcs = []
    ttcd = []
    position_x = []
    position_y = []
    timestamp_a = []
    utimed = []
    velocity_vy = []   #障碍物的速度Y
    velocitys = []         #本车速度
    ttcy = []

    APP = ReadLcmAll()    #实例化
    lcmlog_dataframe = APP.get_lcm_dataset(
    hjyx)                        #数据包
    channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abLcaDebug")     #LCA通道数据
    lca = lca_debug_pb2.LCADebug()
    for packet in packets:
        lca.ParseFromString(packet)
        warn_rights.append(lca.cvw_warn_right)
        warn_lefts.append(lca.cvw_warn_left)
        state_machines.append(lca.cvw_state_machine)
        w = lca.debug_analy_obstacles.obstacle_info
        z = lca.debug_analy_chassis
        x.append(w)
        y.append(z)

    for a,b in zip(x,timestamps):
        for c in a:
            if c.position_x > 0 :
                ttcs.append(c.ttc)
                # timestamp_a.append(b)
                position_x.append(c.position_x)
                position_y.append(c.position_y)
                velocity_vy.append(c.velocity_vy)
    for i in y:
        turnsignals.append(i.turnsignal)

    channel_starting_time, timestamp, packets = APP.unpack_packets(lcmlog_dataframe, "abL10n")  # GPS通道数据
    gps = gps_imu_info_pb2.gpsImu()
    for packet in packets:
        gps.ParseFromString(packet)
        velocitys.append(gps.velocity)
    lookup = APP.lookup_data()           #目标车数据
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']
    key = APP.case_info_dict['key']

    timestamp_x = []
    timestamp_e = []
    timestamp_f = []
    for i in timestamp:  # gps通道abL10n的时间
        timestamp_e.append(i)  # timestamp 转换成列表 timestamp_e
    for i in timestamps:  # DOW通道abDowToDebug的时间
        timestamp_f.append(i)  # timestamps 转换成列表 timestamp_f

    if len(timestamp_f) < len(timestamp_e):  # 判断两个timestamp的大小，使用小的
        timestamp_x = timestamp_f
    else:
        timestamp_x = timestamp_e

    dd = []
    timestampd = []
    if len(timestamp_x) <= len(utime):
        for a in utime:
            a1 = round(a, 2)
            for b in timestamp_x:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(timestamp_x.index(b))
    else:
        for a in timestamp_x:
            a1 = round(a, 2)
            for b in utime:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(utime.index(b))

    timestamp_d = []
    timestampd = []
    for a in utime:
        a1 = round(a, 2)
        for b in timestamp_x:
            b1 = round(b, 2)
            if a1 == b1:
                timestampd.append(b)
                timestamp_d.append(timestamp_x.index(b))

    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []  # 时间同步后的目标车X
    UTM_Y_a = []  # 时间同步后的目标车Y
    wey4_velocity_a = []  # 时间同步后的目标车速度
    velocitys_a = []  # 时间同步后的自车速度
    position_y_a = []  # 自车感知Y值
    velocity_vy_a = []
    position_y_a = []
    for i in dd:  # 时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])

    ttcz = []
    velocitys_b = []
    for a, b, c in zip(UTM_Y_a, wey4_velocity_a, velocitys_a):  # 时间同步后的ttc
        t = (a + 4.7) / (b / 3.6 - c)
        ttcd.append(-t)
        velocitys_b.append(c * 3.6)
    if UTM_X_a[0] > 0:  # 单侧第一阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a

    # if  1 in warn_rights_a :        #单侧第一阶段报警
    #     warn1 = warn_rights_a
    # else:
    #     warn1 = warn_lefts_a
    # if 2 in warn_rights_a :        #单侧第2阶段报警
    #     warn2 = warn_rights_a
    # else:
    #     warn2 = warn_lefts_a

    UTM_X_b = []  # _b为左侧报警等级=1时
    UTM_Y_b = []
    warn_rights_b = []
    warn_lefts_b = []
    ttc_b = []
    wey4_velocity_b = []
    timestamp_b = []
    UTM_X_c = []  # _c为左侧报警等级!=1时
    UTM_Y_c = []
    warn_b = []
    warn_c = []
    warn_rights_c = []
    warn_lefts_c = []
    ttc_c = []
    wey4_velocity_c = []
    timestamp_c = []
    for a, b, c, d, e, f in zip(warn, UTM_X_a, UTM_Y_a, ttcd, wey4_velocity_a, timestampd):
        if a == 1:  # 左侧报警等级=1时的X，Y，ttc
            warn_rights_b.append(a)
            warn_lefts_b.append(a)
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)

        elif a == 2:
            warn_rights_b.append(a)
            warn_lefts_b.append(a)
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)

        else:  # 左侧报警等级！=1时的X，Y，ttc
            warn_rights_c.append(a)
            warn_lefts_c.append(a)
            warn_c.append(a)
            UTM_X_c.append(b)
            UTM_Y_c.append(c)
            ttc_c.append(d)
            wey4_velocity_c.append(e)
            timestamp_c.append(f)

    timestamp_amax = []
    timestamp_amin = []
    timestamp_pingjun = []
    timestamp_sum = []
    velocitys_max = []
    velocitys_min = []
    velocitys_sum = []
    velocitys_average = []
    for a, b in zip(velocitys_b, timestampd):  # 被测车辆最大速度/最小速度
        if a == max(velocitys_b):
            velocitys_max.append(a)
            timestamp_amax.append(b)
        if a == min(velocitys_b):
            velocitys_min.append(a)
            timestamp_amin.append(b)
    for a, b in zip(velocitys_b, timestampd):  # 平均速度
        t = sum(velocitys_b) / len(velocitys_b)
        velocitys_average.append(t)
        timestamp_pingjun.append(b)
    # print(t)
    wey4_velocity_max = []
    wey4_velocity_min = []
    timestampd_bmax = []
    timestampd_bmin = []
    wey4_velocity_average = []
    timestampd_average = []
    for a, b in zip(timestampd, wey4_velocity_a):  # 目标车辆最大速度/最小速度
        if b == max(wey4_velocity_a):
            wey4_velocity_max.append(b)
            timestampd_bmax.append(a)
        if b == min(wey4_velocity_a):
            wey4_velocity_min.append(b)
            timestampd_bmin.append(a)
    for a, b in zip(wey4_velocity_a, timestampd):  # 平均速度
        t = sum(wey4_velocity_a) / len(wey4_velocity_a)
        wey4_velocity_average.append(t)
        timestampd_average.append(b)
    UTM_X_max = []
    UTM_X_min = []
    timestampd_cmax = []
    timestampd_cmin = []
    UTM_X_average = []
    for a, b in zip(timestampd, UTM_X_a):  # 目标车的最大/最小X值
        if b == max(UTM_X_a):
            UTM_X_max.append(b)
            timestampd_cmax.append(a)
        if b == min(UTM_X_a):
            UTM_X_min.append(b)
            timestampd_cmin.append(a)
    for a, b in zip(UTM_X_a, timestampd):  # 目标车的平均X值
        t = sum(UTM_X_a) / len(UTM_X_a)
        UTM_X_average.append(t)
        timestampd_average.append(b)
    UTM_Y_max = []
    UTM_Y_min = []
    timestampd_dmax = []
    timestampd_dmin = []
    UTM_Y_average = []
    for a, b in zip(timestampd, UTM_Y_a):  # 目标车的最大/最小Y值
        if b == max(UTM_Y_a):
            UTM_Y_max.append(b)
            timestampd_dmax.append(a)
        if b == min(UTM_Y_a):
            UTM_Y_min.append(b)
            timestampd_dmin.append(a)
    for a, b in zip(UTM_Y_a, timestampd):  # 目标车的平均X值
        t = sum(UTM_Y_a) / len(UTM_Y_a)
        UTM_Y_average.append(t)
        timestampd_average.append(b)

    fig = plt.figure(figsize=(18, 12))  # 创建画布,绘制场景还原模型
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    ax.axis["x"] = ax.new_floating_axis(0, 0)
    ax.axis["x"].set_axisline_style("->", size=1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1, 0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size=1.0)
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")
    plt.xlim(-60, 60)
    plt.ylim(-60, 60)
    m = timestampd.index(timestamp_b[-1]) + 1
    s = len(ttc_b) // 2  # 报警中的一个点
    xs = timestampd[m] - timestamp_b[0]
    car = [
        [UTM_X_c[0], UTM_Y_c[0], timestamp_c[0], wey4_velocity_c[0], ttc_c[0]],  # 报警前
        [UTM_X_b[0], UTM_Y_b[0], timestamp_b[0], wey4_velocity_b[0], ttc_b[0]],  # 报警开始时刻
        [UTM_X_b[s], UTM_Y_b[s], timestamp_b[s], wey4_velocity_b[s], ttc_b[s]],  # 报警中
        [UTM_X_a[m], UTM_Y_a[m], timestampd[m], wey4_velocity_a[m], ttcd[m]],  # 报警结束时刻
        [UTM_X_c[-10], UTM_Y_c[-10], timestamp_c[-10], wey4_velocity_c[-10], ttc_c[-10]]  # 报警解除之后
    ]

    for p in car:
        plt.plot([p[0] + 0.92, p[0] - 0.92, p[0] - 0.92, p[0] + 0.92, p[0] + 0.92],
                 [p[1] + 3.7, p[1] + 3.7, p[1] - 0.9, p[1] - 0.9, p[1] + 3.7], 'g')  # 目标车模型
        plt.annotate('', xy=(p[0], p[1]),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:
            plt.text(p[0] - 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")  # 文本注释
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),  # 箭头注释
                         xytext=(p[0] - 20, p[1]),
                         weight="bold", color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            if p[4] > 0:
                plt.text(p[0] - 20, p[1] - 2, 'ttc=''%.1f' % p[4], size=6, weight="bold", color="b")  # 文本注释

        else:
            plt.text(p[0] + 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),
                         xytext=(p[0] + 20, p[1]),
                         weight="bold", color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            if p[4] > 0:
                plt.text(p[0] + 20, p[1] - 2, 'ttc=''%.1f' % p[4], size=6, weight="bold", color="b")

    plt.text(50, 50, 'red car:VUT', size=8, color="r")  # 自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92, -0.92, -0.92, 0.92, 0.92], [3.6, 3.6, -1, -1, 3.6], 'r')  # 自车模型

    plt.plot([1.4, 3.9, 3.9, 1.4, 1.4], [-6, -6, -51, -51, -6], 'y:', label='cvw_warn_right')  # 右侧报警区域
    plt.plot([-1.4, -3.9, -3.9, -1.4, -1.4], [-6, -6, -51, -51, -6], 'r:', label='cvw_warn_left')  # 左侧报警区域
    plt.legend()
    plt.title('lca')
    # plt.show()
    name2 = zdhq + APP.lcmlog_dict['filename'] + 'p4'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    x = np.linspace(0, 2, 200)  # 以下为测试状态模型
    fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(2, 1, 1)  # Add a subplot to the current figure
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    # plt.annotate(('X_MAX=''%.1f'%UTM_X_max[0]), xy=(timestampd_cmax[0], UTM_X_max[0]),
    #                  xytext=(timestampd_cmax[0] + 1 , UTM_X_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_MIN=''%.1f'%UTM_X_min[0]), xy=(timestampd_cmin[0], UTM_X_min[0]),
    #                  xytext=(timestampd_cmin[0] + 1 , UTM_X_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_average=''%.1f'%UTM_X_average[0]), xy=(timestampd_average[0], UTM_X_average[0]),
    #                  xytext=(timestampd_average[0] + 12 , UTM_X_average[0] - 25),
    #                  weight="bold", color="b", size=6,)
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    # plt.annotate(('Y_MAX=''%.1f'%UTM_Y_max[0]), xy=(timestampd_dmax[0], UTM_Y_max[0]),
    #                  xytext=(timestampd_dmax[0] + 1 , UTM_Y_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_MIN=''%.1f'%UTM_Y_min[0]), xy=(timestampd_dmin[0], UTM_Y_min[0]),
    #                  xytext=(timestampd_dmin[0] + 1 , UTM_Y_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_average=''%.1f'%UTM_Y_average[0]), xy=(timestampd_average[0], UTM_Y_average[0]),
    #                  xytext=(timestampd_average[0] + 12 , UTM_Y_average[0] - 10),
    #                  weight="bold", color="b", size=6,)
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend()  # 开启图例

    plt.subplot(2, 1, 2)
    plt.plot(timestampd, velocitys_b, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    # plt.annotate(('VUT_MAX=''%.1f'%velocitys_max[0]), xy=(timestamp_amax[0], velocitys_max[0]),
    #                  xytext=(timestamp_amax[0] + 1 , velocitys_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('VUT_MIN=''%.1f'%velocitys_min[0]), xy=(timestamp_amin[0], velocitys_min[0]),
    #                  xytext=(timestamp_amin[0] + 1 , velocitys_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('VUT_average=''%.1f'%velocitys_average[0]), xy=(timestamp_pingjun[0], velocitys_average[0]),
    #                  xytext=(timestamp_pingjun[0] + 5 , velocitys_average[0] + 8),
    #                  weight="bold", color="b", size=6,)
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    # plt.annotate(('GVT_MAX=''%.1f'%wey4_velocity_max[0]), xy=(timestampd_bmax[0], wey4_velocity_max[0]),
    #                  xytext=(timestampd_bmax[0] + 1 , wey4_velocity_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('GVT_MIN=''%.1f'%wey4_velocity_min[0]), xy=(timestampd_bmin[0], wey4_velocity_min[0]),
    #                  xytext=(timestampd_bmin[0] + 1 , wey4_velocity_min[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('GVT_average=''%.1f'%wey4_velocity_average[0]), xy=(timestampd_average[0], wey4_velocity_average[0]),
    #                  xytext=(timestampd_average[0] + 5 , wey4_velocity_average[0] + 6),
    #                  weight="bold", color="b", size=6,)
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend()  # 开启图例
    name1 = zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    x = np.linspace(0, 2, 200)  # 以下为测试状态模型
    fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    # plt.subplot(4,1,1) # Add a subplot to the current figure
    # plt.plot(timestampd,UTM_X_a,color='blue', label='real_X') # 绘制第一个子图 目标车位置
    # plt.annotate(('X_MAX=''%.1f'%UTM_X_max[0]), xy=(timestampd_cmax[0], UTM_X_max[0]),
    #                  xytext=(timestampd_cmax[0] + 1 , UTM_X_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_MIN=''%.1f'%UTM_X_min[0]), xy=(timestampd_cmin[0], UTM_X_min[0]),
    #                  xytext=(timestampd_cmin[0] + 1 , UTM_X_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_average=''%.1f'%UTM_X_average[0]), xy=(timestampd_average[0], UTM_X_average[0]),
    #                  xytext=(timestampd_average[0] + 12 , UTM_X_average[0] - 20),
    #                  weight="bold", color="b", size=6,)
    # plt.plot(timestampd,UTM_Y_a,color='green', label='real_Y')
    # plt.annotate(('Y_MAX=''%.1f'%UTM_Y_max[0]), xy=(timestampd_dmax[0], UTM_Y_max[0]),
    #                  xytext=(timestampd_dmax[0] + 1 , UTM_Y_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_MIN=''%.1f'%UTM_Y_min[0]), xy=(timestampd_dmin[0], UTM_Y_min[0]),
    #                  xytext=(timestampd_dmin[0] + 1 , UTM_Y_min[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_average=''%.1f'%UTM_Y_average[0]), xy=(timestampd_average[0], UTM_Y_average[0]),
    #                  xytext=(timestampd_average[0] + 12 , UTM_Y_average[0] - 10),
    #                  weight="bold", color="b", size=6,)
    # plt.xlabel('time  (s)')
    # plt.ylabel('m')
    # plt.legend() # 开启图例
    #
    # plt.subplot(4,1,2)
    # plt.plot(timestampd,velocitys_b, color='red', label='VUT_V') # 绘制第二个子图  自车与目标车速度
    # plt.annotate(('VUT_MAX=''%.1f'%velocitys_max[0]), xy=(timestamp_amax[0], velocitys_max[0]),
    #                  xytext=(timestamp_amax[0] + 1 , velocitys_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('VUT_MIN=''%.1f'%velocitys_min[0]), xy=(timestamp_amin[0], velocitys_min[0]),
    #                  xytext=(timestamp_amin[0] + 1 , velocitys_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('VUT_average=''%.1f'%velocitys_average[0]), xy=(timestamp_pingjun[0], velocitys_average[0]),
    #                  xytext=(timestamp_pingjun[0] + 5 , velocitys_average[0] + 8),
    #                  weight="bold", color="b", size=6,)
    # plt.plot(timestampd,wey4_velocity_a,color='blue', label='GVT_V')
    # # plt.annotate(('GVT_V_max=''%.1f'%wey4_velocity_max), xy=(timestamp_vmax, wey4_velocity_max),    #目标车最大速度
    # #                  xytext=(timestamp_vmax , wey4_velocity_max - 5),color="b", size=6,
    # #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('GVT_MAX=''%.1f'%wey4_velocity_max[0]), xy=(timestampd_bmax[0], wey4_velocity_max[0]),
    #                  xytext=(timestampd_bmax[0] + 1 , wey4_velocity_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('GVT_MIN=''%.1f'%wey4_velocity_min[0]), xy=(timestampd_bmin[0], wey4_velocity_min[0]),
    #                  xytext=(timestampd_bmin[0] + 1 , wey4_velocity_min[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('GVT_average=''%.1f'%wey4_velocity_average[0]), xy=(timestampd_average[0], wey4_velocity_average[0]),
    #                  xytext=(timestampd_average[0] + 5 , wey4_velocity_average[0] + 6),
    #                  weight="bold", color="b", size=6,)
    # plt.xlabel('time  (s)')
    # plt.ylabel('km/h')
    # plt.legend() # 开启图例
    plt.subplot(4, 1, 1)
    plt.plot(timestampd, ttcd, color='blue', label='ttc')  # 绘制第三个子图 状态机与报警等级
    plt.annotate(('ttc=''%.1f' % ttc_b[0]), xy=(timestamp_b[0], ttc_b[0]),  # 注释报警开始时刻的ttc
                 xytext=(timestamp_b[0] + 1, ttc_b[0] + 5),
                 weight="bold", color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.xlabel('time  (s)')
    plt.ylabel('ttc(s)')
    # plt.ylim(0, 10)
    plt.legend()  # 开启图例

    plt.subplot(4, 1, 2)
    plt.plot(timestampd, state_machines_a, color='green', label='state_machine')  # 绘制第四个子图 LCA状态机与报警等级
    plt.plot(timestampd, warn, color='red', label='warn_left')
    plt.plot(timestampd, warn, color='blue', label='warn_right')
    plt.text(timestamp_b[0], warn_b[0] + 3.2, 'time=''%.1f' % timestamp_b[0], size=6, weight="bold", color="b")  # 文本注释
    plt.annotate(('start_warn'), xy=(timestamp_b[0], warn_b[0]),  # 注释报警开始时刻
                 xytext=(timestamp_b[0], warn_b[0] + 2.5),
                 weight="bold", color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(timestampd[m], warn[m] + 3.2, 'time=''%.1f' % timestampd[m], size=6, weight="bold", color="b")  # 文本注释
    plt.annotate(('end_warn'), xy=(timestampd[m], warn[m]),  # 注释报警最后时刻
                 xytext=(timestampd[m], warn[m] + 2.5),
                 weight="bold", color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.xlabel('time  (s)')
    plt.ylabel('')
    plt.ylabel('level')
    plt.legend()  # 开启图例
    plt.subplots_adjust(hspace=1)
    warn_d = []
    for a, b in zip(warn, timestampd):  # 筛选报警等级=1对应的最小时间与最大时间，对应的报警等级区间
        if timestampd.index(timestamp_b[0]) <= warn.index(a) <= timestampd.index(timestamp_b[-1]):
            warn_d.append(a)
    if UTM_X_a[0] < 0:
        hjy = f'左侧'
    else:
        hjy = f'右侧'
    warn_1 = []
    warn_2 = []
    timestamp_b_1 = []
    timestamp_b_2 = []
    for a, b in zip(warn_b, timestamp_b):
        if a == 1:
            warn_1.append(a)
            timestamp_b_1.append(timestamp_b.index(b))
        elif a == 2:
            warn_2.append(a)
            timestamp_b_2.append(timestamp_b.index(b))
    if 0 in warn_d:
        result3 = '如果报警，测试用例失败。'
    if len(warn_1) == len(warn_b) and key[-1] == 1:
        result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                         "，开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % \
                  timestampd[m] + 's' \
                                  "，报警延续时长为：%0.1f" % xs + 's' \
                                                          f'，激活{hjy}第一阶段报警，且报警连续，与用例预期结果一致，测试用例通过。'
    elif len(warn_2) == len(warn_b) and key[-1] == 2:
        result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                         "，开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % \
                  timestampd[m] + 's' \
                                  "，报警延续时长为：%0.1f" % xs + 's' \
                                                          f'，激活{hjy}第二阶段报警，且报警连续，与用例预期结果一致，测试用例通过。'
    elif len(warn_1) < len(warn_b):
        if timestamp_b_1[0] < timestamp_b_1[-1] < timestamp_b_2[0] < timestamp_b_2[-1]:
            if key[-1] == 3:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                                 "，开始报警时刻为：%0.1f" % timestamp_b[
                              0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' + \
                          "，报警延续时长为：%0.1f" % xs + 's' \
                                                  f'，激活{hjy}第一阶段报警跳转到第二阶段报警，且报警连续，与用例预期结果一致，测试用例通过。'
            else:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                                 "，开始报警时刻为：%0.1f" % timestamp_b[
                              0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                                                                            "，报警延续时长为：%0.1f" % xs + 's' \
                                                                                                    f'，激活{hjy}第一阶段报警跳转到第二阶段报警，且报警连续，与用例预期结果不一致，测试用例失败。'
        elif timestamp_b_2[0] < timestamp_b_2[-1] < timestamp_b_1[0] < timestamp_b_1[-1]:
            if key[-1] == 4:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                                 "，开始报警时刻为：%0.1f" % timestamp_b[
                              0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                                                                            "，报警延续时长为：%0.1f" % xs + 's' \
                                                                                                    f'，激活{hjy}第二阶段报警跳转到第一阶段报警，且报警连续，与用例预期结果一致，测试用例通过。'
            else:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                                 "，开始报警时刻为：%0.1f" % timestamp_b[
                              0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                                                                            "，报警延续时长为：%0.1f" % xs + 's' \
                                                                                                    f'，激活{hjy}第二阶段报警跳转到第一阶段报警，且报警连续，与用例预期结果不一致，测试用例失败。'
        else:
            result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0] + 's' \
                                                             "开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % \
                      timestampd[m] + 's' \
                                      "，报警延续时长为：%0.1f" % xs + 's' \
                                                              f'，多次激活{hjy}报警，且报警连续，与用例预期结果不一致，测试用例失败。'
    elif len(warn) == len(warn_c):
        result3 = f'{hjy}未报警，测试用例失败。'
    # if  0 in warn_d:
    #     result3 = '如果报警，测试用例失败。'

    if key[-2] < 0:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[
                              7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功。'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[
                              7] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功。'
    else:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[
                              7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功。'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[
                              7] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功。'
    result1 = "通过数据分析，测试车最大车速为：%0.1f" % max(velocitys_max) + 'km/h' + ",测试车最小车速为: %0.1f" % min(velocitys_min) + 'km/h' \
                                                                                                                ",测试车平均车速为：%0.1f" % \
              velocitys_average[0] + 'km/h; \n' "配合车最大车速为：%0.1f" % max(wey4_velocity_max) + 'km/h' \
                                                                                            ",配合车最小车速为: %0.1f" % min(
        wey4_velocity_min) + 'km/h' + "配合车平均车速为：%0.1f" % wey4_velocity_average[0] + 'km/h; \n' \
                                                                                    "两车最大横向距离为：%0.1f" % max(
        UTM_X_max) + 'm' + "两车最小横向距离为: %0.1f" % min(UTM_X_min) + 'm' \
                                                                 "两车平均横向距离为：%0.1f" % UTM_X_average[
                  0] + 'm;\n'  "两车最大纵向距离为：%0.1f" % max(UTM_Y_max) + 'm' \
                                                                    ",两车最小纵向距离为: %0.1f" % min(
        UTM_Y_min) + 'm' + "两车平均纵向距离为：%0.1f" % UTM_Y_average[0] + 'm 。 \n'
    results = result1 + result2
    # print(result1)
    name3 = zdhq + APP.lcmlog_dict['filename'] + 'p5'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')  # 保存测试状态图片
    global mysql_status
    mysql_status = APP.word_docx(name1 + '.jpg', f'{results}', name2 + '.jpg', name3 + '.jpg', result3)  # 生成docx文档


def lca_active_passtive(ttrs):
    warn_rights = []         #右侧报警等级
    warn_lefts = []         #左侧报警等级
    state_machines = []         #处于状态机的哪个状态
    cvw_inhibit_reasons = []
    x = []
    y = []
    turnsignals = []
    ttcs = []
    ttcd = []
    CVW_ACTIVEs =[]
    CVW_PASSIVEs = []
    position_x = []
    position_y = []
    timestamp_a = []
    utimed = []
    velocity_vy = []   #障碍物的速度Y
    velocitys = []         #本车速度
    ttcy = []
    APP = ReadLcmAll()    #实例化
    lcmlog_dataframe = APP.get_lcm_dataset(
    ttrs)                        #数据包
    channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abLcaDebug")     #LCA通道数据
    lca = lca_debug_pb2.LCADebug()
    for packet in packets:
        lca.ParseFromString(packet)
        warn_rights.append(lca.cvw_warn_right)
        warn_lefts.append(lca.cvw_warn_left)
        state_machines.append(lca.cvw_state_machine)
        cvw_inhibit_reasons.append(lca.cvw_inhibit_reason)
        CVW_ACTIVEs.append(lca.CVW_ACTIVE)
        CVW_PASSIVEs.append(lca.CVW_PASSIVE)
        w = lca.debug_analy_obstacles.obstacle_info
        z = lca.debug_analy_chassis
        x.append(w)
        y.append(z)

    for a,b in zip(x,timestamps):
        for c in a:
            if c.position_x > 0 :
                ttcs.append(c.ttc)
                # timestamp_a.append(b)
                position_x.append(c.position_x)
                position_y.append(c.position_y)
                velocity_vy.append(c.velocity_vy)
    for i in y:
        turnsignals.append(i.turnsignal)
        # print(turnsignals)

    channel_starting_time, timestamp, packets = APP.unpack_packets(lcmlog_dataframe, "abL10n")  # GPS通道数据
    gps = gps_imu_info_pb2.gpsImu()
    for packet in packets:
        gps.ParseFromString(packet)
        velocitys.append(gps.velocity)
    lookup = APP.lookup_data()           #目标车数据
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']
    key = APP.case_info_dict['key']

    timestamp_x = []
    timestamp_e = []
    timestamp_f = []
    for i in timestamp:                 #gps通道abL10n的时间
        timestamp_e.append(i)           #timestamp 转换成列表 timestamp_e
    for i in timestamps:                #LCA通道abLcaDebug的时间
        timestamp_f.append(i)           #timestamps 转换成列表 timestamp_f

    if len(timestamp_f) < len(timestamp_e):     #判断两个timestamp的大小，使用小的
        timestamp_x = timestamp_f
    else:
        timestamp_x = timestamp_e

    dd = []
    timestampd = []
    if len(timestamp_x) <= len(utime):
        for a in utime:
            a1 = round(a, 2)
            for b in timestamp_x:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(timestamp_x.index(b))
    else:
        for a in timestamp_x:
            a1 = round(a, 2)
            for b in utime:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(utime.index(b))

    timestamp_d = []
    timestampd = []
    for a in utime:
        a1 = round(a, 2)
        for b in timestamp_x:
            b1 = round(b, 2)
            if a1 == b1:
                timestampd.append(b)
                timestamp_d.append(timestamp_x.index(b))

    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []   #时间同步后的目标车X
    UTM_Y_a = []   #时间同步后的目标车Y
    wey4_velocity_a = []   #时间同步后的目标车速度
    velocitys_a = []       #时间同步后的自车速度
    position_y_a = []      #自车感知Y值
    velocity_vy_a = []
    position_y_a = []
    cvw_inhibit_reason_a = []
    for i in dd:                                  #时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])
        cvw_inhibit_reason_a.append(cvw_inhibit_reasons[i])

    ttcz = []
    velocitys_b = []
    for a,b,c in zip(UTM_Y_a,wey4_velocity_a,velocitys_a):#时间同步后的ttc
        t = (a+4.7)/(b/3.6 -c)
        ttcd.append(-t)
        velocitys_b.append(c * 3.6)
    # for i in range(0,len(UTM_Y)):                    #时间同步前的ttc
    #     t = UTM_Y[i]/((wey4_velocity[i]-velocitys[i])/3.6)
    #     ttcz.insert(i,-t)
    # cc = []
    # for a,b,c,d in zip(UTM_X_a,UTM_Y_a,velocitys_a,timestampd):
    #     if c == max(cc):
    #         cc.append(c)
    #         print(c)
    # print('最大值：'+str(max(velocitys_a)),'最小值：'+str(min(velocitys_a)),'求和：'+str(sum(velocitys_a)),
    #       '平均值：'+str(sum()/len(velocitys_a)),sep='\n')
    if UTM_X_a[0] > 0:        #单侧第一阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a

    UTM_X_b = []            #_b为左侧报警等级=1时
    UTM_Y_b = []
    warn_rights_b = []
    warn_lefts_b = []
    ttc_b = []
    wey4_velocity_b = []
    timestamp_b = []
    UTM_X_c = []            #_c为左侧报警等级!=1时
    UTM_Y_c = []
    warn_rights_c = []
    warn_lefts_c = []
    ttc_c = []
    warn_b = []
    warn_c = []
    wey4_velocity_c = []
    timestamp_c = []
    for a,b,c,d,e,f in zip(warn,UTM_X_a,UTM_Y_a,ttcd,wey4_velocity_a,timestampd):
        if  a == 1 :                 #左侧报警等级=1时的X，Y，ttc
            warn_b.append(a)
            warn_lefts_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
        if  a == 2 :                 #左侧报警等级=1时的X，Y，ttc
            warn_b.append(a)
            warn_lefts_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)

        else:                   #左侧报警等级！=1时的X，Y，ttc
            warn_c.append(a)
            # warn_lefts_c.append(a)
            UTM_X_c.append(b)
            UTM_Y_c.append(c)
            ttc_c.append(d)
            wey4_velocity_c.append(e)
            timestamp_c.append(f)

    timestamp_amax = []
    timestamp_amin = []
    timestamp_pingjun = []
    timestamp_sum = []
    velocitys_max = []
    velocitys_min = []
    velocitys_sum = []
    velocitys_average = []
    for a,b in zip(velocitys_b,timestampd):        #被测车辆最大速度/最小速度
        if a == max(velocitys_b):
            velocitys_max.append(a)
            timestamp_amax.append(b)
        if a == min(velocitys_b):
            velocitys_min.append(a)
            timestamp_amin.append(b)
    for a,b in zip(velocitys_b,timestampd):     #平均速度
        t = sum(velocitys_b) / len(velocitys_b)
        velocitys_average.append(t)
        timestamp_pingjun.append(b)
    wey4_velocity_max = []
    wey4_velocity_min = []
    timestampd_bmax = []
    timestampd_bmin = []
    wey4_velocity_average = []
    timestampd_average = []
    for a,b in zip(timestampd,wey4_velocity_a):     #目标车辆最大速度/最小速度
        if b == max(wey4_velocity_a):
            wey4_velocity_max.append(b)
            timestampd_bmax.append(a)
        if b == min(wey4_velocity_a):
            wey4_velocity_min.append(b)
            timestampd_bmin.append(a)
    for a,b in zip(wey4_velocity_a,timestampd):            #平均速度
        t = sum(wey4_velocity_a) / len(wey4_velocity_a)
        wey4_velocity_average.append(t)
        timestampd_average.append(b)
    UTM_X_max = []
    UTM_X_min = []
    timestampd_cmax = []
    timestampd_cmin = []
    UTM_X_average = []
    for a,b in zip(timestampd,UTM_X_a):          #目标车的最大/最小X值
        if b == max(UTM_X_a):
            UTM_X_max.append(b)
            timestampd_cmax.append(a)
        if b == min(UTM_X_a):
            UTM_X_min.append(b)
            timestampd_cmin.append(a)
    for a,b in zip(UTM_X_a,timestampd):             #目标车的平均X值
        t = sum(UTM_X_a) / len(UTM_X_a)
        UTM_X_average.append(t)
        timestampd_average.append(b)
    #print(UTM_X_average)
    UTM_Y_max = []
    UTM_Y_min = []
    timestampd_dmax = []
    timestampd_dmin = []
    UTM_Y_average = []
    for a,b in zip(timestampd,UTM_Y_a):                 #目标车的最大/最小Y值
        if b == max(UTM_Y_a):
            UTM_Y_max.append(b)
            timestampd_dmax.append(a)
        if b == min(UTM_Y_a):
            UTM_Y_min.append(b)
            timestampd_dmin.append(a)
    for a,b in zip(UTM_Y_a,timestampd):             #目标车的平均X值
        t = sum(UTM_Y_a) / len(UTM_Y_a)
        UTM_Y_average.append(t)
        timestampd_average.append(b)

    fig = plt.figure(figsize=(18, 12))  # 创建画布,绘制场景还原模型
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    ax.axis["x"] = ax.new_floating_axis(0,0)
    ax.axis["x"].set_axisline_style("->", size = 1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1,0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size = 1.0)
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")
    plt.xlim(-60,60)
    plt.ylim(-60,60)

    m = timestampd.index(timestamp_b[-1]) + 1
    s = len(ttc_b)//2    #报警中的一个点
    xs = timestampd[m] - timestamp_b[0]
    car = [
            [UTM_X_b[0],UTM_Y_b[0],timestamp_b[0],wey4_velocity_b[0],ttcd[0]],      #报警开始时刻
            [UTM_X_b[s],UTM_Y_b[s],timestamp_b[s],wey4_velocity_b[s],ttcd[s]],      #报警中
            [UTM_X_a[m],UTM_Y_a[m],timestampd[m],wey4_velocity_a[m],ttcd[m]],     #报警结束时刻
            [UTM_X_c[-10],UTM_Y_c[-10],timestamp_c[-10],wey4_velocity_c[-10],ttcd[-10]]   #报警解除之后
            ]

    for p in car:
        plt.plot([p[0]+0.92,p[0]-0.92,p[0]-0.92,p[0]+0.92,p[0]+0.92],
                 [p[1]+3.7,p[1]+3.7,p[1]-0.9,p[1]-0.9,p[1]+3.7],'g')      #目标车模型
        plt.annotate('', xy=(p[0], p[1]),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:
            plt.text(p[0] - 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")  #文本注释
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),    #箭头注释
                     xytext=(p[0]-20,p[1]),
                     weight="bold",color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            # if p[4] < 0:
            #     plt.text(p[0]-20, p[1]-2,'ttc=''%.1f'%p[4],size=6,weight="bold",color="b")     #文本注释

        else:
            plt.text(p[0] + 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),
                     xytext=(p[0] + 20, p[1]),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            if p[4] > 0 :
                plt.text(p[0] + 20, p[1] - 2, 'ttc=''%.1f' % p[4], size=6, weight="bold", color="b")

    plt.text(50, 50, 'red car:VUT', size=8, color="r")  #自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92,-0.92,-0.92,0.92,0.92],[3.6,3.6,-1,-1,3.6],'r')  #自车模型

    plt.plot([1.4,3.9,3.9,1.4,1.4],[-6,-6,-51,-51,-6],'y:',label='cvw_warn_right') #右侧报警区域
    plt.plot([-1.4,-3.9,-3.9,-1.4,-1.4],[-6,-6,-51,-51,-6],'r:',label='cvw_warn_left') #左侧报警区域
    plt.legend()
    plt.title('lca')
    #plt.show()
    name2 = zdhq + APP.lcmlog_dict['filename'] + 'p4'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')               #保存场景还原图片

    x = np.linspace(0,2,200)     #以下为测试状态模型
    fig, ax = plt.subplots(2,2) # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(2,1,1) # Add a subplot to the current figure
    plt.plot(timestampd,UTM_X_a,color='blue', label='real_X') # 绘制第一个子图 目标车位置
    # plt.annotate(('X_MAX=''%.1f'%UTM_X_max[0]), xy=(timestampd_cmax[0], UTM_X_max[0]),
    #                  xytext=(timestampd_cmax[0] + 1 , UTM_X_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_MIN=''%.1f'%UTM_X_min[0]), xy=(timestampd_cmin[0], UTM_X_min[0]),
    #                  xytext=(timestampd_cmin[0] + 1 , UTM_X_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_average=''%.1f'%UTM_X_average[0]), xy=(timestampd_average[0], UTM_X_average[0]),
    #                  xytext=(timestampd_average[0] + 12 , UTM_X_average[0] - 25),
    #                  weight="bold", color="b", size=6,)
    plt.plot(timestampd,UTM_Y_a,color='green', label='real_Y')
    # plt.annotate(('Y_MAX=''%.1f'%UTM_Y_max[0]), xy=(timestampd_dmax[0], UTM_Y_max[0]),
    #                  xytext=(timestampd_dmax[0] + 1 , UTM_Y_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_MIN=''%.1f'%UTM_Y_min[0]), xy=(timestampd_dmin[0], UTM_Y_min[0]),
    #                  xytext=(timestampd_dmin[0] + 1 , UTM_Y_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_average=''%.1f'%UTM_Y_average[0]), xy=(timestampd_average[0], UTM_Y_average[0]),
    #                  xytext=(timestampd_average[0] + 12 , UTM_Y_average[0] - 10),
    #                  weight="bold", color="b", size=6,)
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend() # 开启图例

    plt.subplot(2,1,2)
    plt.plot(timestampd,velocitys_b, color='red', label='VUT_V') # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd,wey4_velocity_a,color='blue', label='GVT_V')
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend() # 开启图例
    name1 = zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')               #保存场景还原图片

    x = np.linspace(0,2,200)     #以下为测试状态模型
    fig, ax = plt.subplots(2,2) # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    # plt.subplot(4,1,1) # Add a subplot to the current figure
    # plt.plot(timestampd,UTM_X_a,color='blue', label='real_X') # 绘制第一个子图 目标车位置
    # plt.annotate(('X_MAX=''%.1f'%UTM_X_max[0]), xy=(timestampd_cmax[0], UTM_X_max[0]),
    #                  xytext=(timestampd_cmax[0] + 1 , UTM_X_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('X_MIN=''%.1f'%UTM_X_min[0]), xy=(timestampd_cmin[0], UTM_X_min[0]),
    #                  xytext=(timestampd_cmin[0] + 1 , UTM_X_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # # plt.annotate(('X_average=''%.1f'%UTM_X_average[0]), xy=(timestampd_average[0], UTM_X_average[0]),
    # #                  xytext=(timestampd_average[0] + 10 , UTM_X_average[0] + 25),
    # #                  weight="bold", color="b", size=6,)
    # plt.plot(timestampd,UTM_Y_a,color='green', label='real_Y')
    # plt.annotate(('Y_MAX=''%.1f'%UTM_Y_max[0]), xy=(timestampd_dmax[0], UTM_Y_max[0]),
    #                  xytext=(timestampd_dmax[0] + 1 , UTM_Y_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('Y_MIN=''%.1f'%UTM_Y_min[0]), xy=(timestampd_dmin[0], UTM_Y_min[0]),
    #                  xytext=(timestampd_dmin[0] + 1 , UTM_Y_min[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # # plt.annotate(('Y_average=''%.1f'%UTM_Y_average[0]), xy=(timestampd_average[0], UTM_Y_average[0]),
    # #                  xytext=(timestampd_average[0] + 10 , UTM_Y_average[0] + 27),
    # #                  weight="bold", color="b", size=6,)
    # plt.xlabel('time  (s)')
    # plt.ylabel('m')
    # plt.legend() # 开启图例
    #
    # plt.subplot(4,1,2)
    # plt.plot(timestampd,velocitys_b, color='red', label='VUT_V') # 绘制第二个子图  自车与目标车速度
    # plt.annotate(('VUT_MAX=''%.1f'%velocitys_max[0]), xy=(timestamp_amax[0], velocitys_max[0]),
    #                  xytext=(timestamp_amax[0] + 1 , velocitys_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('VUT_MIN=''%.1f'%velocitys_min[0]), xy=(timestamp_amin[0], velocitys_min[0]),
    #                  xytext=(timestamp_amin[0] + 1 , velocitys_min[0] + 10),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # # plt.annotate(('VUT_average=''%.1f'%velocitys_average[0]), xy=(timestamp_pingjun[0], velocitys_average[0]),
    # #                  xytext=(timestamp_pingjun[0] + 5 , velocitys_average[0] - 6),
    # #                  weight="bold", color="b", size=6,)
    # plt.plot(timestampd,wey4_velocity_a,color='blue', label='GVT_V')
    # plt.annotate(('GVT_MAX=''%.1f'%wey4_velocity_max[0]), xy=(timestampd_bmax[0], wey4_velocity_max[0]),
    #                  xytext=(timestampd_bmax[0] + 1 , wey4_velocity_max[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # plt.annotate(('GVT_MIN=''%.1f'%wey4_velocity_min[0]), xy=(timestampd_bmin[0], wey4_velocity_min[0]),
    #                  xytext=(timestampd_bmin[0] + 1 , wey4_velocity_min[0] + 5),
    #                  weight="bold", color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    # # plt.annotate(('GVT_average=''%.1f'%wey4_velocity_average[0]), xy=(timestampd_average[0], wey4_velocity_average[0]),
    # #                  xytext=(timestampd_average[0] + 5 , wey4_velocity_average[0] + 6),
    # #                  weight="bold", color="b", size=6,)
    # plt.xlabel('time  (s)')
    # plt.ylabel('km/h')
    # plt.legend() # 开启图例
    plt.subplot(4,1,1)
    plt.plot(timestampd,ttcd, color='blue', label='ttc')                   # 绘制第三个子图 状态机与报警等级
    plt.annotate(('ttc=''%.1f'%ttc_b[0]), xy=(timestamp_b[0], ttcd[0]),    #注释报警开始时刻的ttc
                     xytext=(timestamp_b[0] + 1 , ttc_b[0] + 5),
                     weight="bold", color="b", size=6)

    plt.xlabel('time  (s)')
    plt.ylabel('ttc(s)')
    # plt.ylim(0, 10)
    plt.legend() # 开启图例

    plt.subplot(4,1,2)
    plt.plot(timestampd,state_machines_a, color='green', label='state_machine') # 绘制第四个子图 LCA状态机与报警等级
    plt.plot(timestampd,warn,color='red', label='warn_left')
    plt.plot(timestampd,warn,color='blue', label='warn_right')
    plt.text(timestamp_b[0] , warn_b[0] + 3.2, 'time=''%.1f' % timestamp_b[0], size=6, weight="bold", color="b")  #文本注释
    plt.annotate(('start_warn'), xy=(timestamp_b[0], warn_b[0]),    #注释报警开始时刻
                     xytext=(timestamp_b[0] , warn_b[0] + 2.5),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(timestampd[m] , warn[m] + 3.2, 'time=''%.1f' % timestampd[m], size=6, weight="bold", color="b")  #文本注释
    plt.annotate(('end_warn'), xy=(timestampd[m], warn[m]),    #注释报警最后时刻
                     xytext=(timestampd[m] , warn[m] + 2.5),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.xlabel('time  (s)')
    plt.ylabel('ttc(s)')
    # plt.ylim(0, 10)
    plt.legend() # 开启图例
    plt.subplot(4,1,3)
    plt.plot(timestampd,cvw_inhibit_reason_a, color='green', label='cvw_inhibit_reason')
    plt.xlabel('time  (s)')
    plt.ylabel('')
    plt.ylabel('level')
    plt.legend() # 开启图例
    plt.subplots_adjust(hspace = 1)

    for a in cvw_inhibit_reason_a:    #抑制条件
        if a != 0:
            sign = cvw_inhibit_reason_a.index(a)
            number = a
            break
    warn_d = []
    for a,b in zip(warn,timestampd):            #筛选报警等级=1对应的最小时间与最大时间，对应的报警等级区间
        if timestampd.index(timestamp_b[0]) <= warn.index(a) <=timestampd.index(timestamp_b[-1]):
            warn_d.append(a)
    if UTM_X_a[0] < 0:
        hjy = f'左侧'
    else:
        hjy = f'右侧'
    cvw_inhibit_reason_b = []
    if 0 in warn_d:                              #判断用例通过或是失败：result
        result = f'重复报警，测试用例失败'
    else:
        if 1 or 2 in warn:
            if 1 in cvw_inhibit_reason_a and key[-1] == 6:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0]+ 's' \
                "，开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                "，经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1]  + " ,档位抑制； " \
                f'激活{hjy}第一阶段报警，LCA连续报警，且激活状态与抑制状态时间连续，测试用例通过。'
            elif 2 in cvw_inhibit_reason_a and key[-1] == 6:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0]+ 's' \
                "，开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                "，经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1]  + " ,车速抑制； " \
                f'激活{hjy}第一阶段报警，LCA连续报警，且激活状态与抑制状态时间连续，测试用例通过。'
            elif 4 in cvw_inhibit_reason_a and key[-1] == 6:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0]+ 's' \
                "，开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                "，经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1]  + " ,曲率抑制； " \
                f'激活{hjy}第一阶段报警，LCA连续报警，且激活状态与抑制状态时间连续，测试用例通过。'
            elif 8 in cvw_inhibit_reason_a and key[-1] == 6:
                result3 = f"通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0]+ 's' \
                "，开始报警时刻为：%0.1f" % timestamp_b[0] + 's' + "，结束报警时刻为：%0.1f" % timestampd[m] + 's' \
                "，经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1]  + " ,同方向无车抑制； " \
                f'激活{hjy}第一阶段报警，LCA连续报警，且激活状态与抑制状态时间连续，测试用例通过。'
            else:
                result3 = "经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1]  + " , " \
                "LCA连续报警，且激活状态与抑制状态时间连续，测试用例通过。"
        else:
            result3 = "经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1]  + " , " \
                "LCA连续报警，且激活状态与抑制状态时间连续，测试用例通过。"
    # else:
    #     result3 = f'经数据分析，LCA未激活报警，测试用例失败。'
    # state_machines_b=[]
    # for x in state_machines:
    #     if x == 3 or 5:
    #         state_machines_b.append(x)
    #         if state_machines_b[0] > state_machines_b[-1]:
    #             result3 = '满足抑制，测试用例通过'
    #         else:
    #             result3 = '不满足抑制,测试用例失败'
    # print(state_machines_b)
    if key[-2] < 0:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功；'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功；'
    else:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功；'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功；'

    results =  result3
    result1 = "通过数据分析，测试车最大车速为：%0.1f" % max(velocitys_max)+ 'km/h' +  ",测试车最小车速为: %0.1f" % min(velocitys_min)+'km/h' \
    ",测试车平均车速为：%0.1f" % velocitys_average[0] + 'km/h； \n' "配合车最大车速为：%0.1f" % max(wey4_velocity_max)+ 'km/h' \
    ",配合车最小车速为: %0.1f" % min(wey4_velocity_min)+'km/h' + "配合车平均车速为：%0.1f" % wey4_velocity_average[0] + 'km/h； \n'\
    "两车最大横向距离为：%0.1f" % max(UTM_X_max)+ 'm' + "两车最小横向距离为: %0.1f" % min(UTM_X_min)+'m' \
    "两车平均横向距离为：%0.1f" % UTM_X_average[0] + 'm； \n'  "两车最大纵向距离为：%0.1f" % max(UTM_Y_max) + 'm' \
    ",两车最小纵向距离为: %0.1f" % min(UTM_Y_min )+'m' + "两车平均纵向距离为：%0.1f" % UTM_Y_average[0] + 'm 。 \n'
    resultss = result1 + result2
    name3 = zdhq + APP.lcmlog_dict['filename'] + 'p5'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')                         #保存测试状态图片
    global mysql_status
    mysql_status = APP.word_docx(name1 + '.jpg',f'{resultss}',name2 + '.jpg',name3 + '.jpg',results)     #生成docx文档



def lca_xingneng(ttrs):
    warn_rights = []         #右侧报警等级
    warn_lefts = []         #左侧报警等级
    state_machines = []         #处于状态机的哪个状态
    x = []
    y = []
    turnsignals = []
    ttcs = []
    ttcd = []
    position_x = []
    position_y = []
    timestamp_a = []
    utimed = []
    velocity_vy = []   #障碍物的速度Y
    velocitys = []         #本车速度
    ttcy = []

    APP = ReadLcmAll()    #实例化
    lcmlog_dataframe = APP.get_lcm_dataset(
    ttrs)                        #数据包
    channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abLcaDebug")     #LCA通道数据
    lca = lca_debug_pb2.LCADebug()
    for packet in packets:
        lca.ParseFromString(packet)
        warn_rights.append(lca.cvw_warn_right)
        warn_lefts.append(lca.cvw_warn_left)
        state_machines.append(lca.cvw_state_machine)
        w = lca.debug_analy_obstacles.obstacle_info
        z = lca.debug_analy_chassis
        x.append(w)
        y.append(z)

    for a,b in zip(x,timestamps):
        for c in a:
            if c.position_x > 0 :
                ttcs.append(c.ttc)
                # timestamp_a.append(b)
                position_x.append(c.position_x)
                position_y.append(c.position_y)
                velocity_vy.append(c.velocity_vy)
    for d in y :
        turnsignals.append(d.turnsignal)

    channel_starting_time, timestamp, packets = APP.unpack_packets(lcmlog_dataframe, "abL10n")  # GPS通道数据
    gps = gps_imu_info_pb2.gpsImu()
    for packet in packets:
        gps.ParseFromString(packet)
        velocitys.append(gps.velocity)
    lookup = APP.lookup_data()           #目标车数据
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']
    key = APP.case_info_dict['key']

    timestamp_x = []
    timestamp_e = []
    timestamp_f = []
    for i in timestamp:                 #gps通道abL10n的时间
        timestamp_e.append(i)           #timestamp 转换成列表 timestamp_e
    for i in timestamps:                #LCA通道abLcaDebug的时间
        timestamp_f.append(i)           #timestamps 转换成列表 timestamp_f

    if len(timestamp_f) < len(timestamp_e):     #判断两个timestamp的大小，使用小的
        timestamp_x = timestamp_f
    else:
        timestamp_x = timestamp_e

    dd = []
    timestampd = []
    if len(timestamp_x) <= len(utime):
        for a in utime:
            a1 = round(a, 2)
            for b in timestamp_x:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(timestamp_x.index(b))
    else:
        for a in timestamp_x:
            a1 = round(a, 2)
            for b in utime:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(utime.index(b))

    timestamp_d = []
    timestampd = []
    for a in utime:
        a1 = round(a, 2)
        for b in timestamp_x:
            b1 = round(b, 2)
            if a1 == b1:
                timestampd.append(b)
                timestamp_d.append(timestamp_x.index(b))
    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []   #时间同步后的目标车X
    UTM_Y_a = []   #时间同步后的目标车Y
    wey4_velocity_a = []   #时间同步后的目标车速度
    velocitys_a = []       #时间同步后的自车速度
    position_y_a = []      #自车感知Y值
    velocity_vy_a = []
    position_y_a = []
    turnsignals_a = []
    for i in dd:                                  #时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])
        turnsignals_a.append(turnsignals[i])

    ttcz = []
    velocitys_b = []
    for a,b,c in zip(UTM_Y_a,wey4_velocity_a,velocitys_a):#时间同步后的ttc
        t = (a+4.7)/(b/3.6 -c)
        ttcd.append(-t)
        velocitys_b.append(c * 3.6)

    if UTM_X_a[0] > 0:        #单侧第一阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a

    UTM_X_b = []            #_b为左侧报警等级=1时
    UTM_Y_b = []
    warn_rights_b = []
    warn_lefts_b = []
    ttc_b = []
    wey4_velocity_b = []
    timestamp_b = []
    turnsignals_b = []
    UTM_X_c = []            #_c为左侧报警等级!=1时
    UTM_Y_c = []
    warn_rights_c = []
    warn_lefts_c = []
    ttc_c = []
    warn_b = []
    warn_c = []
    wey4_velocity_c = []
    timestamp_c = []
    turnsignals_c = []
    for a,b,c,d,e,f,g in zip(warn,UTM_X_a,UTM_Y_a,ttcd,wey4_velocity_a,timestampd,turnsignals_a):
        if a == 2 :                 #左侧报警等级=1时的X，Y，ttc
            warn_rights_b.append(a)
            warn_lefts_b.append(a)
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
            turnsignals_b.append(g)
        elif a == 1 :
            warn_rights_b.append(a)
            warn_lefts_b.append(a)
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
            turnsignals_b.append(g)
        else:                   #左侧报警等级！=1时的X，Y，ttc
            warn_rights_c.append(a)
            warn_lefts_c.append(a)
            warn_c.append(a)
            UTM_X_c.append(b)
            UTM_Y_c.append(c)
            ttc_c.append(d)
            wey4_velocity_c.append(e)
            timestamp_c.append(f)
            turnsignals_c.append(g)

    timestamp_amax = []
    timestamp_amin = []
    timestamp_pingjun = []
    timestamp_sum = []
    velocitys_max = []
    velocitys_min = []
    velocitys_sum = []
    velocitys_average = []
    for a,b in zip(velocitys_b,timestampd):        #被测车辆最大速度/最小速度
        if a == max(velocitys_b):
            velocitys_max.append(a)
            timestamp_amax.append(b)
        if a == min(velocitys_b):
            velocitys_min.append(a)
            timestamp_amin.append(b)
    for a,b in zip(velocitys_b,timestampd):     #平均速度
        t = sum(velocitys_b) / len(velocitys_b)
        velocitys_average.append(t)
        timestamp_pingjun.append(b)
    wey4_velocity_max = []
    wey4_velocity_min = []
    timestampd_bmax = []
    timestampd_bmin = []
    wey4_velocity_average = []
    timestampd_average = []
    for a,b in zip(timestampd,wey4_velocity_a):     #目标车辆最大速度/最小速度
        if b == max(wey4_velocity_a):
            wey4_velocity_max.append(b)
            timestampd_bmax.append(a)
        if b == min(wey4_velocity_a):
            wey4_velocity_min.append(b)
            timestampd_bmin.append(a)
    for a,b in zip(wey4_velocity_a,timestampd):            #平均速度
        t = sum(wey4_velocity_a) / len(wey4_velocity_a)
        wey4_velocity_average.append(t)
        timestampd_average.append(b)
    UTM_X_max = []
    UTM_X_min = []
    timestampd_cmax = []
    timestampd_cmin = []
    UTM_X_average = []
    for a,b in zip(timestampd,UTM_X_a):          #目标车的最大/最小X值
        if b == max(UTM_X_a):
            UTM_X_max.append(b)
            timestampd_cmax.append(a)
        if b == min(UTM_X_a):
            UTM_X_min.append(b)
            timestampd_cmin.append(a)
    for a,b in zip(UTM_X_a,timestampd):             #目标车的平均X值
        t = sum(UTM_X_a) / len(UTM_X_a)
        UTM_X_average.append(t)
        timestampd_average.append(b)

    UTM_Y_max = []
    UTM_Y_min = []
    timestampd_dmax = []
    timestampd_dmin = []
    UTM_Y_average = []
    for a,b in zip(timestampd,UTM_Y_a):                 #目标车的最大/最小Y值
        if b == max(UTM_Y_a):
            UTM_Y_max.append(b)
            timestampd_dmax.append(a)
        if b == min(UTM_Y_a):
            UTM_Y_min.append(b)
            timestampd_dmin.append(a)
    for a,b in zip(UTM_Y_a,timestampd):             #目标车的平均X值
        t = sum(UTM_Y_a) / len(UTM_Y_a)
        UTM_Y_average.append(t)
        timestampd_average.append(b)

    fig = plt.figure(figsize=(18, 12))  # 创建画布,绘制场景还原模型
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    ax.axis["x"] = ax.new_floating_axis(0,0)
    ax.axis["x"].set_axisline_style("->", size = 1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1,0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size = 1.0)
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")
    plt.xlim(-60,60)
    plt.ylim(-60,60)

    m = timestampd.index(timestamp_b[-1]) + 1
    s = len(ttc_b)//2    #报警中的一个点
    car = [
            [UTM_X_c[0],UTM_Y_c[0],timestamp_c[0],wey4_velocity_c[0],ttc_c[0]],      #报警前
            [UTM_X_b[0],UTM_Y_b[0],timestamp_b[0],wey4_velocity_b[0],ttc_b[0]],      #报警开始时刻
            [UTM_X_b[s],UTM_Y_b[s],timestamp_b[s],wey4_velocity_b[s],ttc_b[s]],      #报警中
            [UTM_X_a[m],UTM_Y_a[m],timestampd[m],wey4_velocity_a[m],ttcd[m]],     #报警结束时刻
            [UTM_X_c[-1],UTM_Y_c[-1],timestamp_c[-1],wey4_velocity_c[-1],ttc_c[-1]]   #报警解除之后
            ]
    #print(UTM_Y_a[m])
    for p in car:
        plt.plot([p[0]+0.92,p[0]-0.92,p[0]-0.92,p[0]+0.92,p[0]+0.92],
                 [p[1]+3.7,p[1]+3.7,p[1]-0.9,p[1]-0.9,p[1]+3.7],'g')      #目标车模型
        plt.annotate('', xy=(p[0], p[1]),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:
            plt.text(p[0] - 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")  #文本注释
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),    #箭头注释
                     xytext=(p[0]-20,p[1]),
                     weight="bold",color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            if p[4] > 0:
                plt.text(p[0]-20, p[1]-2,'ttc=''%.1f'%p[4],size=6,weight="bold",color="b")     #文本注释

        else:
            plt.text(p[0] + 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),
                     xytext=(p[0] + 20, p[1]),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            if p[4] > 0 :
                plt.text(p[0] + 20, p[1] - 2, 'ttc=''%.1f' % p[4], size=6, weight="bold", color="b")

    plt.text(50, 50, 'red car:VUT', size=8, color="r")  #自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92,-0.92,-0.92,0.92,0.92],[3.6,3.6,-1,-1,3.6],'r')  #自车模型

    plt.plot([1.4,3.9,3.9,1.4,1.4],[-6,-6,-51,-51,-6],'y:',label='cvw_warn_right') #右侧报警区域
    plt.plot([-1.4,-3.9,-3.9,-1.4,-1.4],[-6,-6,-51,-51,-6],'r:',label='cvw_warn_left') #左侧报警区域
    plt.legend()
    plt.title('lca')
    #plt.show()
    name2 = zdhq + APP.lcmlog_dict['filename'] + 'p4'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')               #保存场景还原图片

    x = np.linspace(0,2,200)     #以下为测试状态模型
    fig, ax = plt.subplots(2,2) # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(2,1,1) # Add a subplot to the current figure
    plt.plot(timestampd,UTM_X_a,color='blue', label='real_X') # 绘制第一个子图 目标车位置
    plt.plot(timestampd,UTM_Y_a,color='green', label='real_Y')
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend() # 开启图例

    plt.subplot(2,1,2)
    plt.plot(timestampd,velocitys_b, color='red', label='VUT_V') # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd,wey4_velocity_a,color='blue', label='GVT_V')
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend() # 开启图例
    name1 = zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')               #保存场景还原图片

    x = np.linspace(0,2,200)     #以下为测试状态模型
    fig, ax = plt.subplots(2,2) # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(4,1,1)
    plt.plot(timestampd,ttcd, color='blue', label='ttc')                   # 绘制第三个子图 状态机与报警等级
    plt.annotate(('ttc=''%.1f'%ttc_b[0]), xy=(timestamp_b[0], ttc_b[0]),    #注释报警开始时刻的ttc
                     xytext=(timestamp_b[0] + 1 , ttc_b[0] + 5),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.xlabel('time  (s)')
    plt.ylabel('ttc(s)')
    # plt.ylim(0, 10)
    plt.legend() # 开启图例

    plt.subplot(4,1,2)
    plt.plot(timestampd,state_machines_a, color='green', label='state_machine') # 绘制第四个子图 LCA状态机与报警等级
    plt.plot(timestampd,warn,color='red', label='warn_left')
    plt.plot(timestampd,warn,color='blue', label='warn_right')
    plt.plot(timestampd,turnsignals_a,color='y', label='turnsignal')
    plt.text(timestamp_b[0] , warn_b[0] + 3.2, 'time=''%.1f' % timestamp_b[0], size=6, weight="bold", color="b")  #文本注释
    plt.annotate(('start_warn'), xy=(timestamp_b[0], warn_b[0]),    #注释报警开始时刻
                     xytext=(timestamp_b[0] , warn_b[0] + 2.5),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(timestampd[m] , warn[m] + 3.2, 'time=''%.1f' % timestampd[m], size=6, weight="bold", color="b")  #文本注释
    plt.annotate(('end_warn'), xy=(timestampd[m], warn[m]),    #注释报警最后时刻
                     xytext=(timestampd[m] , warn[m] + 2.5),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.xlabel('time  (s)')
    plt.ylabel('')
    plt.ylabel('level')
    plt.legend() # 开启图例
    plt.subplots_adjust(hspace = 1)

    warn_d = []
    for a,b in zip(warn,timestampd):            #筛选报警等级=1对应的最小时间与最大时间，对应的报警等级区间
        if timestampd.index(timestamp_b[0]) <= warn.index(a) <=timestampd.index(timestamp_b[-1]):
            warn_d.append(a)

    if UTM_X_a[0] < 0:
        hjy = f'左侧'
    else:
        hjy = f'右侧'

    warn_1 =[]
    warn_2 =[]
    timestamp_b_1 =[]
    timestamp_b_2 =[]
    for a,b in zip(warn_b,timestamp_b):
        if a == 1:
            warn_1.append(a)
            timestamp_b_1.append(timestamp_b.index(b))
        elif a == 2:
            warn_2.append(a)
            timestamp_b_2.append(timestamp_b.index(b))

    if len(warn_1) == len(warn_b) and key[-1] == 7:
        result3 = f'激活{hjy}第一阶段报警，且报警连续，无功能抑制，与用例预期结果一致，测试用例通过；'
    elif len(warn_2) == len(warn_b) and key[-1] == 8:
        result3 = f'激活{hjy}第二阶段报警，且报警连续，无功能抑制，与用例预期结果一致，测试用例通过；'
    elif len(warn_1) < len(warn_b):
        if timestamp_b_1[0] < timestamp_b_1[-1] < timestamp_b_2[0] < timestamp_b_2[-1]:
            result3 = f'激活{hjy}第一阶段报警跳转到第二阶段报警；'
        elif timestamp_b_2[0] < timestamp_b_2[-1] < timestamp_b_1[0] < timestamp_b_1[-1]:
            result3 = f'激活{hjy}第二阶段报警跳转到第一阶段报警；'
        else:
            result3 = f'多次激活{hjy}报警，测试用例失败；'
    elif len(warn) == len(warn_c):
        result3 = f'{hjy}未报警，测试用例失败；'

    if 0 in warn_d:                              #判断用例通过或是失败：result
        result4 ="重复报警，测试用例失败。"
    else:
        if 2 <= ttc_b[0] <= 3.5 and 0 <= abs(UTM_Y_a[m]) - 4.7 <= 5:
            result4 ="通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0]+ 's' + \
        '，功能规范为TTC<=3.5s报警，满足报警范围，测试用例通过。'
        else:
            result4 = "通过数据分析报警开始时刻TTC为：%0.1f" % ttc_b[0]+ 's' + \
        '，功能规范为TTC<=3.5s报警，不满足报警范围，测试用例不通过。'
    if key[-1] < 0:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功；'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功；'
    else:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功；'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功；'
    results =  result3 + result4
    result1 = "通过数据分析，测试车最大车速为：%0.1f" % max(velocitys_max)+ 'km/h' +  ",测试车最小车速为: %0.1f" % min(velocitys_min)+'km/h' \
    ",测试车平均车速为：%0.1f" % velocitys_average[0] + 'km/h; \n' "配合车最大车速为：%0.1f" % max(wey4_velocity_max)+ 'km/h' \
    ",配合车最小车速为: %0.1f" % min(wey4_velocity_min)+'km/h' + "配合车平均车速为：%0.1f" % wey4_velocity_average[0] + 'km/h; \n'\
    "两车最大横向距离为：%0.1f" % max(UTM_X_max)+ 'm' + "两车最小横向距离为: %0.1f" % min(UTM_X_min)+'m' \
    "两车平均横向距离为：%0.1f" % UTM_X_average[0] + 'm; \n'  "两车最大纵向距离为：%0.1f" % max(UTM_Y_max) + 'm' \
    ",两车最小纵向距离为: %0.1f" % min(UTM_Y_min )+'m' + "两车平均纵向距离为：%0.1f" % UTM_Y_average[0] + 'm 。 \n'
    resultss = result1 + result2
    name3 = zdhq + APP.lcmlog_dict['filename'] + 'p5'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')                         #保存测试状态图片
    #APP.word_docx(name1 + '.jpg',name2 + '.jpg',name3 + '.jpg',f'{result}')           #生成docx文档
    global mysql_status
    mysql_status = APP.word_docx(name1 + '.jpg',f'{resultss}',name2 + '.jpg',name3 + '.jpg',results)     #生成docx文档


def lca_passtive(ttrs):
    warn_rights = []  # 右侧报警等级
    warn_lefts = []  # 左侧报警等级
    state_machines = []  # 处于状态机的哪个状态
    x = []
    y = []
    turnsignals = []
    ttcs = []
    ttcd = []
    position_x = []
    position_y = []
    timestamp_a = []
    utimed = []
    velocity_vy = []  # 障碍物的速度Y
    velocitys = []  # 本车速度
    ttcy = []
    cvw_inhibit_reasons = []

    APP = ReadLcmAll()  # 实例化
    lcmlog_dataframe = APP.get_lcm_dataset(
        ttrs)  # 数据包
    channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abLcaDebug")  # LCA通道数据
    lca = lca_debug_pb2.LCADebug()
    for packet in packets:
        lca.ParseFromString(packet)
        warn_rights.append(lca.cvw_warn_right)
        warn_lefts.append(lca.cvw_warn_left)
        state_machines.append(lca.cvw_state_machine)
        cvw_inhibit_reasons.append(lca.cvw_inhibit_reason)
        w = lca.debug_analy_obstacles.obstacle_info
        z = lca.debug_analy_chassis
        x.append(w)
        y.append(z)

    for a, b in zip(x, timestamps):
        for c in a:
            if c.position_x > 0:
                ttcs.append(c.ttc)
                # timestamp_a.append(b)
                position_x.append(c.position_x)
                position_y.append(c.position_y)
                velocity_vy.append(c.velocity_vy)
    for i in y:
        turnsignals.append(i.turnsignal)

    channel_starting_time, timestamp, packets = APP.unpack_packets(lcmlog_dataframe, "abL10n")  # GPS通道数据
    gps = gps_imu_info_pb2.gpsImu()
    for packet in packets:
        gps.ParseFromString(packet)
        velocitys.append(gps.velocity)
    lookup = APP.lookup_data()  # 目标车数据
    utime = APP.gps_info_dict['utime']
    UTM_X = APP.gps_info_dict['UTM_X']
    UTM_Y = APP.gps_info_dict['UTM_Y']
    wey4_velocity = APP.gps_info_dict['wey4_velocity']
    key = APP.case_info_dict['key']

    timestamp_x = []
    timestamp_e = []
    timestamp_f = []
    for i in timestamp:  # gps通道abL10n的时间
        timestamp_e.append(i)  # timestamp 转换成列表 timestamp_e
    for i in timestamps:  # LCA通道abLcaDebug的时间
        timestamp_f.append(i)  # timestamps 转换成列表 timestamp_f

    if len(timestamp_f) < len(timestamp_e):  # 判断两个timestamp的大小，使用小的
        timestamp_x = timestamp_f
    else:
        timestamp_x = timestamp_e

    dd = []
    timestampd = []
    if len(timestamp_x) <= len(utime):
        for a in utime:
            a1 = round(a, 2)
            for b in timestamp_x:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(timestamp_x.index(b))
    else:
        for a in timestamp_x:
            a1 = round(a, 2)
            for b in utime:
                b1 = round(b, 2)
                if a1 == b1:
                    timestampd.append(b)
                    dd.append(utime.index(b))

    timestamp_d = []
    timestampd = []
    for a in utime:
        a1 = round(a, 2)
        for b in timestamp_x:
            b1 = round(b, 2)
            if a1 == b1:
                timestampd.append(b)
                timestamp_d.append(timestamp_x.index(b))

    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []  # 时间同步后的目标车X
    UTM_Y_a = []  # 时间同步后的目标车Y
    wey4_velocity_a = []  # 时间同步后的目标车速度
    velocitys_a = []  # 时间同步后的自车速度
    position_y_a = []  # 自车感知Y值
    velocity_vy_a = []
    position_y_a = []
    cvw_inhibit_reason_a = []
    for i in dd:  # 时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])
        cvw_inhibit_reason_a.append(cvw_inhibit_reasons[i])

    ttcz = []
    velocitys_b = []
    for a, b, c in zip(UTM_Y_a, wey4_velocity_a, velocitys_a):  # 时间同步后的ttc
        t = (a + 4.7) / (b / 3.6 - c)
        ttcd.append(-t)
        velocitys_b.append(c * 3.6)

    if 1 in warn_rights_a:  # 单侧第一阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a
    if 2 in warn_rights_a:  # 单侧第2阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a

    UTM_X_b = []  # _b为左侧报警等级=1时
    UTM_Y_b = []
    warn_rights_b = []
    warn_lefts_b = []
    ttc_b = []
    wey4_velocity_b = []
    timestamp_b = []
    UTM_X_c = []  # _c为左侧报警等级!=1时
    UTM_Y_c = []
    warn_rights_c = []
    warn_lefts_c = []
    ttc_c = []
    wey4_velocity_c = []
    timestamp_c = []
    for a, b, c, d, e, f in zip(warn, UTM_X_a, UTM_Y_a, ttcd, wey4_velocity_a, timestampd):
        if 0 < d <= 3.5:  # 左侧报警等级=1时的X，Y，ttc
            # warn_rights_b.append(a)
            # warn_lefts_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            # ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)

        else:  # 左侧报警等级！=1时的X，Y，ttc
            # warn_rights_c.append(a)
            # warn_lefts_c.append(a)
            UTM_X_c.append(b)
            UTM_Y_c.append(c)
            # ttc_c.append(d)
            wey4_velocity_c.append(e)
            timestamp_c.append(f)

    timestamp_amax = []
    timestamp_amin = []
    timestamp_pingjun = []
    timestamp_sum = []
    velocitys_max = []
    velocitys_min = []
    velocitys_sum = []
    velocitys_average = []
    for a, b in zip(velocitys_b, timestampd):  # 被测车辆最大速度/最小速度
        if a == max(velocitys_b):
            velocitys_max.append(a)
            timestamp_amax.append(b)
        if a == min(velocitys_b):
            velocitys_min.append(a)
            timestamp_amin.append(b)
    for a, b in zip(velocitys_b, timestampd):  # 平均速度
        t = sum(velocitys_b) / len(velocitys_b)
        velocitys_average.append(t)
        timestamp_pingjun.append(b)
    wey4_velocity_max = []
    wey4_velocity_min = []
    timestampd_bmax = []
    timestampd_bmin = []
    wey4_velocity_average = []
    timestampd_average = []
    for a, b in zip(timestampd, wey4_velocity_a):  # 目标车辆最大速度/最小速度
        if b == max(wey4_velocity_a):
            wey4_velocity_max.append(b)
            timestampd_bmax.append(a)
        if b == min(wey4_velocity_a):
            wey4_velocity_min.append(b)
            timestampd_bmin.append(a)
    for a, b in zip(wey4_velocity_a, timestampd):  # 平均速度
        t = sum(wey4_velocity_a) / len(wey4_velocity_a)
        wey4_velocity_average.append(t)
        timestampd_average.append(b)
    UTM_X_max = []
    UTM_X_min = []
    timestampd_cmax = []
    timestampd_cmin = []
    UTM_X_average = []
    for a, b in zip(timestampd, UTM_X_a):  # 目标车的最大/最小X值
        if b == max(UTM_X_a):
            UTM_X_max.append(b)
            timestampd_cmax.append(a)
        if b == min(UTM_X_a):
            UTM_X_min.append(b)
            timestampd_cmin.append(a)
    for a, b in zip(UTM_X_a, timestampd):  # 目标车的平均X值
        t = sum(UTM_X_a) / len(UTM_X_a)
        UTM_X_average.append(t)
        timestampd_average.append(b)

    UTM_Y_max = []
    UTM_Y_min = []
    timestampd_dmax = []
    timestampd_dmin = []
    UTM_Y_average = []
    for a, b in zip(timestampd, UTM_Y_a):  # 目标车的最大/最小Y值
        if b == max(UTM_Y_a):
            UTM_Y_max.append(b)
            timestampd_dmax.append(a)
        if b == min(UTM_Y_a):
            UTM_Y_min.append(b)
            timestampd_dmin.append(a)
    for a, b in zip(UTM_Y_a, timestampd):  # 目标车的平均X值
        t = sum(UTM_Y_a) / len(UTM_Y_a)
        UTM_Y_average.append(t)
        timestampd_average.append(b)

    fig = plt.figure(figsize=(18, 12))  # 创建画布,绘制场景还原模型
    ax = axisartist.Subplot(fig, 111)  # 111 代表1行1列的第1个，subplot()可以用于绘制多个子图
    fig.add_axes(ax)  # 将绘图区对象添加到画布中
    ax.axis[:].set_visible(False)  # 隐藏了四周的方框
    ax.axis["x"] = ax.new_floating_axis(0, 0)
    ax.axis["x"].set_axisline_style("->", size=1.0)  # 给x坐标轴加上箭头
    ax.axis["y"] = ax.new_floating_axis(1, 0)  # 添加y坐标轴，且加上箭头
    ax.axis["y"].set_axisline_style("-|>", size=1.0)
    ax.axis["x"].set_axis_direction("top")
    ax.axis["y"].set_axis_direction("right")
    plt.xlim(-60, 60)
    plt.ylim(-60, 60)

    m = timestampd.index(timestamp_b[-1]) + 1
    s = len(ttc_b) // 2  # 报警中的一个点
    car = [
        [UTM_X_b[0], UTM_Y_b[0], timestamp_b[0], wey4_velocity_b[0], ttcd[0]],  # 报警开始时刻
        [UTM_X_b[s], UTM_Y_b[s], timestamp_b[s], wey4_velocity_b[s], ttcd[s]],  # 报警中
        [UTM_X_a[m], UTM_Y_a[m], timestampd[m], wey4_velocity_a[m], ttcd[m]],  # 报警结束时刻
        [UTM_X_c[-10], UTM_Y_c[-10], timestamp_c[-10], wey4_velocity_c[-10], ttcd[-10]]  # 报警解除之后
    ]

    for p in car:
        plt.plot([p[0] + 0.92, p[0] - 0.92, p[0] - 0.92, p[0] + 0.92, p[0] + 0.92],
                 [p[1] + 3.7, p[1] + 3.7, p[1] - 0.9, p[1] - 0.9, p[1] + 3.7], 'g')  # 目标车模型
        plt.annotate('', xy=(p[0], p[1]),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]),
                     weight="bold", color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:
            plt.text(p[0] - 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")  # 文本注释
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),  # 箭头注释
                         xytext=(p[0] - 20, p[1]),
                         weight="bold", color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            # if p[4] < 0:
            #     plt.text(p[0]-20, p[1]-2,'ttc=''%.1f'%p[4],size=6,weight="bold",color="b")     #文本注释

        else:
            plt.text(p[0] + 20, p[1] + 2, 'time=''%.1f' % p[2], size=6, weight="bold", color="b")
            plt.annotate(('velocity=''%.1f' % p[3]), xy=(p[0], p[1]),
                         xytext=(p[0] + 20, p[1]),
                         weight="bold", color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            if p[4] > 0:
                plt.text(p[0] + 20, p[1] - 2, 'ttc=''%.1f' % p[4], size=6, weight="bold", color="b")

    plt.text(50, 50, 'red car:VUT', size=8, color="r")  # 自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92, -0.92, -0.92, 0.92, 0.92], [3.6, 3.6, -1, -1, 3.6], 'r')  # 自车模型

    plt.plot([1.4, 3.9, 3.9, 1.4, 1.4], [-6, -6, -51, -51, -6], 'y:', label='cvw_warn_right')  # 右侧报警区域
    plt.plot([-1.4, -3.9, -3.9, -1.4, -1.4], [-6, -6, -51, -51, -6], 'r:', label='cvw_warn_left')  # 左侧报警区域
    plt.legend()
    plt.title('lca')
    # plt.show()
    name2 = zdhq + APP.lcmlog_dict['filename'] + 'p4'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    x = np.linspace(0, 2, 200)  # 以下为测试状态模型
    fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(2, 1, 1)  # Add a subplot to the current figure
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend()  # 开启图例

    plt.subplot(2, 1, 2)
    plt.plot(timestampd, velocitys_b, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend()  # 开启图例
    name1 = zdhq + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    x = np.linspace(0, 2, 200)  # 以下为测试状态模型
    fig, ax = plt.subplots(2, 2)  # 手动创建一个figure和四个ax对象
    plt.figure(figsize=(18, 12))  # 像素
    plt.subplot(4, 1, 1)
    plt.plot(timestampd, ttcd, color='blue', label='ttc')  # 绘制第三个子图 状态机与报警等级
    plt.xlabel('time  (s)')
    plt.ylabel('ttc(s)')
    # plt.ylim(0, 10)
    plt.legend()  # 开启图例

    plt.subplot(4, 1, 2)
    plt.plot(timestampd, state_machines_a, color='green', label='state_machine')  # 绘制第四个子图 LCA状态机与报警等级
    plt.plot(timestampd, warn_lefts_a, color='red', label='warn_left')
    plt.plot(timestampd, warn_rights_a, color='blue', label='warn_right')
    plt.xlabel('time  (s)')
    plt.ylabel('ttc(s)')
    plt.legend()  # 开启图例
    plt.subplot(4, 1, 3)
    plt.plot(timestampd, cvw_inhibit_reason_a, color='green', label='cvw_inhibit_reason')
    plt.subplots_adjust(hspace=1)
    plt.xlabel('time  (s)')
    plt.ylabel('')
    plt.ylabel('level')
    plt.legend()  # 开启图例
    # warn_d = []
    # for a,b in zip(warn,timestampd):            #筛选报警等级=1对应的最小时间与最大时间，对应的报警等级区间
    #     if timestampd.index(timestamp_b[0]) <= warn.index(a) <=timestampd.index(timestamp_b[-1]):
    #         warn_d.append(a)
    # print(warn_d)
    # if 0 in warn:                              #判断用例通过或是失败：result
    #     result4 = f'如果报警，测试用例失败'
    # else:

    if all(i == 0 for i in warn):
        if 1 in cvw_inhibit_reason_a and key[-1] == 5:
            result4 = "经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1] + " ,档位抑制； " \
                                                                       "LCA未报警，与用例预期结果一致，测试用例通过。"
        elif 2 in cvw_inhibit_reason_a and key[-1] == 5:
            result4 = "经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1] + " ,车速抑制；" \
                                                                       "LCA未报警，与用例预期结果一致，测试用例通过。"
        elif 4 in cvw_inhibit_reason_a and key[-1] == 5:
            result4 = "经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1] + " , 曲率抑制；" \
                                                                       "LCA未报警，与用例预期结果一致，测试用例通过。"
        elif 8 in cvw_inhibit_reason_a and key[-1] == 5:
            result4 = "经数据分析，抑制条件为：%0.1f" % cvw_inhibit_reason_a[-1] + " ,同方向无车抑制； " \
                                                                       "LCA未报警，与用例预期结果一致，测试用例通过。"
        else:
            if all(i != 0 for i in cvw_inhibit_reason_a):
                result4 = "LCA未报警，功能未抑制，与用例预期结果不一致，测试用例失败。"
            else:
                result4 = "LCA未报警，不存在抑制，与用例预期结果不一致，测试用例失败。"
    else:
        result4 = "LCA未报警，与用例预期结果一致，测试用例通过。"
    state_machines_b = []
    for x in state_machines:
        if x == 4 or 3:
            state_machines_b.append(x)
            if len(state_machines) == len(state_machines_b):
                result3 = "通过数据分析车辆状态为：%0.1f" % state_machines_b[0] + \
                          '，满足功能规范；'
        else:
            result3 = "通过数据分析车辆状态为：%0.1f" % state_machines_b[0] + \
                      '，不满足功能规范；。'
    if key[-1] < 0:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功；'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功；'
    else:
        if key[2] - 0.3 * key[2] <= velocitys_average[0] <= key[2] + 0.3 * key[2]:
            if key[7] - 0.3 * key[7] <= wey4_velocity_average[0] <= key[7] + 0.3 * key[7]:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[2] + 'km/h' + \
                          ",本次测试目标车平均速度为：%0.1f" % wey4_velocity_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配成功；'
            else:
                result2 = "本次测试被测车平均速度为：%0.1f" % velocitys_average[0] + 'km/h' + ",测试用例的速度为：%0.1f" % key[7] + 'km/h' + \
                          ', 经分析，测试场景匹配不成功；'
    results = result3 + result4
    result1 = "通过数据分析，测试车最大车速为：%0.1f" % max(velocitys_max) + 'km/h' + ",测试车最小车速为: %0.1f" % min(velocitys_min) + 'km/h' \
                ",测试车平均车速为：%0.1f" % \
              velocitys_average[0] + 'km/h； \n' "配合车最大车速为：%0.1f" % max(wey4_velocity_max) + 'km/h' \
            ",配合车最小车速为: %0.1f" % min(
        wey4_velocity_min) + 'km/h' + "配合车平均车速为：%0.1f" % wey4_velocity_average[0] + 'km/h； \n' \
        "两车最大横向距离为：%0.1f" % max(
        UTM_X_max) + 'm' + "两车最小横向距离为: %0.1f" % min(UTM_X_min) + 'm' \
        "两车平均横向距离为：%0.1f" % UTM_X_average[
        0] + 'm； \n'  "两车最大纵向距离为：%0.1f" % max(UTM_Y_max) + 'm' \
        ",两车最小纵向距离为: %0.1f" % min(
        UTM_Y_min) + 'm' + "两车平均纵向距离为：%0.1f" % UTM_Y_average[0] + 'm 。 \n'
    resultss = result1 + result2
    name3 = zdhq + APP.lcmlog_dict['filename'] + 'p5'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')  # 保存测试状态图片
    global mysql_status
    mysql_status = APP.word_docx(name1 + '.jpg', f'{resultss}', name2 + '.jpg', name3 + '.jpg', results)  # 生成docx文档



app = PushLcmState()
app.run_analysis()
app.state = 1
ap = PullLcmName()
ap.run_analysis()
data_name = 0

while True:
    if len(ap.name) == 0:
        pass
    elif ap.name != data_name:
        APP = ReadLcmAll()
        APP.get_lcm_dataset(ap.name)
        lookup = APP.lookup_data()
        sxx = APP.case_info_dict['key']

        if sxx[-1] == 82:
            app.state = 2
            data_name = ap.name
            BSD_yizhi(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif sxx[-1] == 81:
            app.state = 2
            data_name = ap.name
            BSD_gongneng(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif sxx[-1] == 83:
            app.state = 2
            data_name = ap.name
            BSD_xingneng(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif sxx[-1] == 1 or sxx[-1] == 2 or sxx[-1] == 3 or sxx[-1] == 4:
            app.state = 2
            data_name = ap.name
            lca_fun_I_II(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif sxx[-1] == 6:
            app.state = 2
            data_name = ap.name
            lca_active_passtive(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif sxx[-1] == 78:
            app.state = 2
            data_name = ap.name
            lca_xingneng(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif sxx[-1] == 5:
            app.state = 2
            data_name = ap.name
            lca_passtive(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        else:
            data_name = ap.name
