#!/usr/bin/env python
# coding:utf-8
from conf import conf
from libs import mylib
'''
角色模块，分为一般角色，猪脚、女猪脚、和商人
'''

class role(object):
    '''
    角色类，用于一般角色，只有说话方法
    '''
    def __init__(self, name):
        '''
        构造方法
        :param name: 姓名
        :return:
        '''
        self.name = name

    def say(self, msg):
        '''
        说话方法
        :param msg: 说的话
        :return: 返回说话是输入内容，用于角色间的交互
        '''
        return input('%s: %s' %(self.name, msg))


class leading_role(role):
    '''
    主角类，继承自role（一般角色类）
    '''
    def __init__(self, leading_role_info):
        '''
        主角构造方法
        :param leading_role_info: 包含用户信息的字典，除了姓名，其他均来自配置文件
        :return:
        '''
        super(leading_role, self).__init__(leading_role_info['name'])

        self.__cash = leading_role_info['cash'] # 现金
        self.__deposit = leading_role_info['deposit'] # 存款
        self.__hp = leading_role_info['hp'] # 生命值
        self.__rp = leading_role_info['rp'] # 声望
        self.__ndays = leading_role_info['ndays'] # 穿越天数
        self.__goods_list = leading_role_info['goods_list'] # 包裹列表
        self.__max_goods_list = leading_role_info['max_goods_list'] # 包裹容量，做多可以存放多少商品
        self.__goods_total_count = 0 # 包裹内商品总数，用于判断空间是否够等
        self.__one_day_cash = 0 # 一天内现金的消费统计

    def get_name(self):
        '''
        获取姓名方法
        :return: 姓名
        '''
        return self.name
    def get_info(self):
        '''
        获取主角基本星系方法
        :return: 基本信息
        '''
        # print('ss')
        role_info = (self.name, self.__hp, self.__rp, self.__cash, self.__deposit, self.__goods_total_count, self.__max_goods_list, self.__ndays)
        return role_info

    def think(self, msg):
        '''
        想方法，主角的内心活动
        :param msg: 想的内容
        :return:
        '''
        input(mylib.color(msg, 32))

    def get_goods_list(self):
        '''
        获取包裹物品列表
        :return: 包裹列表
        '''
        return self.__goods_list

    def get_free_count(self):
        '''
        获取包裹剩余空间方法
        :return: 剩余空间
        '''
        return self.__max_goods_list - self.__goods_total_count

    def find_goods_count(self, goods_name):
        '''
        获取包裹内某一个物品的数量方法
        :param goods_name: 物品名称
        :return: 如果包裹内存在改物品，放回数量，如果不存在则放回None
        '''
        for item in self.__goods_list: # 遍历包裹
            if item['name'] == goods_name: # 判断是否是要找的物品
                return item['count'] # 是则放回数量

    def get_cash(self):
        '''
        获取现金方法
        :return: 现金
        '''
        return self.__cash

    def buy_goods(self, goods_name, count, price):
        '''
        购买物品方法
        :param goods_name: 商品名称
        :param count: 购买的数量
        :param price: 该商品的价格
        :return: 无
        '''
        for goods in self.__goods_list: # 遍历商品列表
            if goods['name'] == goods_name: # 判断商品名是否相等
                goods['count'] += count # 数量相加
                break
        else:
            # 如果不存在，新建包裹项目
            tmp_goods = {}
            tmp_goods['name'] = goods_name
            tmp_goods['count'] = count
            self.__goods_list.append(tmp_goods)
        # 计算新的商品总数
        self.__goods_total_count += count
        # 每天花费的现金总数递减
        self.__one_day_cash -= price
        # 计算新的现金总数
        self.__cash -= price

    def sale_goods(self, goods_name, count, price):
        '''
        售出商品方法
        :param goods_name: 商品名
        :param count: 售出总量
        :param price: 单价
        :return:
        '''
        for goods in self.__goods_list: # 遍历包裹列表
            if goods['name'] == goods_name: # 判断是否存在
                if goods['count'] == count: # 如果包裹内的数量等于售出的数量，移除包裹
                    self.__goods_list.remove(goods)
                else:
                    goods['count'] -= count # 否则商品数量递减
            break
        # 计算新的商品总数
        self.__goods_total_count -= count
        # 每天花费的现金总数递加
        self.__one_day_cash += price
        # 计算新的现金总数
        self.__cash += price


    def go_one_day(self):
        '''
        过了一天方法，调用该方法说明过了一天
        :return: 无
        '''
        import random
        self.__ndays += 1 # 穿越天数+1
        # 判断是否有存款，有则计算利息
        if self.__deposit >= 0:
            deposit = self.__deposit + int(self.__deposit * conf.INTERESTS)
            self.__deposit = deposit
        # 随机减少生命值
        hp_del = random.randrange(1, 4)
        self.__hp -= hp_del
        # 统计花销
        cash = self.__one_day_cash if self.__one_day_cash <= 0 else '+%s' %self.__one_day_cash
        input('一天过去了，%s的现银 %s' % (self.name, cash))
        # 清空每日花销统计
        self.__one_day_cash = 0


    def pay(self, money):
        '''
        支付现金方法，用于逛妓院啥的付费用
        :param money: 金额
        :return:
        '''
        if self.__cash > money:
            self.__cash -= money
            self.__one_day_cash -= money

    def add_hp(self, hp):
        '''
        加生命方法
        :param hp: 加的生命值
        :return:
        '''
        if self.__hp + hp > conf.MAX_HP:
            self.__hp = conf.MAX_HP
        else:
            self.__hp += hp

    def add_rp(self):
        '''
        加声望方法，随机
        :return:
        '''
        import random
        rp = random.randrange(1, 5)
        if self.__rp + rp > conf.MAX_RP:
            self.__rp = conf.MAX_RP
        else:
            self.__rp += rp
        return rp

    def get_hp(self):
        '''
        获取生命值方法
        :return:
        '''
        return self.__hp

    def depo(self, money):
        '''
        存款方法
        :param money: 金额
        :return:
        '''
        self.__deposit += money
        self.__cash -= money

    def take_cash(self, money):
        '''
        取款方法
        :param money: 金额
        :return:
        '''
        self.__cash += money
        self.__deposit -= money

    def get_deposit(self):
        '''
        获取存款方法
        :return:
        '''
        return self.__deposit

    def get_total(self):
        return self.__deposit + self.__cash

