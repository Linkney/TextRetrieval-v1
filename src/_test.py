import matplotlib.pyplot as plt
import numpy as np
import pymysql
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort



# class test:
#     # 类变量
#     i = -1
#     l = [-1]
#
#     def __init__(self):
#         print("init")
#
#
# def fakemain():
#     a = test()
#     b = test()
#     listtest = [a, b]
#     print(listtest[0].i)
#     print(listtest[1].i)
#     print(test.i)
#     print(listtest[0].l)
#     print(listtest[1].l)
#     print(test.l)
#     print('-------------------')
#     listtest[0].i = 2
#     listtest[0].l = [2]
#     print(listtest[0].i)
#     print(listtest[1].i)
#     print(test.i)
#     print(listtest[0].l)
#     print(listtest[1].l)
#     print(test.l)
#     print('-------------------')
#     listtest[1].i = 3
#     listtest[1].l = [3]
#     print(listtest[0].i)
#     print(listtest[1].i)
#     print(test.i)
#     print(listtest[0].l)
#     print(listtest[1].l)
#     print(test.l)
#     print('-------------------')
#     test.i = 4
#     test.l = [4]
#     print(listtest[0].i)
#     print(listtest[1].i)
#     print(test.i)
#     print(listtest[0].l)
#     print(listtest[1].l)
#     print(test.l)
#     print('-------------------')
#
#
# def matplot():
#     x = np.linspace(0, 2, 2)
#     y = [2, 3]
#     plt.xlabel("x'slabel")  # x轴上的名字
#     plt.ylabel("y's;abel")  # y轴上的名字
#     plt.plot(x, y)
#     plt.show()
#
#
# def sql():
#     conn = pymysql.connect(host="localhost", user="root", password="root", database="test")
#     cursor = conn.cursor()
#
#     # sql语句及执行
#     sql = "select * from testinfo"
#     cursor.execute(sql)
#     # 数据处理
#     getFromMysql = cursor.fetchall()
#     print(getFromMysql)
#
#     cursor.close()
#     conn.close()


if __name__ == '__main__':
    sql = "(paperId, title, author, abstract, localAddress) values(%d, %s, %s, %s, %s)"


