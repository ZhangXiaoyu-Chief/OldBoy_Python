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
        self.__cash = leading_role_info['cash']
        self.__deposit = leading_role_info['deposit']
        self.__hp = leading_role_info['hp']
        self.__rp = leading_role_info['rp']
        self.__ndays = leading_role_info['ndays']
        self.__goods_list = leading_role_info['goods_list']
        self.__max_goods_list = leading_role_info['max_goods_list']
        self.__goods_total_count = 0
        self.__one_day_cash = 0



    def get_name(self):
        return self.name
    def get_info(self):
        # print('ss')
        role_info = (self.name, self.__hp, self.__rp, self.__cash, self.__deposit, self.__goods_total_count, self.__max_goods_list, self.__ndays)
        return role_info
    def think(self, msg):
        input(mylib.color(msg, 32))

    def get_goods_list(self):
        return self.__goods_list

    def get_free_count(self):
        return self.__max_goods_list - self.__goods_total_count

    def find_goods_count(self, goods_name):
        for item in self.__goods_list:
            if item['name'] == goods_name:
                return item['count']
        pass
    def get_cash(self):
        return self.__cash

    def buy_goods(self, goods_name, count, price):
        pass
        for goods in self.__goods_list:
            if goods['name'] == goods_name:
                goods['count'] += count
                break
        else:
            tmp_goods = {}
            tmp_goods['name'] = goods_name
            tmp_goods['count'] = count
            self.__goods_list.append(tmp_goods)
        self.__goods_total_count += count
        self.__one_day_cash -= price
        self.__cash -= price
    def sale_goods(self, goods_name, count, price):
        for goods in self.__goods_list:
            if goods['name'] == goods_name:
                if goods['count'] == count:
                    self.__goods_list.remove(goods)

                else:
                    goods['count'] -= count
            break
        self.__goods_total_count -= count
        self.__one_day_cash += price
        self.__cash += price


    def go_one_day(self):
        import random
        self.__ndays += 1
        if self.__deposit >= 0:
            deposit = self.__deposit + int(self.__deposit * conf.INTERESTS)
            self.__deposit = deposit
        hp_del = random.randrange(1, 4)
        self.__hp -= hp_del
        cash = self.__one_day_cash if self.__one_day_cash <= 0 else '+%s' %self.__one_day_cash
        input('一天过去了，%s的现银 %s' % (self.name, cash))

        self.__one_day_cash = 0


    def pay(self, money):
        if self.__cash > money:
            self.__cash -= money
            self.__one_day_cash -= money

    def add_hp(self, hp):
        if self.__hp + hp > conf.MAX_HP:
            self.__hp = conf.MAX_HP
        else:
            self.__hp += hp

    def add_rp(self):
        import random
        rp = random.randrange(1, 5)
        if self.__rp + rp > conf.MAX_RP:
            self.__rp = conf.MAX_RP
        else:
            self.__rp += rp
        return rp

    def get_hp(self):
        return self.__hp

    def depo(self, money):
        self.__deposit += money
        self.__cash -= money

    def take_cash(self, money):
        self.__cash += money
        self.__deposit -= money

    def get_deposit(self):
        return self.__deposit

class wanqing(role):
    def __init__(self, name):
        super(wanqing, self).__init__(name)
        self.__love = 0

    def get_love(self):
        return self.__love

    def get_name(self):
        return self.name

    def add_love(self, name):
        import random
        love = random.randrange(1, 5)
        self.__love += love
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
        #   plist[rd] = ( int )( plist[rd] * news_list[news_id].impact );
        # }
        # else if( news_list[news_id].impact < 0 ){
        #
        #   plist[rd] = ( int )( plist[rd] / ( -news_list[news_id].impact ) );
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