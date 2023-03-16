"""
这是一个使用Python增、删、改、查MySQL数据的工具，直接封装成函数，进行导包使用
"""
import pymysql


def add_mysql(join_time, name, car, functional, test_id, vut_name, case_modular, case_title, data_duration,
              data_mileage, auto_mileage, gvt_name1, gvt_name2, status):
    # 2.打开数据库连接
    conn = pymysql.connect(host='localhost', user='root', password="12345678", database='test_data', port=3306)
    # 3.获取游标
    cursor = conn.cursor()
    # 查询数据库，当日信息是否有重复的数据名称，如果有则删除旧的，写入新的数据
    cursor.execute("select * from data_tbl")
    tup = cursor.fetchall()
    for i in tup:
        if str(i[1]) == join_time and str(i[6]) == vut_name:
            cursor.execute("DELETE FROM data_tbl WHERE id=%s;", i[0])
    # 写入新的数据
    sql = "INSERT INTO data_tbl (join_time,name,car,functional,test_id,vut_name,case_modular,case_title,data_duration,data_mileage,auto_mileage,gvt_name1,gvt_name2,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    param = (join_time, name, car, functional, test_id, vut_name, case_modular, case_title, data_duration, data_mileage,
             auto_mileage, gvt_name1, gvt_name2, status)
    # 4.执行SQL语句
    cursor.execute(sql, param)
    # 提交事务
    conn.commit()
    # 关闭一定保留
    conn.close()
    cursor.close()


def delete_mysql():
    # 2.打开数据库连接
    conn = pymysql.connect(host='localhost', user='root', password="000000", database='test_data', port=3306)
    # 3.获取游标
    cursor = conn.cursor()
    # 需要获取ID才能删除
    cursor.execute("DELETE FROM data_tbl WHERE id=25;")
    # 提交
    conn.commit()
    # 关闭一定保留
    conn.close()
    cursor.close()


def change_mysql():
    pass


def check_mysql():
    # 2.打开数据库连接
    conn = pymysql.connect(host='localhost', user='root', password="12345678", database='test_data', port=3306)
    # 3.获取游标
    cursor = conn.cursor()
    # 查询
    cursor.execute("select * from data_tbl")
    tup = cursor.fetchall()
    # 关闭一定保留
    conn.close()
    cursor.close()
    return tup


if __name__ == '__main__':
    add_mysql('2022-12-09', '01', 'LiK2', 'DOW开门预警系统', '111', '02_LiK2_DOW_457_7297_13.40.51_WEY1_',
              '/DOW开门预警系统/功能测试/功能激活测试/第一阶段报警-目标车辆(#457)', '目标车辆20km/h右侧超越被测车辆', '4.06', '0.00', '0.00', '配合车数据1',
              '配合车数据名称2', '失败')
