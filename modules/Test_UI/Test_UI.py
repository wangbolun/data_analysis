import os
import time
from PyQt5 import uic
from threading import Thread
from PyQt5.QtWidgets import QApplication, QFileDialog
from tools.listens_lcm import ListensLcmAll, ListensLcmAll_VV6
from tools.read_case import ReadCase


class Test_UI:
    def __init__(self):
        self.keys = 0  # 状态
        # 从文件中加载UI定义
        self.main_path = os.getcwd()
        self.ui = uic.loadUi(os.path.join(self.main_path, 'statics/test_ui.ui'))
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_22.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.radioButton.setChecked(True)  # 默认选择测试车
        self.ui.pushButton.setText('请选择测试用例')
        self.ui.pushButton_6.setText('*请选择测试用例')
        self.ui.pushButton_22.setText('请选择测试用例')
        self.ui.pushButton.clicked.connect(self.lcm_logger)
        self.ui.pushButton_4.clicked.connect(self.kill_lcm)
        self.ui.pushButton_6.clicked.connect(self.lcm_logger)
        self.ui.pushButton_9.clicked.connect(self.kill_lcm)
        self.ui.pushButton_2.clicked.connect(self.bug_record)
        self.ui.pushButton_7.clicked.connect(self.bug_record)
        self.ui.pushButton_3.clicked.connect(self.bug_writer)
        self.ui.pushButton_8.clicked.connect(self.bug_writer)
        self.ui.pushButton_5.clicked.connect(self.cases_data)
        self.ui.pushButton_22.clicked.connect(self.login_case)
        self.ui.pushButton_21.clicked.connect(self.login_case_default)
        self.ui.tabWidget.setCurrentIndex(0)  # 设定初始页面
        self.mkdir_file(str(time.strftime("%Y-%m-%d")))  # 创建日期目录

    def lcm_logger(self):
        # 切换主目录  切换日期目录  创建车辆目录   切入车辆目录
        os.chdir(self.main_path)
        os.chdir('./' + str(time.strftime("%Y-%m-%d")))
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        if self.login_car == 0:
            self.mkdir_file('VUT')  # 创建目录
            os.chdir('./' + 'VUT')  # 切换目录
            self.lcmlog_name = self.ui.comboBox_5.currentText()[-2:] + str('_') + self.ui.comboBox_2.currentText() + \
                               self.read_case.cases_list_dict['lcm_name'][
                                   self.read_case.cases_list_dict['id_name'].index(
                                       self.ui.comboBox.currentText())] + str(
                time.strftime('%H.%M.%S', time.localtime(time.time()))) + str('_') + str(
                self.ui.comboBox_6.currentText()) + str('_') + str(self.ui.comboBox_4.currentText())
            os.system('lcm-logger ' + str(self.lcmlog_name) + str(' &'))
            self.ui.pushButton.setText('数据正在记录')
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.plainTextEdit.setPlainText('欢迎使用奥贝测试工具，数据已开始记录...........')
            self.ui.label_8.setText(str('数据名称:  ') + str(self.lcmlog_name))
            self.ui.label.setText(str('测试车辆:  ') + str(self.ui.comboBox_2.currentText()))

        elif self.login_car == 1:
            self.mkdir_file('GVT')
            os.chdir('./' + 'GVT')  # 切换目录
            self.lcmlog_name = self.ui.comboBox_5.currentText()[-2:] + str('_') + self.ui.comboBox_2.currentText() + \
                               self.read_case.cases_list_dict['lcm_name'][
                                   self.read_case.cases_list_dict['id_name'].index(
                                       self.ui.comboBox_3.currentText())] + str(
                time.strftime('%H.%M.%S', time.localtime(time.time())))
            os.system('lcm-logger ' + str(self.lcmlog_name) + str(' &'))
            self.ui.pushButton_7.setEnabled(True)
            self.ui.pushButton_6.setText('*数据正在记录')
            self.ui.plainTextEdit_2.setPlainText('欢迎使用奥贝测试工具，数据已开始记录...........')
            self.ui.label_50.setText(str('数据名称:  ') + str(self.lcmlog_name))
            self.ui.label_51.setText(str('测试车辆:  ') + str(self.ui.comboBox_2.currentText()))


    def kill_lcm(self):
        # 切换目录  接触LCM锁  状态绘制  窗口反馈   数据显示
        if self.login_car == 0:
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton.setText('数据记录')
            self.ui.plainTextEdit.setPlainText('数据结束记录，期待大佬再次使用.')
            self.ui.label_8.setText(str('数据名称:  '))
            os.system('pkill lcm-logger &')
        elif self.login_car == 1:
            self.ui.pushButton_6.setEnabled(True)
            self.ui.pushButton_6.setText('*数据记录')
            self.ui.plainTextEdit_2.setPlainText('数据结束记录，期待大佬再次使用.')
            self.ui.label_50.setText(str('*数据名称:  '))
            os.system('pkill lcm-logger &')

    def bug_record(self):
        bug_time = (str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.ui.plainTextEdit.setPlainText(
            str(self.lcmlog_name) + str('    ') + str(self.ui.comboBox.currentText()) + str('    ') + str(
                bug_time) + str('    ') + str('    问题描述：  '))
        self.ui.plainTextEdit_2.setPlainText(
            str(self.lcmlog_name) + str('    ') + str(bug_time) + str('    ') + str('    问题描述：  '))

    def bug_writer(self):
        if self.login_car == 0:
            info = self.ui.plainTextEdit.toPlainText()
            with open("BUG.txt", "a") as f:
                f.write(info + '\n')  # 自带文件关闭功能，不需要再写f.close()
            self.ui.plainTextEdit.setPlainText('数据写入成功')
        elif self.login_car == 1:
            info = self.ui.plainTextEdit_2.toPlainText()
            with open("BUG.txt", "a") as f:
                f.write(info + '\n')  # 自带文件关闭功能，不需要再写f.close()
            self.ui.plainTextEdit_2.setPlainText('数据写入成功')

    def mkdir_file(self, file_name):
        # 创建文件夹
        if not os.path.exists(file_name):
            os.makedirs(file_name)
            return True
        else:
            return False

    def read_cases(self):
        self.read_case = ReadCase()
        self.read_case.read(self.cases_filePath)

    def login_case_default(self):
        # 去除BUG 选择数据后锁定
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_22.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.cases_filePath = os.path.join(self.main_path, 'statics/case_default.csv')
        # self.ui.pushButton_21.setEnabled(False)
        self.ui.label_72.setText(str(os.path.basename(self.cases_filePath)))
        # 解除禁用
        self.ui.pushButton_22.setEnabled(True)
        self.ui.pushButton_22.setText('进入测试页面')
        # 车辆选择
        if self.ui.radioButton.isChecked() == True:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(['LiK1', 'LiK2', 'LiK9'])
        elif self.ui.radioButton_2.isChecked() == True:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(['WEY1', 'WEY4', 'OULA'])

    def cases_data(self):
        self.cases_filePath, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要执行测的用例",  # 标题
            r"self.main_path",  # 起始目录
            "数据类型 (*.csv )"  # 选择类型过滤项，过滤内容在括号中
        )
        self.ui.label_72.setText(str(os.path.basename(self.cases_filePath)))
        # 进入车辆选择
        if self.ui.radioButton.isChecked() == True:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(['LingK1', 'LingK2', 'LingK9'])

        elif self.ui.radioButton_2.isChecked() == True:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(['WEY1', 'WEY4', 'OULA'])
        # 解除禁用
        self.ui.pushButton_22.setEnabled(True)
        self.ui.pushButton_22.setText('进入测试页面')

    def login_case(self):
        # 消除复选框
        self.ui.comboBox.clear()
        self.ui.comboBox_3.clear()
        self.read_cases()  # 读取cvs文件
        # 赋值下拉框
        self.ui.comboBox.addItems(self.read_case.cases_list_dict['id_name'])
        # 赋值下拉框
        self.ui.comboBox_3.addItems(self.read_case.cases_list_dict['id_name'])
        if self.ui.radioButton.isChecked() == True:
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_4.setEnabled(True)
            self.ui.pushButton.setText('数据记录')
            self.ui.pushButton_6.setEnabled(False)
            self.ui.pushButton_7.setEnabled(False)
            self.ui.pushButton_8.setEnabled(False)
            self.ui.pushButton_9.setEnabled(False)
            self.ui.tabWidget.setCurrentIndex(1)
            self.login_car = 0
            self.listens_lcm_all = ListensLcmAll()  # 监听目标车通道
            self.listens_lcm_all.start_receiving()
            self.updata()
            # 控制配合车数据记录按钮

        elif self.ui.radioButton_2.isChecked() == True:
            self.ui.pushButton_6.setEnabled(True)
            self.ui.pushButton_8.setEnabled(True)
            self.ui.pushButton_9.setEnabled(True)
            self.ui.pushButton_6.setText('数据记录')
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.tabWidget.setCurrentIndex(2)
            self.login_car = 1
            self.vv6_data = ListensLcmAll_VV6()  # 监听配合车通道
            self.vv6_data.start_receiving()
            self.updata_vv6()

    def keyy(self):
        ###通过按钮获取配合车状态
        self.key = int((self.read_case.cases_list_dict['key'][
            self.read_case.cases_list_dict['id_name'].index(self.ui.comboBox.currentText())][0]))
        if self.key == 0:
            self.ui.comboBox_6.clear()
            self.ui.comboBox_4.clear()
        elif self.key == 1:
            self.ui.comboBox_6.clear()
            self.ui.comboBox_4.clear()
            self.ui.comboBox_6.addItems(['WEY1', 'WEY4', 'OULA'])
        elif self.key == 2:
            self.ui.comboBox_6.clear()
            self.ui.comboBox_4.clear()
            self.ui.comboBox_6.addItems(['WEY1', 'WEY4', 'OULA'])
            self.ui.comboBox_4.addItems(['WEY1', 'WEY4', 'OULA'])

    def updata(self):
        def run():
            while True:
                time.sleep(0.1)
                # 验证数值变化
                self.key = int(self.read_case.cases_list_dict['key'][
                                   self.read_case.cases_list_dict['id_name'].index(self.ui.comboBox.currentText())][0])
                if self.key != self.keys:
                    self.keyy()
                    self.keys = self.key
                self.ui.label_31.setText(str('测试人员:  ') + self.ui.comboBox_5.currentText())
                self.ui.label_41.setText(
                    str('系统时间:  ') + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                self.ui.label_2.setText(str('定位模式:  ') + str(self.listens_lcm_all.gps_imu_dict["gps"][5]))
                self.ui.label_3.setText(str('GPS经度:  ') + str(self.listens_lcm_all.gps_imu_dict["gps"][0]))
                self.ui.label_4.setText(str('GPS纬度:  ') + str(self.listens_lcm_all.gps_imu_dict["gps"][1]))
                self.ui.label_5.setText(str('GPS航向:  ') + str(self.listens_lcm_all.gps_imu_dict["gps"][2]))
                self.ui.label_6.setText(str('GPS速度:  ') + str(self.listens_lcm_all.gps_imu_dict["gps"][4]))
                self.ui.label_9.setText(str('卫星数:  ') + str(self.listens_lcm_all.gps_imu_dict["gps"][6]))
                self.ui.label_11.setText(str('自驾模式:  ') + str(self.listens_lcm_all.chassis_dict["state"][0]))
                self.ui.label_12.setText(str('设置最大速度:  ') + str(self.listens_lcm_all.chassis_dict["state"][3]))
                self.ui.label_13.setText(str('底盘速度:  ') + str(self.listens_lcm_all.chassis_dict["state"][4]))
                self.ui.label_14.setText(str('转向灯状态:  ') + str(self.listens_lcm_all.chassis_dict["state"][5]))
                self.ui.label_15.setText(str('方向盘转角:  ') + str(self.listens_lcm_all.chassis_dict["state"][1]))
                self.ui.label_28.setText(str('中心线长度和横向误差:  ') +
                                         str(self.listens_lcm_all.lanes_coeff_dict["center_line"][4]) + str('      ') +
                                         str(self.listens_lcm_all.lanes_coeff_dict["center_line"][0]))
                self.ui.label_29.setText(str('车道线长度:  ') +
                                         str(self.listens_lcm_all.lanes_coeff_dict["lane_left_most"][4])
                                         + str('      ') + str(
                    self.listens_lcm_all.lanes_coeff_dict["lane_left_middle"][4])
                                         + str('      ') + str(
                    self.listens_lcm_all.lanes_coeff_dict["lane_right_middle"][4])
                                         + str('      ') + str(
                    self.listens_lcm_all.lanes_coeff_dict["lane_right_most"][4]))
                self.ui.label_30.setText(str('车道线类型:  ')
                                         + str(self.listens_lcm_all.lanes_coeff_dict["lane_type"][0]) + str('      ')
                                         + str(self.listens_lcm_all.lanes_coeff_dict["lane_type"][1]) + str('      ')
                                         + str(self.listens_lcm_all.lanes_coeff_dict["lane_type"][2]) + str('      ')
                                         + str(self.listens_lcm_all.lanes_coeff_dict["lane_type"][3]) + str('      '))
                self.ui.label_19.setText(
                    str("%.2f" % self.listens_lcm_all.grid_info_dict["front_left"][2]) + str('      ') + str(
                        "%.2f" % self.listens_lcm_all.grid_info_dict["front_left"][4]))
                self.ui.label_20.setText(str("%.2f" % self.listens_lcm_all.grid_info_dict["front"][2]) + str('      ')
                                         + str("%.2f" % self.listens_lcm_all.grid_info_dict["front"][4]))
                self.ui.label_18.setText(
                    str("%.2f" % self.listens_lcm_all.grid_info_dict["front_right"][2]) + str('      ')
                    + str("%.2f" % self.listens_lcm_all.grid_info_dict["front_right"][4]))
                self.ui.label_23.setText(str("%.2f" % self.listens_lcm_all.grid_info_dict["left"][2]) + str('      ')
                                         + str("%.2f" % self.listens_lcm_all.grid_info_dict["left"][4]))
                self.ui.label_24.setText(str("%.2f" % self.listens_lcm_all.grid_info_dict["right"][2]) + str('      ')
                                         + str("%.2f" % self.listens_lcm_all.grid_info_dict["right"][4]))
                self.ui.label_25.setText(
                    str("%.2f" % self.listens_lcm_all.grid_info_dict["rear_left"][2]) + str('      ')
                    + str("%.2f" % self.listens_lcm_all.grid_info_dict["rear_left"][4]))
                self.ui.label_22.setText(str("%.2f" % self.listens_lcm_all.grid_info_dict["rear"][2]) + str('      ')
                                         + str("%.2f" % self.listens_lcm_all.grid_info_dict["rear"][4]))
                self.ui.label_26.setText(
                    str("%.2f" % self.listens_lcm_all.grid_info_dict["rear_right"][2]) + str('      ')
                    + str("%.2f" % self.listens_lcm_all.grid_info_dict["rear_right"][4]))
                # ADAS
                self.ui.label_36.setText(
                    str('LCA、BSD、DOW模式：  ') + str(self.listens_lcm_all.lcm_info_dict["state_machine"][0])
                    + str('            ') + str(self.listens_lcm_all.lcm_info_dict["state_machine"][1])
                    + str('            ') + str(self.listens_lcm_all.lcm_info_dict["state_machine"][2]))
                self.ui.label_37.setText(
                    str('报警方向及等级：  ') + str(self.listens_lcm_all.lcm_info_dict["warn"][0])
                    + str('    ') + str(self.listens_lcm_all.lcm_info_dict["warn"][1]) + str('          ') + str(
                        self.listens_lcm_all.lcm_info_dict["warn"][2]) + str('    ') + str(
                        self.listens_lcm_all.lcm_info_dict["warn"][3]) + str('          ') + str(
                        self.listens_lcm_all.lcm_info_dict["warn"][4]) + str('    ') + str(
                        self.listens_lcm_all.lcm_info_dict["warn"][5]))

        t = Thread(target=run)
        t.start()

    def updata_vv6(self):
        def run():
            while True:
                time.sleep(0.1)
                self.ui.label_52.setText(str('*测试人员:  ') + self.ui.comboBox_5.currentText())
                self.ui.label_53.setText(
                    str('*系统时间:  ') + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                self.ui.label_55.setText(str('*定位模式:  ') + str(self.vv6_data.vv6_gps_imu_dict["gps"][5]))
                self.ui.label_56.setText(str('*GPS经度:  ') + str(self.vv6_data.vv6_gps_imu_dict["gps"][0]))
                self.ui.label_57.setText(str('*GPS纬度:  ') + str(self.vv6_data.vv6_gps_imu_dict["gps"][1]))
                self.ui.label_58.setText(str('*GPS航向:  ') + str(self.vv6_data.vv6_gps_imu_dict["gps"][2]))
                self.ui.label_59.setText(str('*GPS速度:  ') + str(self.vv6_data.vv6_gps_imu_dict["gps"][4]))
                self.ui.label_60.setText(str('*卫星数:  ') + str(self.vv6_data.vv6_gps_imu_dict["gps"][6]))

        t = Thread(target=run)
        t.start()


if __name__ == '__main__':
    app = QApplication([])
    stats = Test_UI()
    stats.ui.show()
    app.exec_()
