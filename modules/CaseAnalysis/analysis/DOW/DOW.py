import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from static.lcm import dow_debug_pb2
from static.lcm import gps_imu_info_pb2
from tools.lcm_utilities import ReadLcmAll
import mpl_toolkits.axisartist as axisartist
from tools.connect_lcm import PushLcmState
from tools.connect_lcm import PullLcmName
# from PyQt5.QtWidgets import QApplication
# app = QApplication([])
pic_path = os.path.join(os.getcwd(),'pic/')

def function(ddt):
    warn_rights = []  # 右侧报警等级
    warn_lefts = []  # 左侧报警等级
    state_machines = []  # 处于状态机的哪个状态
    ttcd = []
    velocitys = []  # 本车速度
    inhibitions = []  # 抑制条件： 0 无抑制 1 自车速度超过5kmph抑制 2车门全部闭锁 3存在关联故障
    door_status_fls = []  # 左前门状态
    door_status_rls = []  # 左后门状态
    door_status_frs = []  # 右前门状态
    door_status_rrs = []  # 右后门状态

    APP = ReadLcmAll()  # 实例化
    lcmlog_dataframe = APP.get_lcm_dataset(ddt)  # 数据包
    channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abDowToDebug")  # DOW通道数据
    dowdebug = dow_debug_pb2.DOWDebug()
    for packet in packets:
        dowdebug.ParseFromString(packet)
        warn_rights.append(dowdebug.war_right)
        warn_lefts.append(dowdebug.war_left)
        state_machines.append(dowdebug.state_machine)
        inhibitions.append(dowdebug.inhibition)
        door_status_fls.append(dowdebug.door_status_fl)
        door_status_rls.append(dowdebug.door_status_rl)
        door_status_frs.append(dowdebug.door_status_fr)
        door_status_rrs.append(dowdebug.door_status_rr)

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

    if not UTM_X:  # 判断目标车列表为空就退出程序
        print("GVT_list is empty")
        sys.exit(1)

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

    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []  # 时间同步后的目标车X
    UTM_Y_a = []  # 时间同步后的目标车Y
    wey4_velocity_a = []  # 时间同步后的目标车速度
    velocitys_a = []  # 时间同步后的自车速度
    inhibitions_a = []  # 时间同步后的抑制条件
    door_status_fl_a = []  # 时间同步后的左前门状态
    door_status_rl_a = []  # 时间同步后的左后门状态
    door_status_fr_a = []  # 时间同步后的右前门状态
    door_status_rr_a = []  # 时间同步后的右后门状态

    for i in dd:  # 时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])
        inhibitions_a.append(inhibitions[i])
        door_status_fl_a.append(door_status_fls[i])
        door_status_rl_a.append(door_status_rls[i])
        door_status_fr_a.append(door_status_frs[i])
        door_status_rr_a.append(door_status_rrs[i])

    vut_velocity = []
    for a in velocitys_a:
        b = 3.6 * a
        vut_velocity.append(b)

    for a, b, c in zip(UTM_Y_a, wey4_velocity_a, vut_velocity):  # 时间同步后的ttc
        t = (a + 4.7) / (b / 3.6 - c / 3.6)
        ttcd.append(-t)

    if UTM_X_a[0] > 0:  # 单侧第一阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a

    UTM_X_b = []  # _b为 报警侧 报警等级=1时
    UTM_Y_b = []
    warn_b = []
    ttc_b = []
    wey4_velocity_b = []
    timestamp_b = []
    UTM_X_c = []  # _c为 报警侧 报警等级!=1时
    UTM_Y_c = []
    warn_c = []
    ttc_c = []
    wey4_velocity_c = []
    timestamp_c = []

    for a, b, c, d, e, f in zip(warn, UTM_X_a, UTM_Y_a, ttcd, wey4_velocity_a, timestampd):
        if a == 1:  # 报警时的X，Y，ttc
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
        elif a == 2:
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
        else:  # 未报警的X，Y，ttc
            warn_c.append(a)
            UTM_X_c.append(b)
            UTM_Y_c.append(c)
            ttc_c.append(d)
            wey4_velocity_c.append(e)
            timestamp_c.append(f)

    wey4_velocity_max = max(wey4_velocity_a)  # 目标车的最大速度/最小速度
    wey4_velocity_min = min(wey4_velocity_a)
    timestamp_vmax = timestampd[wey4_velocity_a.index(wey4_velocity_max)]
    timestamp_vmin = timestampd[wey4_velocity_a.index(wey4_velocity_min)]
    GVT_velocity_average = sum(wey4_velocity_a) / len(wey4_velocity_a)  # 目标车的平均速度

    vut_velocity_max = max(vut_velocity)  # 自车的最大速度
    timestamp_vutmax = timestampd[vut_velocity.index(vut_velocity_max)]

    UTM_X_max = max(UTM_X_a)  # 目标车的最大/最小X值
    UTM_X_min = min(UTM_X_a)
    timestamp_xmax = timestampd[UTM_X_a.index(UTM_X_max)]
    timestamp_xmin = timestampd[UTM_X_a.index(UTM_X_min)]
    UTM_X_average = sum(UTM_X_a) / len(UTM_X_a)  # 目标车的平均X值

    UTM_Y_max = max(UTM_Y_a)  # 目标车的最大/最小Y值
    UTM_Y_min = min(UTM_Y_a)
    timestamp_ymax = timestampd[UTM_Y_a.index(UTM_Y_max)]
    timestamp_ymin = timestampd[UTM_Y_a.index(UTM_Y_min)]
    UTM_Y_average = sum(UTM_Y_a) / len(UTM_Y_a)  # 目标车的平均Y值

    s = int(len(ttc_b) // 4)  # 报警中的一个点
    m = timestampd.index(timestamp_b[-1]) + 1  # 报警解除的第一个点在时间同步后的列表中的下标

    for a in inhibitions_a:  # 抑制条件
        if a != 0:
            sign = inhibitions_a.index(a)
            number = a
            break

    warn_d = []
    if len(warn_b):
        for a, b in zip(warn, timestampd):  # 筛选报警等级对应的最小时间与最大时间，对应的报警等级区间
            if timestampd.index(timestamp_b[0]) <= warn.index(a) <= timestampd.index(timestamp_b[-1]):
                warn_d.append(a)

    if UTM_X_a[0] < 0:
        side = f'左侧'
    else:
        side = f'右侧'

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

    if len(warn_b):  # 列表warn_b不为空，有报警
        if 0 in warn_d:
            if len(warn_1) == len(warn_b):
                if all(el == 0 for el in inhibitions_a):
                    if key[-1] == 71:
                        warn_level = f'经过数据分析，DOW{side}重复报警，与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，DOW{side}重复报警，与用例预期结果不一致，测试用例失败。'
                else:
                    warn_level = f'经过数据分析，DOW{side}重复报警，有功能抑制，与用例预期结果不一致，测试用例失败。'
            else:
                warn_level = f'经过数据分析，DOW{side}重复报警，与用例预期结果不一致，测试用例失败。'
        else:
            if len(warn_1) == len(warn_b):  # 第一阶段报警
                if all(el == 0 for el in inhibitions_a):  # 不存在抑制条件的情况
                    if key[-1] == 1:  # 激活第一阶段报警
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，且报警连续，无功能抑制，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    elif key[-1] == 72:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，且报警连续，无功能抑制，' \
                                     f'目标车Y轴与被测车辆Y轴接近角度超出±30°，与用例预期结果一致，测试用例通过。'
                    elif key[-1] == 73:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，且报警连续，无功能抑制，' \
                                     f'目标车速度={wey4_velocity_a[m]}，与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，且报警连续，无功能抑制，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                elif all(el == 0 or el == 1 for el in inhibitions_a):
                    if key[-1] == 5:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，自车速度 > 5km/h功能抑制，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，自车速度 > 5km/h功能抑制，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                elif all(el == 0 or el == 2 for el in inhibitions_a):
                    if key[-1] == 5:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，车门全部闭锁功能抑制，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，车门全部闭锁功能抑制，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                elif all(el == 0 or el == 3 for el in inhibitions_a):
                    if key[-1] == 5:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，存在关联故障功能抑制，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，存在关联故障功能抑制，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                else:
                    warn_level = f'经过数据分析，激活DOW{side}第一阶段报警，有多种功能抑制，' \
                                 f'但与用例预期结果不一致，测试用例失败。'
            elif len(warn_2) == len(warn_b):  # 第二阶段报警
                if all(el == 0 for el in inhibitions_a):  # 不存在抑制条件的情况
                    if key[-1] == 2:
                        warn_level = f'经过数据分析，激活DOW{side}第二阶段报警，且报警连续，无功能抑制，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第二阶段报警，且报警连续，无功能抑制，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                else:
                    warn_level = f'经过数据分析，激活DOW{side}第二阶段报警，且报警连续，但有功能抑制，' \
                                 f'但与用例预期结果不一致，测试用例失败。'
            elif len(warn_1) < len(warn_b):
                if timestamp_b_1[0] < timestamp_b_1[-1] < timestamp_b_2[0] < timestamp_b_2[-1]:
                    if key[-1] == 3:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警跳转到第二阶段报警，且报警连续，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第一阶段报警跳转到第二阶段报警，且报警连续，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                elif timestamp_b_2[0] < timestamp_b_2[-1] < timestamp_b_1[0] < timestamp_b_1[-1]:
                    if key[-1] == 4:
                        warn_level = f'经过数据分析，激活DOW{side}第二阶段报警跳转到第一阶段报警，且报警连续，' \
                                     f'与用例预期结果一致，测试用例通过。'
                    else:
                        warn_level = f'经过数据分析，激活DOW{side}第二阶段报警跳转到第一阶段报警，且报警连续，' \
                                     f'但与用例预期结果不一致，测试用例失败。'
                else:
                    warn_level = f'经过数据分析，多次激活DOW{side}报警，且报警连续，' \
                                 f'与用例预期结果不一致，测试用例失败。'
    else:
        if key[-1] == 8:
            warn_level = f'经过数据分析，DOW未报警，与用例预期结果一致，测试用例通过。'
        else:
            warn_level = f'经过数据分析，DOW未报警，与用例预期结果不一致，测试用例失败。'

    if int(vut_velocity_max) == 0:
        VUT = f'被测车辆静止'
    else:
        VUT = f'被测车辆最大速度={round(vut_velocity_max, 1)}km/h'

    legend1 = f'real_X：真实的横向距离；\nreal_Y：真实的纵向距离；\nVUT_V：被测车辆速度；\nGVT_V：目标车辆速度；\n'
    legend2 = f'ttc：保持当前时刻的运动状态，测试车辆与目标物发生碰撞所需的时间；\n' \
              f'state_machine：状态机 Off=1 Fault=2 On=3 Passive=4 Standby=5 ' \
              f'Active=6 DOWI=7 DOWII=8；\n' \
              f'warn_left：左侧报警等级 None=0 WarnLevelI=1 WarnLevelII=2；\n' \
              f'warn_right：右侧报警等级 None=0 WarnLevelI=1 WarnLevelII=2；\n' \
              f'door_status_fl:左前车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_fr:右前车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_rl:左后车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_rr:右后车门状态 开门=0 关门=1 锁门=2；\n' \
              f'inhibition：抑制条件 无抑制=0 自车速度超过5km/h=1 车门全部闭锁=2 存在关联故障=3；\n'

    coincide1 = f'经过数据分析，{VUT}；目标车辆最大速度={round(wey4_velocity_max, 1)}km/h，' \
                f'最小速度={round(wey4_velocity_min, 1)}km/h，' \
                f'平均速度={round(GVT_velocity_average, 1)}km/h，' \
                f'real_X的最大值={round(UTM_X_max, 1)}km/h，' \
                f'real_X的最小值={round(UTM_X_min, 1)}m，' \
                f'real_X的平均值={round(UTM_X_average, 1)}m，' \
                f'real_Y的最大值={round(UTM_Y_max, 1)}m，' \
                f'real_Y的最小值={round(UTM_Y_min, 1)}m，'

    if key[-2] < 0:
        if key[-2] < UTM_X_average <= 0:
            if 1.3 * key[7] <= GVT_velocity_average <= 0.7 * key[7]:
                coincide2 = f'测试场景符合测试用例要求，场景匹配成功。'
            else:
                coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
        else:
            coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
    else:
        if 0 <= UTM_X_average < key[-2]:
            if 0.7 * key[7] <= GVT_velocity_average <= 1.3 * key[7]:
                coincide2 = f'测试场景符合测试用例要求，场景匹配成功。'
            else:
                coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
        else:
            coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'

    coincide = f'{legend1}{coincide1}{coincide2}'
    Warn_level = f'{legend2}{warn_level}'
    np.linspace(0, 2, 200)  # 以下为测试状态模型
    plt.figure(figsize=(12, 12))
    plt.subplot(2, 1, 1)
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend(fontsize=6)  # 开启图例，设置字体大小=6
    plt.subplot(2, 1, 2)
    plt.plot(timestampd, vut_velocity, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend(fontsize=6)  # 开启图例
    name1 = pic_path + APP.lcmlog_dict['filename'] + 'p1'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    fig = plt.figure(figsize=(12, 12))  # 创建画布,绘制场景还原模型
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
    car = [
        [UTM_X_c[0], UTM_Y_c[0], timestamp_c[0], wey4_velocity_c[0], ttc_c[0]],  # 报警前
        [UTM_X_b[0], UTM_Y_b[0], timestamp_b[0], wey4_velocity_b[0], ttc_b[0]],  # 报警开始时刻
        [UTM_X_b[s], UTM_Y_b[s], timestamp_b[s], wey4_velocity_b[s], ttc_b[s]],  # 报警中
        [UTM_X_a[m], UTM_Y_a[m], timestampd[m], wey4_velocity_a[m], ttcd[m]],  # 报警解除时刻
        [UTM_X_c[-1], UTM_Y_c[-1], timestamp_c[-1], wey4_velocity_c[-1], ttc_c[-1]]  # 报警解除之后
    ]

    for p in car:
        plt.plot([p[0] + 0.92, p[0] - 0.92, p[0] - 0.92, p[0] + 0.92, p[0] + 0.92],
                 [p[1] + 3.7, p[1] + 3.7, p[1] - 0.9, p[1] - 0.9, p[1] + 3.7], 'g')  # 目标车模型
        plt.annotate('', xy=(p[0], p[1] + 8),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]), color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:  # 判断注释的位置
            num = -20
        else:
            num = 20
        if p[4] >= 0:  # 当ttc>=0,作注释；当ttc<0不做注释
            plt.annotate(f'time={round(p[2], 1)} velocity={round(p[3], 1)} ttc={round(p[4], 1)}', xy=(p[0], p[1]),
                         xytext=(p[0] + num, p[1] + 1.2), color="b", size=6,  # 注释时间、目标车速度与ttc
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        else:
            plt.annotate(f'time={round(p[2], 1)} velocity={round(p[3], 1)}', xy=(p[0], p[1]),  # 注释时间与目标车速度
                         xytext=(p[0] + num, p[1] + 1.2), color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))

    plt.text(50, 50, 'red car:VUT', size=8, color="r")  # 自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92, -0.92, -0.92, 0.92, 0.92], [3.6, 3.6, -1, -1, 3.6], 'r')  # 自车模型
    plt.plot([-0.92, -3.42, -3.42, -0.92, -0.92], [1.315, 1.315, -51, -51, 1.315], 'r:')  # 左侧报警区域
    plt.plot([0.92, 3.42, 3.42, 0.92, 0.92], [1.315, 1.315, -51, -51, 1.315], 'b:')  # 右侧报警区域
    plt.legend()
    plt.title('dow')
    name2 = pic_path + APP.lcmlog_dict['filename'] + 'p2'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    np.linspace(0, 2, 200)  # 以下为测试状态模型
    plt.figure(figsize=(18, 18))
    plt.subplot(5, 1, 1)
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.annotate(f'real_Y_max={round(UTM_Y_max, 1)}', xy=(timestamp_ymax, UTM_Y_max),  # 目标车最大Y值
                 xytext=(timestamp_ymax, UTM_Y_max - 3), color="g", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.annotate(f'real_Y_min={round(UTM_Y_min, 1)}', xy=(timestamp_ymin, UTM_Y_min),  # 目标车最小Y值
                 xytext=(timestamp_ymin, UTM_Y_min + 3), color="g", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.annotate(f'real_X_max={round(UTM_X_max, 1)}', xy=(timestamp_xmax, UTM_X_max),  # 目标车最大X值
                 xytext=(timestamp_xmax, UTM_X_max - 3), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'real_X_min={round(UTM_X_min, 1)}', xy=(timestamp_xmin, UTM_X_min),  # 目标车最小X值
                 xytext=(timestamp_xmin, UTM_X_min - 3), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(1, -10, f'real_X_avg={round(UTM_X_average, 1)}'
                     f'\nreal_Y_avg={round(UTM_Y_average, 1)}', size=6, color="b")  # 平均XY值
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend(fontsize=8)  # 开启图例，设置字体大小=6
    plt.subplot(5, 1, 2)
    plt.plot(timestampd, vut_velocity, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    if round(vut_velocity_max, 1) > 0:
        plt.annotate(f'VUT_V_max={round(vut_velocity_max, 1)}', xy=(timestamp_vutmax, vut_velocity_max),  # 自车最大速度
                     xytext=(timestamp_vutmax, vut_velocity_max * 0.9), color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'GVT_V_max={round(wey4_velocity_max, 1)}', xy=(timestamp_vmax, wey4_velocity_max),  # 注释目标车最大速度
                 xytext=(timestamp_vmax, wey4_velocity_max * 0.9), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'GVT_V_min={round(wey4_velocity_min, 1)}', xy=(timestamp_vmin, wey4_velocity_min),  # 注释目标车最小速度
                 xytext=(timestamp_vmin, wey4_velocity_min * 0.9), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(int(timestampd[-1] * 0.9), int(wey4_velocity_max / 2), f'GVT_V_avg={round(GVT_velocity_average, 1)}',
             size=6, color="b")  # 注释平均速度
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 3)
    plt.plot(timestampd, ttcd, color='yellow', label='ttc')  # 绘制第三个子图 DOW状态机与报警等级
    # plt.annotate(f'ttc={round(ttc_b[0],1)}', xy=(timestamp_b[0], ttc_b[0]),    #注释报警开始时刻的ttc
    #                  xytext=(timestamp_b[0] , ttc_b[0] + 2),color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.plot(timestampd, state_machines_a, color='green', label='state_machine')  # DOW状态机与报警等级
    plt.plot(timestampd, warn_lefts_a, color='red', label='warn_left')
    plt.plot(timestampd, warn_rights_a, color='blue', label='warn_right')
    plt.annotate(f'time={round(timestamp_b[0], 1)} start_warn', xy=(timestamp_b[0], warn_b[0]),  # 注释报警开始时刻
                 xytext=(timestamp_b[0], warn_b[0] + 1), color="r", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="r"))
    plt.annotate(f'time={round(timestampd[m], 1)} end_warn', xy=(timestampd[m], warn[m]),  # 注释报警解除时刻
                 xytext=(timestampd[m], warn[m] + 1), color="r", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="r"))
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 4)
    plt.plot(timestampd, door_status_fl_a, color='green', label='door_status_fl')  # 绘制第四个子图 DOW车门状态
    plt.plot(timestampd, door_status_rl_a, color='red', label='door_status_rl')
    plt.plot(timestampd, door_status_fr_a, color='blue', label='door_status_fr')
    plt.plot(timestampd, door_status_rr_a, color='yellow', label='door_status_rr')
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 5)
    plt.plot(timestampd, inhibitions_a, color='green', label='inhibition')  # 绘制第五个子图 抑制条件
    if not all(el == 0 for el in inhibitions_a):
        plt.annotate(f'time={round(timestampd[sign], 1)}', xy=(timestampd[sign], number),
                     xytext=(timestampd[sign], number * 0.9), color="g", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplots_adjust(hspace=0.5)  # 调整子图纵向间隔
    name3 = pic_path + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')  # 保存测试状态图片
    global mysql_status
    mysql_status = APP.word_docx(f'{name1}.jpg', f'{coincide}', f'{name2}.jpg', f'{name3}.jpg', f'{Warn_level}')  # 生成docx文档


def standby_passive(ddt):
    warn_rights = []  # 右侧报警等级
    warn_lefts = []  # 左侧报警等级
    state_machines = []  # 处于状态机的哪个状态
    ttcd = []
    velocitys = []  # 本车速度
    inhibitions = []  # 抑制条件： 0 无抑制 1 自车速度超过5kmph抑制 2车门全部闭锁 3存在关联故障
    door_status_fls = []  # 左前门状态
    door_status_rls = []  # 左后门状态
    door_status_frs = []  # 右前门状态
    door_status_rrs = []  # 右后门状态

    if __name__ == '__main__':
        APP = ReadLcmAll()  # 实例化
        lcmlog_dataframe = APP.get_lcm_dataset(ddt)  # 数据包
        channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abDowToDebug")  # DOW通道数据
        dowdebug = dow_debug_pb2.DOWDebug()
        for packet in packets:
            dowdebug.ParseFromString(packet)
            warn_rights.append(dowdebug.war_right)
            warn_lefts.append(dowdebug.war_left)
            state_machines.append(dowdebug.state_machine)
            inhibitions.append(dowdebug.inhibition)
            door_status_fls.append(dowdebug.door_status_fl)
            door_status_rls.append(dowdebug.door_status_rl)
            door_status_frs.append(dowdebug.door_status_fr)
            door_status_rrs.append(dowdebug.door_status_rr)

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

    if not UTM_X:  # 判断目标车列表为空就退出程序
        sys.exit(1)

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

    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []  # 时间同步后的目标车X
    UTM_Y_a = []  # 时间同步后的目标车Y
    wey4_velocity_a = []  # 时间同步后的目标车速度
    velocitys_a = []  # 时间同步后的自车速度
    inhibitions_a = []  # 时间同步后的抑制条件
    door_status_fl_a = []  # 时间同步后的左前门状态
    door_status_rl_a = []  # 时间同步后的左后门状态
    door_status_fr_a = []  # 时间同步后的右前门状态
    door_status_rr_a = []  # 时间同步后的右后门状态

    for i in dd:  # 时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])
        inhibitions_a.append(inhibitions[i])
        door_status_fl_a.append(door_status_fls[i])
        door_status_rl_a.append(door_status_rls[i])
        door_status_fr_a.append(door_status_frs[i])
        door_status_rr_a.append(door_status_rrs[i])

    vut_velocity = []
    for a in velocitys_a:
        b = 3.6 * a
        vut_velocity.append(b)

    for a, b, c in zip(UTM_Y_a, wey4_velocity_a, vut_velocity):  # 时间同步后的ttc
        t = (a + 4.7) / (b / 3.6 - c / 3.6)
        ttcd.append(-t)

    if UTM_X_a[0] < 0:  # X值<0 目标车在左侧
        warn = warn_lefts_a
    else:
        warn = warn_rights_a

    wey4_velocity_max = max(wey4_velocity_a)  # 目标车的最大速度/最小速度
    wey4_velocity_min = min(wey4_velocity_a)
    timestamp_vmax = timestampd[wey4_velocity_a.index(wey4_velocity_max)]
    timestamp_vmin = timestampd[wey4_velocity_a.index(wey4_velocity_min)]
    GVT_velocity_average = sum(wey4_velocity_a) / len(wey4_velocity_a)  # 目标车的平均速度

    vut_velocity_max = max(vut_velocity)  # 自车的最大速度
    timestamp_vutmax = timestampd[vut_velocity.index(vut_velocity_max)]

    UTM_X_max = max(UTM_X_a)  # 目标车的最大/最小X值
    UTM_X_min = min(UTM_X_a)
    timestamp_xmax = timestampd[UTM_X_a.index(UTM_X_max)]
    timestamp_xmin = timestampd[UTM_X_a.index(UTM_X_min)]
    UTM_X_average = sum(UTM_X_a) / len(UTM_X_a)  # 目标车的平均X值

    UTM_Y_max = max(UTM_Y_a)  # 目标车的最大/最小Y值
    UTM_Y_min = min(UTM_Y_a)
    timestamp_ymax = timestampd[UTM_Y_a.index(UTM_Y_max)]
    timestamp_ymin = timestampd[UTM_Y_a.index(UTM_Y_min)]
    UTM_Y_average = sum(UTM_Y_a) / len(UTM_Y_a)  # 目标车的平均Y值

    for a in inhibitions_a:  # 抑制条件
        if a != 0:
            sign = inhibitions_a.index(a)
            number = a
            break

    if all(el == 0 for el in warn):
        if all(el == 1 for el in inhibitions_a):
            if key[-1] == 6:
                warn_level = f'经过数据分析，DOW未激活，自车速度 > 5km/h功能抑制，与用例预期结果一致，测试用例通过。'
            else:
                warn_level = f'经过数据分析，DOW未激活，自车速度 > 5km/h功能抑制，与用例预期结果不一致，测试用例失败。'
        elif all(el == 2 for el in inhibitions_a):
            if key[-1] == 6:
                warn_level = f'经过数据分析，DOW未激活，车门全部闭锁功能抑制，与用例预期结果一致，测试用例通过。'
            else:
                warn_level = f'经过数据分析，DOW未激活，车门全部闭锁功能抑制，与用例预期结果不一致，测试用例失败。'
        elif all(el == 3 for el in inhibitions_a):
            if key[-1] == 6:
                warn_level = f'经过数据分析，DOW未激活，存在关联故障功能抑制，与用例预期结果一致，测试用例通过。'
            else:
                warn_level = f'经过数据分析，DOW未激活，存在关联故障功能抑制，与用例预期结果不一致，测试用例失败。'
        elif all(el == 0 for el in inhibitions_a):
            warn_level = f'经过数据分析，DOW未激活，功能未抑制，与用例预期结果不一致，测试用例失败。'
        else:
            warn_level = f'经过数据分析，DOW未激活，有多种功能抑制，与用例预期结果不一致，测试用例失败。'
    else:
        warn_level = f'经过数据分析，DOW功能激活，与用例预期结果不一致，测试用例失败。'

    if int(vut_velocity_max) == 0:
        VUT = f'被测车辆静止'
    else:
        VUT = f'被测车辆最大速度={round(vut_velocity_max, 1)}km/h'

    legend1 = f'real_X：真实的横向距离；\nreal_Y：真实的纵向距离；\nVUT_V：被测车辆速度；\nGVT_V：目标车辆速度；\n'
    legend2 = f'ttc：保持当前时刻的运动状态，测试车辆与目标物发生碰撞所需的时间；\n' \
              f'state_machine：状态机 Off=1 Fault=2 On=3 Passive=4 Standby=5 ' \
              f'Active=6 DOWI=7 DOWII=8；\n' \
              f'warn_left：左侧报警等级 None=0 WarnLevelI=1 WarnLevelII=2；\n' \
              f'warn_right：右侧报警等级 None=0 WarnLevelI=1 WarnLevelII=2；\n' \
              f'door_status_fl:左前车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_fr:右前车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_rl:左后车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_rr:右后车门状态 开门=0 关门=1 锁门=2；\n' \
              f'inhibition：抑制条件 无抑制=0 自车速度超过5km/h=1 车门全部闭锁=2 存在关联故障=3；\n'

    coincide1 = f'经过数据分析，{VUT}；目标车辆最大速度={round(wey4_velocity_max, 1)}km/h，' \
                f'最小速度={round(wey4_velocity_min, 1)}km/h，' \
                f'平均速度={round(GVT_velocity_average, 1)}km/h，' \
                f'real_X的最大值={round(UTM_X_max, 1)}m，' \
                f'real_X的最小值={round(UTM_X_min, 1)}m，' \
                f'real_X的平均值={round(UTM_X_average, 1)}m，' \
                f'real_Y的最大值={round(UTM_Y_max, 1)}m，' \
                f'real_Y的最小值={round(UTM_Y_min, 1)}m，'

    if key[-2] < 0:
        if key[-2] < UTM_X_average <= 0:
            if 1.3 * key[7] <= GVT_velocity_average <= 0.7 * key[7]:
                coincide2 = f'测试场景符合测试用例要求，场景匹配成功。'
            else:
                coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
        else:
            coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
    else:
        if 0 <= UTM_X_average < key[-2]:
            if 0.7 * key[7] <= GVT_velocity_average <= 1.3 * key[7]:
                coincide2 = f'测试场景符合测试用例要求，场景匹配成功。'
            else:
                coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
        else:
            coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'

    coincide = f'{legend1}{coincide1}{coincide2}'
    Warn_level = f'{legend2}{warn_level}'
    np.linspace(0, 2, 200)  # 以下为测试状态模型
    plt.figure(figsize=(12, 12))
    plt.subplot(2, 1, 1)
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend(fontsize=6)  # 开启图例，设置字体大小=6
    plt.subplot(2, 1, 2)
    plt.plot(timestampd, vut_velocity, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend(fontsize=6)  # 开启图例
    name1 = pic_path + APP.lcmlog_dict['filename'] + 'p1'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    fig = plt.figure(figsize=(12, 12))  # 创建画布,绘制场景还原模型
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
    s1 = int(len(UTM_X_a) // 4)
    s2 = int(len(UTM_X_a) // 2)
    s3 = int(len(UTM_X_a) * 3 // 4)
    car = [
        [UTM_X_a[0], UTM_Y_a[0], timestampd[0], wey4_velocity_a[0], ttcd[0]],  # 开始时刻
        [UTM_X_a[s1], UTM_Y_a[s1], timestampd[s1], wey4_velocity_a[s1], ttcd[s1]],  # 四分之一时刻
        [UTM_X_a[s2], UTM_Y_a[s2], timestampd[s2], wey4_velocity_a[s2], ttcd[s2]],  # 二分之一时刻
        [UTM_X_a[s3], UTM_Y_a[s3], timestampd[s3], wey4_velocity_a[s3], ttcd[s3]],  # 四分之三时刻
        [UTM_X_a[-1], UTM_Y_a[-1], timestampd[-1], wey4_velocity_a[-1], ttcd[-1]],  # 结束时刻
    ]
    for p in car:
        plt.plot([p[0] + 0.92, p[0] - 0.92, p[0] - 0.92, p[0] + 0.92, p[0] + 0.92],
                 [p[1] + 3.7, p[1] + 3.7, p[1] - 0.9, p[1] - 0.9, p[1] + 3.7], 'g')  # 目标车模型
        plt.annotate('', xy=(p[0], p[1] + 8),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]), color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:  # 判断注释的位置
            num = -20
        else:
            num = 20
        if p[4] >= 0:  # 当ttc>=0,作注释；当ttc<0不做注释
            plt.annotate(f'time={round(p[2], 1)} velocity={round(p[3], 1)} ttc={round(p[4], 1)}', xy=(p[0], p[1]),
                         xytext=(p[0] + num, p[1] + 1.2), color="b", size=6,  # 注释时间、目标车速度与ttc
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        else:
            plt.annotate(f'time={round(p[2], 1)} velocity={round(p[3], 1)}', xy=(p[0], p[1]),  # 注释时间与目标车速度
                         xytext=(p[0] + num, p[1] + 1.2), color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(50, 50, 'red car:VUT', size=8, color="r")  # 自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92, -0.92, -0.92, 0.92, 0.92], [3.6, 3.6, -1, -1, 3.6], 'r')  # 自车模型
    plt.plot([-0.92, -3.42, -3.42, -0.92, -0.92], [1.315, 1.315, -51, -51, 1.315], 'r:')  # 左侧报警区域
    plt.plot([0.92, 3.42, 3.42, 0.92, 0.92], [1.315, 1.315, -51, -51, 1.315], 'b:')  # 右侧报警区域
    plt.legend()
    plt.title('dow')
    name2 = pic_path + APP.lcmlog_dict['filename'] + 'p2'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    np.linspace(0, 2, 200)  # 以下为测试状态模型
    plt.figure(figsize=(18, 18))
    plt.subplot(5, 1, 1)
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.annotate(f'real_Y_max={round(UTM_Y_max, 1)}', xy=(timestamp_ymax, UTM_Y_max),  # 目标车最大Y值
                 xytext=(timestamp_ymax, UTM_Y_max - 10), color="g", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.annotate(f'real_Y_min={round(UTM_Y_min, 1)}', xy=(timestamp_ymin, UTM_Y_min),  # 目标车最小Y值
                 xytext=(timestamp_ymin, UTM_Y_min + 10), color="g", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.annotate(f'real_X_max={round(UTM_X_max, 1)}', xy=(timestamp_xmax, UTM_X_max),  # 目标车最大X值
                 xytext=(timestamp_xmax, UTM_X_max - 5), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'real_X_min={round(UTM_X_min, 1)}', xy=(timestamp_xmin, UTM_X_min),  # 目标车最小X值
                 xytext=(timestamp_xmin, UTM_X_min - 5), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(1, -10, f'real_X_avg={round(UTM_X_average, 1)}'
                     f'\nreal_Y_avg={round(UTM_Y_average, 1)}', size=6, color="b")  # 平均XY值
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend(fontsize=8)  # 开启图例，设置字体大小=6
    plt.subplot(5, 1, 2)
    plt.plot(timestampd, vut_velocity, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    plt.annotate(f'GVT_V_max={round(wey4_velocity_max, 1)}', xy=(timestamp_vmax, wey4_velocity_max),  # 注释目标车最大速度
                 xytext=(timestamp_vmax, 0.9 * wey4_velocity_max), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'GVT_V_min={round(wey4_velocity_min, 1)}', xy=(timestamp_vmin, wey4_velocity_min),  # 注释目标车最小速度
                 xytext=(timestamp_vmin, 0.9 * wey4_velocity_min), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(int(timestampd[-1]) * 0.9, int(wey4_velocity_max) / 2, f'GVT_V_avg={round(GVT_velocity_average, 1)}',
             size=6, color="b")  # 注释平均速度
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 3)  # 绘制第三个子图
    plt.plot(timestampd, ttcd, color='y', label='ttc')  # ttc
    plt.plot(timestampd, state_machines_a, color='green', label='state_machine')  # DOW状态机与报警等级
    plt.plot(timestampd, warn_lefts_a, color='red', label='warn_left')
    plt.plot(timestampd, warn_rights_a, color='blue', label='warn_right')
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 4)
    plt.plot(timestampd, door_status_fl_a, color='green', label='door_status_fl')  # 绘制第四个子图 DOW车门状态
    plt.plot(timestampd, door_status_rl_a, color='red', label='door_status_rl')
    plt.plot(timestampd, door_status_fr_a, color='blue', label='door_status_fr')
    plt.plot(timestampd, door_status_rr_a, color='yellow', label='door_status_rr')
    plt.xlabel('time  (s)')
    plt.ylabel('door_status')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 5)
    plt.plot(timestampd, inhibitions_a, color='green', label='inhibition')  # 绘制第五个子图 抑制条件
    # if not all(el==0 for el in inhibitions_a):
    #     plt.annotate(f'time={round(timestampd[sign], 1)}', xy=(timestampd[sign], number),  # 目标车最大Y值
    #                  xytext=(timestampd[sign], number * 0.9), color="g", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplots_adjust(hspace=0.5)  # 调整子图纵向间隔
    name3 = pic_path + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')  # 保存测试状态图片
    global mysql_status
    mysql_status = APP.word_docx(f'{name1}.jpg', f'{coincide}', f'{name2}.jpg', f'{name3}.jpg', f'{Warn_level}')  # 生成docx文档


def performance(ddt):
    warn_rights = []  # 右侧报警等级
    warn_lefts = []  # 左侧报警等级
    state_machines = []  # 处于状态机的哪个状态
    ttcd = []
    velocitys = []  # 本车速度
    inhibitions = []  # 抑制条件： 0 无抑制 1 自车速度超过5kmph抑制 2车门全部闭锁 3存在关联故障
    door_status_fls = []  # 左前门状态
    door_status_rls = []  # 左后门状态
    door_status_frs = []  # 右前门状态
    door_status_rrs = []  # 右后门状态
    if __name__ == '__main__':
        APP = ReadLcmAll()  # 实例化
        lcmlog_dataframe = APP.get_lcm_dataset(ddt)  # 数据包
        channel_starting_time, timestamps, packets = APP.unpack_packets(lcmlog_dataframe, "abDowToDebug")  # DOW通道数据
        dowdebug = dow_debug_pb2.DOWDebug()
        for packet in packets:
            dowdebug.ParseFromString(packet)
            warn_rights.append(dowdebug.war_right)
            warn_lefts.append(dowdebug.war_left)
            state_machines.append(dowdebug.state_machine)
            inhibitions.append(dowdebug.inhibition)
            door_status_fls.append(dowdebug.door_status_fl)
            door_status_rls.append(dowdebug.door_status_rl)
            door_status_frs.append(dowdebug.door_status_fr)
            door_status_rrs.append(dowdebug.door_status_rr)

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

    if not UTM_X:  # 判断目标车列表为空就退出程序
        sys.exit(1)

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

    warn_lefts_a = []
    warn_rights_a = []
    state_machines_a = []
    UTM_X_a = []  # 时间同步后的目标车X
    UTM_Y_a = []  # 时间同步后的目标车Y
    wey4_velocity_a = []  # 时间同步后的目标车速度
    velocitys_a = []  # 时间同步后的自车速度
    inhibitions_a = []  # 时间同步后的抑制条件
    door_status_fl_a = []  # 时间同步后的左前门状态
    door_status_rl_a = []  # 时间同步后的左后门状态
    door_status_fr_a = []  # 时间同步后的右前门状态
    door_status_rr_a = []  # 时间同步后的右后门状态

    for i in dd:  # 时间同步
        warn_lefts_a.append(warn_lefts[i])
        warn_rights_a.append(warn_rights[i])
        state_machines_a.append(state_machines[i])
        velocitys_a.append(velocitys[i])
        UTM_X_a.append(UTM_X[i])
        UTM_Y_a.append(UTM_Y[i])
        wey4_velocity_a.append(wey4_velocity[i])
        inhibitions_a.append(inhibitions[i])
        door_status_fl_a.append(door_status_fls[i])
        door_status_rl_a.append(door_status_rls[i])
        door_status_fr_a.append(door_status_frs[i])
        door_status_rr_a.append(door_status_rrs[i])

    vut_velocity = []
    for a in velocitys_a:
        b = 3.6 * a
        vut_velocity.append(b)

    for a, b, c in zip(UTM_Y_a, wey4_velocity_a, vut_velocity):  # 时间同步后的ttc
        t = (a + 4.7) / (b / 3.6 - c / 3.6)
        ttcd.append(-t)

    if UTM_X_a[0] > 0:  # 单侧第一阶段报警
        warn = warn_rights_a
    else:
        warn = warn_lefts_a

    UTM_X_b = []  # _b为 报警侧 报警等级=1时
    UTM_Y_b = []
    warn_b = []
    ttc_b = []
    wey4_velocity_b = []
    timestamp_b = []
    UTM_X_c = []  # _c为 报警侧 报警等级!=1时
    UTM_Y_c = []
    warn_c = []
    ttc_c = []
    wey4_velocity_c = []
    timestamp_c = []

    for a, b, c, d, e, f in zip(warn, UTM_X_a, UTM_Y_a, ttcd, wey4_velocity_a, timestampd):
        if a == 1:  # 报警时的X，Y，ttc
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
        elif a == 2:
            warn_b.append(a)
            UTM_X_b.append(b)
            UTM_Y_b.append(c)
            ttc_b.append(d)
            wey4_velocity_b.append(e)
            timestamp_b.append(f)
        else:  # 未报警的X，Y，ttc
            warn_c.append(a)
            UTM_X_c.append(b)
            UTM_Y_c.append(c)
            ttc_c.append(d)
            wey4_velocity_c.append(e)
            timestamp_c.append(f)

    wey4_velocity_max = max(wey4_velocity_a)  # 目标车的最大速度/最小速度
    wey4_velocity_min = min(wey4_velocity_a)
    timestamp_vmax = timestampd[wey4_velocity_a.index(wey4_velocity_max)]
    timestamp_vmin = timestampd[wey4_velocity_a.index(wey4_velocity_min)]
    GVT_velocity_average = sum(wey4_velocity_a) / len(wey4_velocity_a)  # 目标车的平均速度

    vut_velocity_max = max(vut_velocity)  # 自车的最大速度
    timestamp_vutmax = timestampd[vut_velocity.index(vut_velocity_max)]

    UTM_X_max = max(UTM_X_a)  # 目标车的最大/最小X值
    UTM_X_min = min(UTM_X_a)
    timestamp_xmax = timestampd[UTM_X_a.index(UTM_X_max)]
    timestamp_xmin = timestampd[UTM_X_a.index(UTM_X_min)]
    UTM_X_average = sum(UTM_X_a) / len(UTM_X_a)  # 目标车的平均X值

    UTM_Y_max = max(UTM_Y_a)  # 目标车的最大/最小Y值
    UTM_Y_min = min(UTM_Y_a)
    timestamp_ymax = timestampd[UTM_Y_a.index(UTM_Y_max)]
    timestamp_ymin = timestampd[UTM_Y_a.index(UTM_Y_min)]
    UTM_Y_average = sum(UTM_Y_a) / len(UTM_Y_a)  # 目标车的平均Y值

    for a in inhibitions_a:  # 抑制条件
        if a != 0:
            sign = inhibitions_a.index(a)
            number = a
            break

    warn_d = []
    if len(warn_b):
        for a, b in zip(warn, timestampd):  # 筛选报警等级对应的最小时间与最大时间，对应的报警等级区间
            if timestampd.index(timestamp_b[0]) <= warn.index(a) <= timestampd.index(timestamp_b[-1]):
                warn_d.append(a)

    if UTM_X_a[0] < 0:
        side = f'左侧'
        number0 = 1.84
        number1 = -2.8
        number2 = -2.2
    else:
        side = f'右侧'
        number0 = -1.84
        number1 = 2.2
        number2 = 2.8

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

    if len(warn_b):  # 列表warn_b不为空，有报警
        if 0 in warn_d:
            warn_level = f'经过数据分析，DOW{side}重复报警，与用例预期结果不一致，测试用例失败。'
        else:
            if key[-1] == 11:
                if 2.5 <= ttc_b[0] <= 3.5 and -0.8 <= UTM_Y_b[-1] - 2.215 <= 0.8 and -0.8 <= UTM_Y_b[0] + 54.7 <= 0.8:
                    warn_level = f'经过数据分析，DOW{side}激活报警，报警开始时刻ttc={round(ttc_b[0], 1)}s，' \
                                 f'目标车到被测车辆后保险杠距离={round(UTM_Y_b[0] + 4.7, 1)}m，' \
                                 f'报警解除时刻目标车到被测车辆后视镜距离={round(UTM_Y_b[-1] - 2.215, 1)}m，' \
                                 f'与用例预期结果一致，DOW{side}报警区域纵向为后保险杠后方50m到后视镜，' \
                                 f'激活条件：目标车任何部位进入报警区域，测试用例通过。'
                else:
                    warn_level = f'经过数据分析，与用例预期结果不一致，测试用例失败。'
            elif key[-1] == 12:
                if 2.5 <= ttc_b[0] <= 3.5 and -0.8 <= UTM_X_b[0] <= 0.8:
                    warn_level = f'经过数据分析，DOW{side}激活报警，报警开始时刻ttc={round(ttc_b[0], 1)}s，' \
                                 f'目标车到被测车辆横向距离={round(UTM_X_b[0], 1)}m，' \
                                 f'与用例预期结果一致，DOW{side}报警区域横向内侧为车身{side}最外缘，' \
                                 f'激活条件：目标车任何部位位于车身{side}最外缘{side}，测试用例通过。'
                else:
                    warn_level = f'经过数据分析，与用例预期结果不一致，测试用例失败。'
            elif key[-1] == 13:
                if 2.5 <= ttc_b[0] <= 3.5 and number1 <= UTM_X_b[-1] + number0 <= number2:
                    warn_level = f'经过数据分析，DOW{side}激活报警，报警开始时刻ttc={round(ttc_b[0], 1)}s，' \
                                 f'报警解除时刻目标车到被测车辆横向距离={round(UTM_X_b[-1] + number, 1)}m，' \
                                 f'与用例预期结果一致，DOW{side}报警区域横向外侧为车身{side}最外缘向外扩展2.5m，' \
                                 f'激活条件：目标车任何部位位于车身{side}最外缘向外扩展2.5m{side}，测试用例通过。'
                else:
                    warn_level = f'经过数据分析，与用例预期结果不一致，测试用例失败。'
    else:
        warn_level = f'经过数据分析，DOW未报警，与用例预期结果不一致，测试用例失败。'

    if int(vut_velocity_max) == 0:
        VUT = f'被测车辆静止'
    else:
        VUT = f'被测车辆最大速度={round(vut_velocity_max, 1)}km/h'

    legend1 = f'real_X：真实的横向距离；\nreal_Y：真实的纵向距离；\nVUT_V：被测车辆速度；\nGVT_V：目标车辆速度；\n'
    legend2 = f'ttc：保持当前时刻的运动状态，测试车辆与目标物发生碰撞所需的时间；\n' \
              f'state_machine：状态机 Off=1 Fault=2 On=3 Passive=4 Standby=5 ' \
              f'Active=6 DOWI=7 DOWII=8；\n' \
              f'warn_left：左侧报警等级 None=0 WarnLevelI=1 WarnLevelII=2；\n' \
              f'warn_right：右侧报警等级 None=0 WarnLevelI=1 WarnLevelII=2；\n' \
              f'door_status_fl:左前车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_fr:右前车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_rl:左后车门状态 开门=0 关门=1 锁门=2；\n' \
              f'door_status_rr:右后车门状态 开门=0 关门=1 锁门=2；\n' \
              f'inhibition：抑制条件 无抑制=0 自车速度超过5km/h=1 车门全部闭锁=2 存在关联故障=3；\n'

    coincide1 = f'经过数据分析，{VUT}；' \
                f'目标车辆最大速度={round(wey4_velocity_max, 1)}km/h，' \
                f'最小速度={round(wey4_velocity_min, 1)}km/h，' \
                f'平均速度={round(GVT_velocity_average, 1)}km/h，' \
                f'real_X的最大值={round(UTM_X_max, 1)}m，' \
                f'real_X的最小值={round(UTM_X_min, 1)}m，' \
                f'real_X的平均值={round(UTM_X_average, 1)}m，' \
                f'real_Y的最大值={round(UTM_Y_max, 1)}m，' \
                f'real_Y的最小值={round(UTM_Y_min, 1)}m，'

    if key[-1] < 0:
        if key[-1] < UTM_X_average < 0:
            if 1.3 * key[7] <= GVT_velocity_average <= 0.7 * key[7]:
                coincide2 = f'测试场景符合测试用例要求，场景匹配成功。'
            else:
                coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
        else:
            coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
    else:
        if 0 < UTM_X_average < key[-1]:
            if 0.7 * key[7] <= GVT_velocity_average <= 1.3 * key[7]:
                coincide2 = f'测试场景符合测试用例要求，场景匹配成功。'
            else:
                coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'
        else:
            coincide2 = f'测试场景不符合测试用例要求，场景匹配失败。'

    coincide = f'{legend1}{coincide1}{coincide2}'
    Warn_level = f'{legend2}{warn_level}'
    np.linspace(0, 2, 200)  # 以下为测试状态模型
    plt.figure(figsize=(12, 12))
    plt.subplot(2, 1, 1)
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend(fontsize=6)  # 开启图例，设置字体大小=6
    plt.subplot(2, 1, 2)
    plt.plot(timestampd, vut_velocity, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend(fontsize=6)  # 开启图例
    name1 = pic_path + APP.lcmlog_dict['filename'] + 'p1'
    plt.savefig(name1 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    fig = plt.figure(figsize=(12, 12))  # 创建画布,绘制场景还原模型
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
    s = int(len(ttc_b) // 4)  # 报警中的一个点
    m = timestampd.index(timestamp_b[-1]) + 1  # 报警解除的第一个点在时间同步后的列表中的下标
    car = [
        [UTM_X_c[0], UTM_Y_c[0], timestamp_c[0], wey4_velocity_c[0], ttc_c[0]],  # 报警前
        [UTM_X_b[0], UTM_Y_b[0], timestamp_b[0], wey4_velocity_b[0], ttc_b[0]],  # 报警开始时刻
        [UTM_X_b[s], UTM_Y_b[s], timestamp_b[s], wey4_velocity_b[s], ttc_b[s]],  # 报警中
        [UTM_X_a[m], UTM_Y_a[m], timestampd[m], wey4_velocity_a[m], ttcd[m]],  # 报警解除时刻
        [UTM_X_c[-1], UTM_Y_c[-1], timestamp_c[-1], wey4_velocity_c[-1], ttc_c[-1]]  # 报警解除之后
    ]

    for p in car:
        plt.plot([p[0] + 0.92, p[0] - 0.92, p[0] - 0.92, p[0] + 0.92, p[0] + 0.92],
                 [p[1] + 3.7, p[1] + 3.7, p[1] - 0.9, p[1] - 0.9, p[1] + 3.7], 'g')  # 目标车模型
        plt.annotate('', xy=(p[0], p[1] + 8),  # 小车黑色箭头表示前进方向
                     xytext=(p[0], p[1]), color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="black"))
        if p[0] < 0:  # 判断注释的位置
            num = -20
        else:
            num = 20
        if p[4] >= 0:  # 当ttc>=0,作注释；当ttc<0不做注释
            plt.annotate(f'time={round(p[2], 1)} velocity={round(p[3], 1)} ttc={round(p[4], 1)}', xy=(p[0], p[1]),
                         xytext=(p[0] + num, p[1] + 1.2), color="b", size=6,  # 注释时间、目标车速度与ttc
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        else:
            plt.annotate(f'time={round(p[2], 1)} velocity={round(p[3], 1)}', xy=(p[0], p[1]),  # 注释时间与目标车速度
                         xytext=(p[0] + num, p[1] + 1.2), color="b", size=6,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))

    plt.text(50, 50, 'red car:VUT', size=8, color="r")  # 自车与目标车注释
    plt.text(50, 46, 'green car:GVT', size=8, color="g")
    plt.plot([0.92, -0.92, -0.92, 0.92, 0.92], [3.6, 3.6, -1, -1, 3.6], 'r')  # 自车模型
    plt.plot([-0.92, -3.42, -3.42, -0.92, -0.92], [1.315, 1.315, -51, -51, 1.315], 'r:')  # 左侧报警区域
    plt.plot([0.92, 3.42, 3.42, 0.92, 0.92], [1.315, 1.315, -51, -51, 1.315], 'b:')  # 右侧报警区域
    plt.legend()
    plt.title('dow')
    name2 = pic_path + APP.lcmlog_dict['filename'] + 'p2'
    plt.savefig(name2 + '.jpg', bbox_inches='tight')  # 保存场景还原图片

    np.linspace(0, 2, 200)  # 以下为测试状态模型
    plt.figure(figsize=(18, 18))
    plt.subplot(5, 1, 1)
    plt.plot(timestampd, UTM_X_a, color='blue', label='real_X')  # 绘制第一个子图 目标车位置
    plt.plot(timestampd, UTM_Y_a, color='green', label='real_Y')
    plt.annotate(f'real_Y_max={round(UTM_Y_max, 1)}', xy=(timestamp_ymax, UTM_Y_max),  # 目标车最大Y值
                 xytext=(timestamp_ymax, UTM_Y_max - 3), color="g", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.annotate(f'real_Y_min={round(UTM_Y_min, 1)}', xy=(timestamp_ymin, UTM_Y_min),  # 目标车最小Y值
                 xytext=(timestamp_ymin, UTM_Y_min + 3), color="g", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.annotate(f'real_X_max={round(UTM_X_max, 1)}', xy=(timestamp_xmax, UTM_X_max),  # 目标车最大X值
                 xytext=(timestamp_xmax, UTM_X_max - 3), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'real_X_min={round(UTM_X_min, 1)}', xy=(timestamp_xmin, UTM_X_min),  # 目标车最小X值
                 xytext=(timestamp_xmin, UTM_X_min - 3), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(1, -10, f'real_X_avg={round(UTM_X_average, 1)}'
                     f'\nreal_Y_avg={round(UTM_Y_average, 1)}', size=6, color="b")  # 平均XY值
    plt.xlabel('time  (s)')
    plt.ylabel('m')
    plt.legend(fontsize=8)  # 开启图例，设置字体大小=6
    plt.subplot(5, 1, 2)
    plt.plot(timestampd, vut_velocity, color='red', label='VUT_V')  # 绘制第二个子图  自车与目标车速度
    plt.plot(timestampd, wey4_velocity_a, color='blue', label='GVT_V')
    if round(vut_velocity_max, 1) > 0:
        plt.annotate(f'VUT_V_max={round(vut_velocity_max, 1)}', xy=(timestamp_vutmax, vut_velocity_max),  # 自车最大速度
                     xytext=(timestamp_vutmax, vut_velocity_max * 0.9), color="b", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'GVT_V_max={round(wey4_velocity_max, 1)}', xy=(timestamp_vmax, wey4_velocity_max),  # 注释目标车最大速度
                 xytext=(timestamp_vmax, wey4_velocity_max * 0.9), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.annotate(f'GVT_V_min={round(wey4_velocity_min, 1)}', xy=(timestamp_vmin, wey4_velocity_min),  # 注释目标车最小速度
                 xytext=(timestamp_vmin, wey4_velocity_min * 0.9), color="b", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.text(int(timestampd[-1] * 0.9), int(wey4_velocity_max / 2), f'GVT_V_avg={round(GVT_velocity_average, 1)}',
             size=6,
             color="b")  # 注释平均速度
    plt.xlabel('time  (s)')
    plt.ylabel('km/h')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 3)
    plt.plot(timestampd, ttcd, color='yellow', label='ttc')  # 绘制第三个子图 DOW状态机与报警等级
    # plt.annotate(f'ttc={round(ttc_b[0],1)}', xy=(timestamp_b[0], ttc_b[0]),    #注释报警开始时刻的ttc
    #                  xytext=(timestamp_b[0] , ttc_b[0] + 2),color="b", size=6,
    #                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
    plt.plot(timestampd, state_machines_a, color='green', label='state_machine')  # DOW状态机与报警等级
    plt.plot(timestampd, warn_lefts_a, color='red', label='warn_left')
    plt.plot(timestampd, warn_rights_a, color='blue', label='warn_right')
    plt.annotate(f'time={round(timestamp_b[0], 1)} start_warn', xy=(timestamp_b[0], warn_b[0]),  # 注释报警开始时刻
                 xytext=(timestamp_b[0], warn_b[0] + 1), color="r", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="r"))
    plt.annotate(f'time={round(timestampd[m], 1)} end_warn', xy=(timestampd[m], warn[m]),  # 注释报警解除时刻
                 xytext=(timestampd[m], warn[m] + 1), color="r", size=6,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="r"))
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 4)
    plt.plot(timestampd, door_status_fl_a, color='green', label='door_status_fl')  # 绘制第四个子图 DOW车门状态
    plt.plot(timestampd, door_status_rl_a, color='red', label='door_status_rl')
    plt.plot(timestampd, door_status_fr_a, color='blue', label='door_status_fr')
    plt.plot(timestampd, door_status_rr_a, color='yellow', label='door_status_rr')
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplot(5, 1, 5)
    plt.plot(timestampd, inhibitions_a, color='green', label='inhibition')  # 绘制第五个子图 抑制条件
    if not all(el == 0 for el in inhibitions_a):
        plt.annotate(f'time={round(timestampd[sign], 1)}', xy=(timestampd[sign], number),  # 目标车最大Y值
                     xytext=(timestampd[sign], number * 0.9), color="g", size=6,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="g"))
    plt.xlabel('time  (s)')
    plt.ylabel('number')
    plt.legend(fontsize=8)  # 开启图例
    plt.subplots_adjust(hspace=0.5)  # 调整子图纵向间隔
    name3 = pic_path + APP.lcmlog_dict['filename'] + 'p3'
    plt.savefig(name3 + '.jpg', bbox_inches='tight')  # 保存测试状态图片
    global mysql_status
    mysql_status = APP.word_docx(f'{name1}.jpg', f'{coincide}', f'{name2}.jpg', f'{name3}.jpg', f'{Warn_level}','')  # 生成docx文档



app = PushLcmState()
app.run_analysis()
app.state = 1
ap = PullLcmName()
ap.run_analysis()

data_name = 0
function_key = [1, 2, 3, 4, 5, 71, 72, 73, 8, 9]
performance_key = [11, 12, 13]
while True:
    if len(ap.name) == 0:
        pass
    elif ap.name != data_name and len(ap.name) != 0:
        APP = ReadLcmAll()
        APP.get_lcm_dataset(ap.name)
        lookup = APP.lookup_data()
        key = APP.case_info_dict['key']
        if key[-1] in function_key:
            app.state = 2
            data_name = ap.name
            function(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif key[-1] in performance_key:
            app.state = 2
            data_name = ap.name
            performance(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        elif key[-1] == 6:
            app.state = 2
            data_name = ap.name
            standby_passive(ap.name)
            app.state = 3
            app.name = str(mysql_status)
        else:
            data_name = ap.name
