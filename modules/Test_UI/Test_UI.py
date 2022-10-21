import os
import time
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog
from tools.listens_lcm import ListensLcmAll
from tools.read_case import ReadCase

# 获取工作路径
main_path = os.getcwd()


class Test_UI:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi(os.path.join(main_path, 'statics/test_ui.ui'))
        # self.ui.comboBox.addItems(['测试用例名称1', '测试用例名称2', '测试用例名称3', '测试用例名称4'])
        # print(self.read_case.cases_list_dict['modular'])
        #self.ui.label_73.QPixmap('/home/wbl/2CAR/data_analysis/modules/control/LingK/Test_UI/statics/捕获.PNG')
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_22.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
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
        # self.ui.pushButton_5.clicked.connect(filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径"))
        # self.listens_lcm()
        # self.updata()
        self.mkdir_file(str(time.strftime("%Y-%m-%d")))

    def lcm_logger(self):
        # 切换主目录  切换日期目录  创建车辆目录   切入车辆目录
        os.chdir(main_path)
        os.chdir('./' + str(time.strftime("%Y-%m-%d")))
        self.mkdir_file(self.ui.comboBox_2.currentText())
        os.chdir('./' + str(self.ui.comboBox_2.currentText()))
        # self.lcmlog_name = str(self.ui.comboBox_2.currentText()) + str('_') \
        #                    + str(time.strftime('%H.%M.%S', time.localtime(time.time())))

        self.lcmlog_name = self.ui.comboBox_5.currentText()[-2:] + self.read_case.cases_list_dict['lcm_name'][
            self.read_case.cases_list_dict['id_name'].index(self.ui.comboBox.currentText())] + str(
            time.strftime('%H.%M.%S', time.localtime(time.time())))
        # self.lcmlog_name = str(self.ui.comboBox_2.currentText()) + str('_') \
        #                    + str(time.strftime('%H.%M.%S', time.localtime(time.time())))

        os.system('lcm-logger ' + str(self.lcmlog_name) + str(' &'))

        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        if self.login_car == 0:
            self.ui.pushButton.setText('数据正在记录')
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.plainTextEdit.setPlainText('欢迎使用奥贝测试工具，数据已开始记录...........')
            self.ui.label_8.setText(str('数据名称:  ') + str(self.lcmlog_name))
        elif self.login_car == 1:
            self.ui.pushButton_7.setEnabled(True)
            self.ui.pushButton_6.setText('*数据正在记录')
            self.ui.plainTextEdit_2.setPlainText('欢迎使用奥贝测试工具，数据已开始记录...........')
        # self.ui.label_8.setText(str('数据名称:  ') + str(self.lcmlog_name))

        self.ui.label.setText(str('测试车辆:  ') + str(self.ui.comboBox_2.currentText()))
        # 下拉获取选中信息
        print(self.ui.comboBox.currentText())
        print(self.ui.comboBox_2.currentText())

    def kill_lcm(self):
        # 切换目录  接触LCM锁  状态绘制  窗口反馈   数据显示
        os.system('pkill lcm-logger')
        if self.login_car == 0:
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton.setText('数据记录')
            self.ui.plainTextEdit.setPlainText('数据结束记录，期待大佬再次使用.')
            self.ui.label_8.setText(str('数据名称:  '))
        elif self.login_car == 1:
            self.ui.pushButton_6.setEnabled(True)
            self.ui.pushButton_6.setText('*数据记录')
            self.ui.plainTextEdit_2.setPlainText('数据结束记录，期待大佬再次使用.')

    def bug_record(self):
        bug_time = (str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.ui.plainTextEdit.setPlainText(
            str(self.lcmlog_name) + str('    ') + str(self.ui.comboBox.currentText()) + str('    ') + str(
                bug_time) + str('    ') + str('    问题描述：  '))
        self.ui.plainTextEdit_2.setPlainText(
            str(self.lcmlog_name) + str('    ') + str(bug_time) + str('    ') + str('    问题描述：  '))

    def bug_writer(self):
        info = self.ui.plainTextEdit.toPlainText()
        with open("BUG.txt", "a") as f:
            f.write(info + '\n')  # 自带文件关闭功能，不需要再写f.close()
        self.ui.plainTextEdit.setPlainText('数据写入成功')
        self.ui.plainTextEdit_2.setPlainText('数据写入成功')

    def mkdir_file(self, file_name):
        # 创建文件夹
        if not os.path.exists(file_name):
            os.makedirs(file_name)
            return True
        else:
            return False

    def listens_lcm(self):
        self.camera_line_data = ListensLcmAll()
        self.camera_line_data.start_receiving()

    def read_cases(self):
        self.read_case = ReadCase()
        self.read_case.read(self.cases_filePath)

        # print(self.read_case.cases_list_dict['name'])

    def cases_data(self):
        self.cases_filePath, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要执行测的用例",  # 标题
            r"main_path",  # 起始目录
            "数据类型 (*.csv )"  # 选择类型过滤项，过滤内容在括号中
        )
        self.ui.label_72.setText(str(os.path.basename(self.cases_filePath)))
        # 解除禁用
        self.ui.pushButton_22.setEnabled(True)
        self.ui.pushButton_22.setText('进入测试页面')

    def login_case(self):
        self.ui.comboBox.clear()
        self.read_cases()  # 读取cvs文件
        self.ui.comboBox.addItems(self.read_case.cases_list_dict['id_name'])

        #self.ui.tabWidget.setCurentIndex(1)
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
        else:
            self.ui.label_72.setText(str('请选择测试车辆'))
            pass

    def login_case_default(self):
        self.cases_filePath = os.path.join(main_path, 'statics/case_default.csv')
        # self.ui.pushButton_21.setEnabled(False)
        self.ui.label_72.setText(str(os.path.basename(self.cases_filePath)))
        # 解除禁用
        self.ui.pushButton_22.setEnabled(True)
        self.ui.pushButton_22.setText('进入测试页面')
        #接触锁定
        self.listens_lcm()
        self.updata()

    def updata(self):
        def run():
            while True:
                time.sleep(0.1)
                self.ui.label_31.setText(str('测试人员:  ') + self.ui.comboBox_5.currentText())
                self.ui.label_52.setText(str('*测试人员:  ') + self.ui.comboBox_5.currentText())
                self.ui.label_41.setText(
                    str('系统时间:  ') + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                self.ui.label_53.setText(
                    str('*系统时间:  ') + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                self.ui.label_2.setText(str('定位模式:  ') + str(self.camera_line_data.gps_imu_dict["gps"][5]))
                self.ui.label_3.setText(str('GPS经度:  ') + str(self.camera_line_data.gps_imu_dict["gps"][0]))
                self.ui.label_4.setText(str('GPS纬度:  ') + str(self.camera_line_data.gps_imu_dict["gps"][1]))
                self.ui.label_5.setText(str('GPS航向:  ') + str(self.camera_line_data.gps_imu_dict["gps"][2]))
                self.ui.label_6.setText(str('GPS速度:  ') + str(self.camera_line_data.gps_imu_dict["gps"][4]))
                self.ui.label_9.setText(str('卫星数:  ') + str(self.camera_line_data.gps_imu_dict["gps"][6]))
                self.ui.label_11.setText(str('自驾模式:  ') + str(self.camera_line_data.chassis_dict["state"][0]))
                self.ui.label_12.setText(str('设置最大速度:  ') + str(self.camera_line_data.chassis_dict["state"][3]))
                self.ui.label_13.setText(str('底盘速度:  ') + str(self.camera_line_data.chassis_dict["state"][4]))
                self.ui.label_14.setText(str('转向灯状态:  ') + str(self.camera_line_data.chassis_dict["state"][5]))
                self.ui.label_15.setText(str('方向盘转角:  ') + str(self.camera_line_data.chassis_dict["state"][1]))
                self.ui.label_28.setText(str('中心线长度和横向误差:  ') +
                                         str(self.camera_line_data.lanes_coeff_dict["center_line"][4]) + str('      ') +
                                         str(self.camera_line_data.lanes_coeff_dict["center_line"][0]))
                self.ui.label_29.setText(str('车道线长度:  ') +
                                         str(self.camera_line_data.lanes_coeff_dict["lane_left_most"][4])
                                         + str('      ') + str(
                    self.camera_line_data.lanes_coeff_dict["lane_left_middle"][4])
                                         + str('      ') + str(
                    self.camera_line_data.lanes_coeff_dict["lane_right_middle"][4])
                                         + str('      ') + str(
                    self.camera_line_data.lanes_coeff_dict["lane_right_most"][4]))
                self.ui.label_30.setText(str('车道线类型:  ')
                                         + str(self.camera_line_data.lanes_coeff_dict["lane_type"][0]) + str('      ')
                                         + str(self.camera_line_data.lanes_coeff_dict["lane_type"][1]) + str('      ')
                                         + str(self.camera_line_data.lanes_coeff_dict["lane_type"][2]) + str('      ')
                                         + str(self.camera_line_data.lanes_coeff_dict["lane_type"][3]) + str('      '))

        t = Thread(target=run)
        t.start()


if __name__ == '__main__':
    app = QApplication([])
    stats = Test_UI()
    stats.ui.show()
    app.exec_()
