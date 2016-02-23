#!/usr/bin/env python
# coding:utf-8
from conf import conf
from model import role

def print_main(leading_role):
    pass
    role_info = leading_role.get_info()

    main_map = '''
返回主菜单(r)  存档(s)   查看背包(p)
%s: 生命 %s   声望 %s   现银 %s   银票 %s   欠账 %s   level %s %s %s   穿越天数 %s
---------------------------------------------------------------------------------
                              北市(2)
                        |                    |
            钱庄(1)     |                    |      木婉清的家(3)
                        |                    |
    --------------------+                    +---------------------

西市(4)                           我                            东市(5)

    --------------------+                    +---------------------
                        |                    |
           医馆(6)      |                    |     丽春院(8)
                        |                    |
                             南市(7)
    ''' %(role_info[0], role_info[1], role_info[2], role_info[3], role_info[4], role_info[5], role_info[6], role_info[7], role_info[8], role_info[9])
    print(main_map)

def new_game():
    me = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    name = input('请输入玩家的姓名: ').strip()
    if name:
        me.name = name
    # input('我叫%s,' % me.name)
    # for item in conf.STORY:
    #     input(item)
    # wanqing = role.role('木婉清')
    # wanqing.say('太好了你终于醒了')
    # me.say('这里是哪儿？我为什么会在这里？')
    # wanqing.say('这是我的家，我在上山采药的时候发现了你。')
    # me.think('欧系吧！难道我穿越了？？')
    # input('从后来的交谈中，我知道她叫木婉清，是个苦命的女子，父母双亡')
    # wanqing.say('这里有现银%s，你拿去做个小生意吧' %me.cash)
    # me.say('姑娘，我今生必不负你')
    # input('木婉清脸上害羞的红了起来')
    # wanqing.say('嗯，...')
    # input('于是我出了姑娘的屋子，来到街上')
    flag = True
    while flag:
        print_main(me)
        chose = input('>> ').strip()
        main_menu_do = {"2":market}
        if chose in main_menu_do.keys():
            main_menu_do[chose](me)
        if chose == 'r':
            flag = False

def buy_goods(me, seller, goods, price):
    import re


    while True:
        count = seller.say('你要多少(返回r)').strip()

        if count == 'r':
            return False
        me.say(count)
        if re.match('^\d+$', count):
            max_count = me.get_goods_count()
            cash = me.get_cash()
            total = price * int(count)
            if int(total) <= cash:
                if int(count) <= max_count:
                    seller.say('好嘞，客官，这是您的%s个%s' %(count, goods['name']))
                    me.buy_goods(goods['name'], int(count), total)
                    return True
                else:
                    seller.say('客官，您的背包好像没那么多地儿啊')
                    me.say('对哦，我再考虑一下')
            else:
                seller.say('客官，您好像没那么多银子')
                me.say('对哦，我再考虑一下')





        else:
            seller.say('客官，我听不懂你说什么，Can you speak chinese？')
def sale_goods():
    pass


def market(me):
    import random
    goods_list = conf.GOODS_list
    # for( i = 0; i < GOODS_LIST_MAX; i++ ){
    #
	# 	plist[i] = goods_list[rlist[i]].min_price + rand32() % ( abs( goods_list[rlist[i]].max_price - goods_list[rlist[i]].min_price ) + 1 );
	# }
    prices = []
    for num, goods in enumerate(goods_list, 1):
        price = goods['min'] + random.random() * (goods['max'] - goods['min'] + 1)

        prices.append(int(price))
    seller = role.role('商贩')
    seller.say(random_news(prices))
    seller.say('客官，您需要点什么，我这里应有皆有，价格公道')
    me.say('我看看')

    # print(goods_list)
    # print(enumerate(goods_list, 1))




    while True:
        for num, goods in enumerate(goods_list, 1):
            print('%s %s %s' %(num, goods['name'], prices[num - 1]))
        print('0 退出')
        chose = input('>> ').strip()
        #chose in map(lambda x:str(int(x)+1),select_list)
        chose_do_menu = {'1' : buy_goods, '2' : sale_goods }
        if chose in map(lambda x:str(x), range(1, len(goods_list))):
            print(chose)
            chose_goods = goods_list[int(chose) - 1]
            print(chose_goods)
            me.say('%s' %chose_goods['name'])
            chose_do = seller.say('%s？您是买(1)还是卖(2)还是不要(0)' %chose_goods['name']).strip()
            while True:

                if chose_do in chose_do_menu.keys():
                    if(chose_do_menu[chose_do](me, seller, chose_goods, prices[int(chose) - 1])):
                        seller.say('客官您还看点啥')
                        break
                    else:
                        me.say('不不，还是不要%s了'  %chose_goods['name'])

                        seller.say('那您要啥？')
                        break
                elif chose_do == '0':
                    me.say('不要')
                    seller.say('不要您说什么，拿我消遣')
                    break
                else:
                    me.say(chose_do)
                    chose_do = seller.say('客官，我听不懂你说什么，Can you speak chinese？您是买(1)还是卖(2)还是不要(0)')

        elif chose == '0':
            seller.say("客官，欢迎您下次再来")
            me.go_one_day()
            print(me.goods_list)
            break
        else:
            me.say(chose)
            seller.say('客官，Can you speak chinese？')




def random_news(prices):
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
    rd = random.randrange(0, len(prices))
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
        prices[news['id']] = int(prices[news['id']] * news['impact'])
        # print(prices[news['id']])
    else:
        # print(prices[news['id']])
        prices[news['id']] = int(prices[news['id']] / (-news['impact']))
        # print(prices[news['id']])
    #print('---世界消息---')
    # input(news['msg'])
    return news['msg']





def reload_game():
    pass
def exit_game():
    pass
def print_game_info():
    pass
def exit_game():
    pass

def print_main_menu():
    #main_menu = {1:"新的游戏", 2:"旧的记忆", 3:"制作人员", 4:"退出游戏"}
    main_menu = ['新的游戏', '旧的记忆', '制作人员', '退出游戏']

    #print(enumerate(main_menu))
    for menu in enumerate(main_menu):
        print(menu[0]+1, menu[1])


def run():
    # role_1 = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    # print(role_1.get_name)

    # role_1.say('testing')
    main_menu_do = {"1":new_game, "2":reload_game, "3":print_game_info, "4":exit_game}

    flag = True
    while flag:
        print_main_menu()
        chose = input('\n>> ')
        if chose in main_menu_do.keys():
            main_menu_do[chose]()