class wanqing(role):
    '''
    女主角类，由于我太喜欢木婉清这个角色，所以类名以木婉清命名
    '''
    def __init__(self, name):
        '''
        构造方法
        :param name:
        :return:
        '''
        super(wanqing, self).__init__(name)
        # 爱慕值
        self.__love = 0

    def get_love(self):
        '''
        获取爱慕值方法
        :return: 爱慕值
        '''
        return self.__love

    def get_name(self):
        '''
        获取姓名方法
        :return: 姓名
        '''
        return self.name

    def add_love(self, name):
        '''
        增加爱慕值方法（随机）
        :param name: 爱慕的人姓名，用于输出
        :return:
        '''
        import random
        love = random.randrange(1, 5)
        self.__love += love
        input('%s对%s爱慕之情+%s' %(self.name, name, love))

class seller(role):
    '''
    商人类，
    '''
    def __init__(self, name):
        super(seller, self).__init__(name)
        self.__prices = self.__get_prices()

    def __get_prices(self):
        '''
        获取价格列表方法，商品的价格通过是通过商品的最大价格和最小价格通过随机的系数计算出来的
        :return: 价格列表
        '''
        import random
        prices = [] # 创建空的价格理列表
        for num, goods in enumerate(conf.GOODS_list, 1): # 遍历商品列表
            # 计算价格
            price = goods['min'] + random.random() * (goods['max'] - goods['min'] + 1)
            prices.append(int(price))
        return prices

    def say_news(self):
        '''
        说新闻方法
        :return: 无
        '''
        # 调用__random_news()获得新闻及重新计算收到新闻影响的商品价格
        msg = self.__random_news()
        input('%s: %s' %(self.name, msg))

    def get_prices(self):
        '''
        获取价格列表方法，用于外部调用
        :return:
        '''
        return self.__get_prices()

    def __random_news(self):
        '''
        获取随机新闻方法
        :return: 新闻内容
        '''
        import random
        news_list = conf.NEWS_LIST # 获取新闻列表
        # 随机产生收到影响的商品索引
        rd = random.randrange(0, len(self.__prices))
        # 计算新闻索引值
        news_id = rd * 4 + random.randrange(0, 4)
        # 获取新闻
        news = news_list[news_id]
        # 根据对商品的影响度，重新计算收到影响的商品价格
        if news['impact'] > 0:
            self.__prices[news['id']] = int(self.__prices[news['id']] * news['impact'])
        else:
            self.__prices[news['id']] = int(self.__prices[news['id']] / (-news['impact']))
        return news['msg']