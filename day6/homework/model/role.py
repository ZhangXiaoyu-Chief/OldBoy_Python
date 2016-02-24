#!/usr/bin/env python
# coding:utf-8
from conf import conf
from libs import mylib

class role(object):
    def __init__(self, name):
        self.name = name

    def say(self, msg):
        return input('%s: %s' %(self.name, msg))


class leading_role(role):
    def __init__(self, leading_role_info):
        super(leading_role, self).__init__(leading_role_info['name'])
        #self.name = leading_role_info['name']
        self.cash = leading_role_info['cash']
        self.deposit = leading_role_info['deposit']
        self.debt = leading_role_info['debt']
        self.hp = leading_role_info['hp']
        self.rp = leading_role_info['rp']
        self.level = leading_role_info['level']
        self.ndays = leading_role_info['ndays']
        self.goods_list = leading_role_info['goods_list']
        self.max_goods_list = leading_role_info['max_goods_list']
        self.goods_total_count = 0
        self.one_day_cash = 0



    def get_name(self):
        return self.name
    def get_info(self):
        # print('ss')
        role_info = (self.name, self.hp, self.rp, self.cash, self.deposit, self.goods_total_count, self.ndays)
        return role_info
    def think(self, msg):
        input(mylib.color(msg, 32))

    def get_free_count(self):
        return self.max_goods_list - self.goods_total_count

    def find_goods_count(self, goods_name):
        for item in self.goods_list:
            if item['name'] == goods_name:
                return item['count']
        pass
    def get_cash(self):
        return self.cash

    def buy_goods(self, goods_name, count, price):
        pass
        for goods in self.goods_list:
            if goods['name'] == goods_name:
                goods['count'] += count
                break
        else:
            tmp_goods = {}
            tmp_goods['name'] = goods_name
            tmp_goods['count'] = count
            self.goods_list.append(tmp_goods)
        self.goods_total_count += count
        self.one_day_cash -= price
        self.cash -= price
    def sale_goods(self, goods_name, count, price):
        for goods in self.goods_list:
            if goods['name'] == goods_name:
                if goods['count'] == count:
                    self.goods_list.remove(goods)

                else:
                    goods['count'] -= count
            break
        self.goods_total_count -= count
        self.one_day_cash += price
        self.cash += price


    def go_one_day(self):
        import random
        self.ndays += 1
        if self.deposit >= 0:
            deposit = self.deposit + int(self.deposit * conf.INTERESTS)
            self.deposit = deposit
        hp_del = random.randrange(1, 4)
        self.hp -= hp_del
        input('一天过去了，%s的现银 %s，hp -%s' % (self.name, self.one_day_cash, hp_del))

        self.one_day_cash = 0


    def pay(self, money):
        if self.cash > money:
            self.cash -= money

    def add_hp(self, hp):
        if self.hp + hp > 100:
            self.hp = 100
        else:
            self.hp += hp

    def get_hp(self):
        return self.hp

    def depo(self, money):
        self.deposit += money
        self.cash -= money

    def take_cash(self, money):
        self.cash += money
        self.deposit -= money

    def get_deposit(self):
        return self.deposit

class wanqing(role):
    def __init__(self, name):
        super(wanqing, self).__init__(name)
        self.love = 0

    def get_love(self):
        return self.love

    def get_name(self):
        return self.name

    def add_love(self, name):
        import random
        love = random.randrange(1, 5)
        self.love += love
        input('%s对%s爱慕之情+%s' %(self.name, name, love))

class seller(role):
    def __init__(self, name):
        super(seller, self).__init__(name)
        self.__prices = self.__get_prices()

    def __get_prices(self):
        import random
        prices = []
        for num, goods in enumerate(conf.GOODS_list, 1):
            price = goods['min'] + random.random() * (goods['max'] - goods['min'] + 1)
            prices.append(int(price))
        return prices

    def say_news(self):
        msg = self.__random_news()
        input('%s: %s' %(self.name, msg))
    def get_prices(self):
        return self.__get_prices()

    def __random_news(self):
        import random
        news_list = conf.NEWS_LIST
        # int rd = rand32() % GOODS_LIST_MAX;
        #
        # system( "cls" );
        #
        # puts( "-北京新闻播报-\n" );
        #
        # //随机选择新闻
        # int news_id = rlist[rd] * 4 + rand32() % 4;
        rd = random.randrange(0, len(self.__prices))
        news_id = rd * 4 + random.randrange(0, 4)
        # print(len(news_list))
        #news = news_list[random.randrange(0, 35585 ) % len(news_list)]
        news = news_list[news_id]
        # if( news_list[news_id].impact > 0 ){
        #
        # 	plist[rd] = ( int )( plist[rd] * news_list[news_id].impact );
        # }
        # else if( news_list[news_id].impact < 0 ){
        #
        # 	plist[rd] = ( int )( plist[rd] / ( -news_list[news_id].impact ) );
        # }

        if news['impact'] > 0:
            # print(prices[news['id']])
            self.__prices[news['id']] = int(self.__prices[news['id']] * news['impact'])
            # print(prices[news['id']])
        else:
            # print(prices[news['id']])
            self.__prices[news['id']] = int(self.__prices[news['id']] / (-news['impact']))
            # print(prices[news['id']])
        #print('---世界消息---')
        # input(news['msg'])
        return news['msg']