#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2015年12月30日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: 三层菜单
                1、菜单一共三级即：省，市，区县
                2、每一级菜单输入的如果输入的是菜单里的选项则进入下级菜单
                3、第1级菜单输入q退出系统
                4、第2、3级菜单输入q退出系统，输入b返回上级菜单
                5、三级菜单全部正确打印最后的全部选择结果，否则继续循环该机菜单

Help:
'''


if __name__ == '__main__':
    '''
    @parameters:
        provinces：定义省一级菜单，格式为字典，{"菜单序号":"省名称", ...}
        citys：定义省一级菜单，格式为二级嵌套字典{"省名称":{"菜单序号":"市名称"}, ...}
        area：定义区县一级菜单，格式为二级嵌套字典{"市名称":{"菜单序号":"区县名称"}, ...}
        app_info：系统信息，主要用于显示
    '''
    provinces = {
        "1":"北京",
        "2":"上海",
        "3":"河北省",
    }
    citys = {
        "北京":{"1":"北京市区","2":"北京市郊区"},
        "上海":{"1":"上海市区"},
        "河北省":{"1":"石家庄市", "2":"秦皇岛市", "3":"保定市"}
    }
    areas = {
        "北京市区":{"1":"东城区", "2":"西城区", "3":"海淀区", "4":"朝阳区", "5":"丰台区", "6":"石景山区"},
        "北京市郊区":{ "1":"通州区", "2":"顺义区", "3":"房山区", "4":"大兴区", "5":"昌平区", "6":"怀柔区", "7":"平谷区", "8":"门头沟区", "9":"密云县", "10":"延庆县"},
        "上海市区":{"1":"黄浦区", "2":"卢湾区", "3":"徐汇区", "4":"长宁区", "6":"静安区", "7":"普陀区", "8":"闸北区", "9":"虹口区", "11":"杨浦区", "12":"宝山区"},
        "石家庄市":{"1":"鹿泉", "2":"正定", "3":"藁城", "4":"栾城", "5":"高邑", "6":"新乐", "7":"辛集", "8":"赵县", "9":"深泽", "10":"晋州"},
        "保定市":{"1":"南市区", "2":"北市区", "3":"新市区", "4":"白沟新城区", "5":"顺平县"},
        "秦皇岛市":{"1":"海港区", "2":"山海关区", "3":"北戴河区", "4":"抚宁区", "5":"昌黎县", "6":"卢龙县", "7":"青龙满族自治县"}
    }

    app_info = '''
+-----------------------------------+
| Welcome to 65brother system       |
| Version: 1.0                      |
| Author: zhangxiaoyu               |
+-----------------------------------+
'''
    # 初始化菜单列表，主要是做了一次排序，解决字典无序的问题，这里的d[0]表示对key做排序，int表示先转换成整数，也就是按照整数的顺序进行排序否则如果序号超过10，会出现1后面的是10而不是2
    province_list = sorted(provinces.items(), key = lambda d:int(d[0]))
    # 初始化省一级菜单循环开关
    province_flag = True
    # 省一级菜单循环
    while province_flag:
        # 初始化市一级菜单的循环开关
        city_flag = True
        print(app_info)
        # 打印当前用户的位置
        print("home>")
        # 打印省一级菜单
        print("+-----------------------------------+")
        for province_item in province_list:
            print("  %s、%s" %province_item)
        print("+-----------------------------------+")
        # 获取用户输入的选项
        province = input("请输入你的省份（输入'q'退出系统）：").strip()
        # 判断用户的输入
        if province == 'q':
            # 如果用户输入的是q关闭省一级菜单循环开关，也就是退出系统
            province_flag = False
        elif province in provinces:
            # 如果输入的是菜单的序号执行
            # 获取省的名称
            province_name = provinces[province]
            # 初始化市一级菜单，同省一样对key进行排序
            city_list = sorted(citys[province_name].items(), key = lambda  d:int(d[0]))
            # 市一级菜单循环
            while city_flag:
                # 打印用户位置
                print("home>%s>" %province_name)
                # 打印市一级菜单
                print("+-----------------------------------+")
                for city_item in city_list:
                    print("  %s、%s" %city_item)
                print("+-----------------------------------+")
                # 获取用户输入
                city = input("请输入你的城市（输入'q'退出系统，输入'b'返回上一级菜单）：").strip()
                # 判断用户输入
                if city == 'q':
                    # 如果输入q关闭省一级和市一级循环开关，也就是退出系统
                    province_flag = False
                    city_flag = False
                elif city == 'b':
                    # 如果用户输入的是b，关闭市一级循环开关，继续省一级循环
                    city_flag = False
                elif city in citys[province_name]:
                    # 如果用户输入的是正确的菜单项
                    # 初始化区县一级循环开关
                    area_flag = True
                    # 获取市的名称
                    city_name = citys[province_name][city]
                    # 初始户区县菜单
                    area_list = sorted(areas[city_name].items(), key = lambda  d:int(d[0]))
                    # 区县一级循环
                    while area_flag:
                        # 打印用户位置
                        print("home>%s>%s>" %(province_name,city_name))
                        # 打印区县菜单
                        print("+-----------------------------------+")
                        for area_item in area_list:
                            print("  %s、%s" %area_item)
                        print("+-----------------------------------+")
                        # 获取用户输入
                        area = input("请输入你的区/县（输入'q'退出系统，输入'b'返回上一级菜单）：").strip()
                        # 判断用户输入
                        if area == 'q':
                            # 如果是q，关闭省、市、区县一级循环开关，也就是退出系统
                            area_flag = False
                            city_flag = False
                            province_flag = False
                        elif area == 'b':
                            # 如果是b，关闭县一级循环开关，继续市循环
                            area_flag = False
                        elif area in areas[city_name]:
                            # 如果输入正确
                            # 获取区县名称
                            area_name = areas[city_name][area]
                            # 输出完整的三级菜单选择信息
                            input('您选择的是%s，%s，%s。选择任意键退出系统' %(province_name, city_name, area_name))
                            # 关闭省、市、区县循环开关，退出系统
                            area_flag = False
                            city_flag = False
                            province_flag = False
                        else:
                            # 如果区县选项输入错误提示错误
                            input("输入错误请重新输入，输入任意键继续")
                else:
                    # 如果市选项输入错误提示错误
                    input("输入错误请重新输入，输入任意键继续")
        else:
            # 如果省选项输入错误提示错误
            input("输入错误请重新输入，输入任意键继续")