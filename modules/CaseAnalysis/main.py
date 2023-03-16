import os
import time
from tools import mysqlpy
from tools.connect_lcm import PullLcmState, PushLcmName


class RunDataAnalysis:
    def __init__(self):
        self.data_info = {"name": [],
                          "name_path": [],
                          "lca_name": [],
                          "dow_name": []}
        # self.mkdir_file(str(time.strftime("%Y-%m-%d")))  # 创建日期目录
        pass

    def mkdir_file(self, file_name):
        # 创建文件夹,传参
        if not os.path.exists(file_name):
            os.makedirs(file_name)
            return True
        else:
            return False

    def monitor(self):
        # 监控目标路径是否有新文件
        path = '/home/dell/APP/CaseAnalysis/2022-12-09/VUT'
        # 自动获取路径    获取当前路径   添加时间路径   添加VUT路径
        # path = os.path.join(os.getcwd(), time.strftime("%Y-%m-%d"), 'VUT')
        #创建存放测试结果的文件
        self.mkdir_file(os.path.join(os.getcwd(), '2022-12-09', 'report'))

        # 创建目录
        for (dirpath, dirnames, filenames) in os.walk(path):
            for fn in filenames:
                fpath = os.path.join(dirpath, fn)
                self.data_info['name'].append(fn)
                self.data_info['name_path'].append(fpath)
                # 分类判断
                if fn.split('_')[2] == 'LCA':
                    self.data_info['lca_name'].append(fpath)
                elif fn.split('_')[2] == 'DOW':
                    self.data_info['dow_name'].append(fpath)

    def demo(self):
        # 运行数据发送的程序
        ap = PushLcmName()
        ap.run_analysis()
        app = PullLcmState()
        app.run_analysis()
        lca_len = int(len(self.data_info['lca_name']))
        dow_len = int(len(self.data_info['dow_name']))
        print(lca_len, dow_len)

        # DOW功能数据下发
        time.sleep(1)
        if dow_len >= 0:
            print('启动DOW程序')
            os.system('sh /home/dell/APP/CaseAnalysis/analysis/dist_DOW/run_dow.sh &')
        while dow_len > 0:
            if int(app.state) == 1 or int(app.state) == 3:
                status = 1  # 状态用于接收返回的状态
                ap.name = self.data_info['dow_name'][int(dow_len) - 1]
                dow_len = dow_len - 1
                time.sleep(2)
                print('正在发送数据，剩余：', dow_len, ap.name)
                # 这里用于MySQL数据写入，转移文件等
                while status > 0:
                    # 验证是否完成工作，并且返回数据的ID与发送ID一直。（app.name是是字符串   之一注意）
                    if int(app.state) == 3 and int(ap.name.split('/')[-1].split('_')[4]) == int(
                            str(app.name.split(',')[5]).split('_')[4]):
                        # 将字符串变回列表
                        lcm_name = eval(app.name)
                        # 写入MySQL数据
                        try:
                            mysqlpy.add_mysql(lcm_name[0], lcm_name[1], lcm_name[2], lcm_name[3], lcm_name[4],
                                              lcm_name[5], lcm_name[6], lcm_name[7], lcm_name[8], lcm_name[9],
                                              lcm_name[10], lcm_name[11], lcm_name[12], lcm_name[13])
                        except:
                            print('mysql 数据写入失败')

                        status = 0  # 写入成功后退出循环
                    else:
                        time.sleep(0.2)
        if dow_len == 0:
            os.system('sync')
            time.sleep(10)
            os.system('pkill DOW')

        # LCA功能数据下发
        time.sleep(5)
        if lca_len >= 0:
            print('启动LCA程序')
            os.system('sh /home/dell/APP/CaseAnalysis/analysis/dist_LCA/run_lca.sh &')
        while lca_len > 0:
            if int(app.state) == 1 or int(app.state) == 3:
                status = 1  # 状态用于接收返回的状态
                ap.name = self.data_info['lca_name'][int(lca_len) - 1]
                lca_len = lca_len - 1
                time.sleep(2)
                print('正在发送数据，剩余：', lca_len, ap.name)
                # 这里用于MySQL数据写入，转移文件等
                while status > 0:
                    # 验证是否完成工作，并且返回数据的ID与发送ID一直。（app.name是是字符串   之一注意）
                    if int(app.state) == 3 and int(ap.name.split('/')[-1].split('_')[4]) == int(
                            str(app.name.split(',')[5]).split('_')[4]):
                        # 将字符串变回列表
                        lcm_name = eval(app.name)
                        # 写入MySQL数据
                        try:
                            mysqlpy.add_mysql(lcm_name[0], lcm_name[1], lcm_name[2], lcm_name[3], lcm_name[4],
                                              lcm_name[5], lcm_name[6], lcm_name[7], lcm_name[8], lcm_name[9],
                                              lcm_name[10], lcm_name[11], lcm_name[12], lcm_name[13])
                        except:
                            print('mysql 数据写入失败')

                        status = 0  # 写入成功后退出循环
                    else:
                        # print(int(ap.name.split('/')[-1].split('_')[4]),int(str(app.name.split(',')[5]).split('_')[4]))
                        time.sleep(0.2)
        if lca_len == 0:
            os.system('sync')
            time.sleep(10)
            os.system('pkill LCA')

        print('彻底结束杀死main程序.........')


if __name__ == '__main__':
    a = RunDataAnalysis()
    a.monitor()
    a.demo()
