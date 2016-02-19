#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年2月17日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: time和datetime模块演示程序

Help:
'''
if __name__ == '__main__':
    import time
    import datetime
    print(time.time()) # 返回当前时间的时间戳
    print(time.ctime()) # 将时间戳转化为字符串格式Wed Feb 17 11:41:27 2016，默认是当前系统时间的时间戳
    print(time.ctime(time.time() - 3600)) # ctime可以接收一个时间戳作为参数，返回该时间戳的字符串形式 Wed Feb 17 10:43:04 2016
    print(time.gmtime()) # 将时间戳转化为struct_time格式，默认是当前系统时间戳
    print(time.gmtime(time.time() - 3600))
    #print(dict(time.gmtime()))
    print(time.gmtime()[0])
    print(time.localtime()) # 同样是将时间戳转化为struct_time，只不过显示的是本地时间，gmtime显示的是标准时间（格里尼治时间）
    print(time.mktime(time.localtime())) # 将struct_time时间格式转化为时间戳
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) # 将struct_time时间格式转化为自定义的字符串格式
    print(time.strptime("2016-2-17", "%Y-%m-%d")) # 与trftime相反，将字符串格式转化为struct_time格式
    print(time.asctime(time.localtime())) # 将struct_time转化为字符串形式


    print(datetime.date.today()) # 返回当前日期的字符串形式2016-02-17
    print(datetime.date.fromtimestamp(time.time() - 3600 * 24)) # 将时间戳转化为字符串形式2016-02-16
    print(datetime.datetime.now()) # 返回的时间的字符串形式2016-02-17 13:53:30.719803
    print(datetime.datetime.now().timetuple()) # 转化为struct_time格式
    # timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
    print(datetime.datetime.now() - datetime.timedelta(days = 2))

    import random
    print(random.random()) #生成大于0小于1的浮点类型随机数
    print(random.randint(1, 10)) # 生成指定大于等于1小于等于10的随机数
    print(random.randrange(1,10))