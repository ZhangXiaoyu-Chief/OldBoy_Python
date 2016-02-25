#!/usr/bin/env python
# coding:utf-8
from conf import conf
from model import role
from libs import  mylib
'''
主逻辑模块
'''

# 初始化猪脚和女猪脚对象
me = None
wanqing = None

def play_main():
    '''
    主界面函数
    '''
    global me
    global wanqing
    role_info = me.get_info() # 获取主角信息
    main_map = '''
返回主菜单(r)  存档(s)   查看背包(p)
%s: 生命 %s/%s   声望 %s/%s   现银 %s   银票 %s  背包 %s/%s   穿越天数 %s   爱情 %s
---------------------------------------------------------------------------------------
                              北市(2)
                        |                    |
            钱庄(1)     |                    |      木婉清的家(3)
                        |                    |
    --------------------+                    +---------------------

西市(4)                           %s                         东市(5)

    --------------------+                    +---------------------
                        |                    |
           医馆(6)      |                    |     丽春院(8)
                        |                    |
                             南市(7)
    ''' %(role_info[0], role_info[1], conf.MAX_HP, role_info[2], conf.MAX_RP, role_info[3], role_info[4], role_info[5], role_info[6],role_info[7], wanqing.get_love(), role_info[0])
    print(main_map)

def show_goods_list(*args):
    '''
    显示包裹列表方法
    :param args:
    :return:
    '''
    global me
    #print(me.get_goods_list())
    goods_list = me.get_goods_list()
    print('背包：')
    if goods_list:

        for num , line in enumerate(goods_list, 1):
            print('%s %s %s' %(mylib.myrjust(str(num), 5), mylib.myljust(line['name'], 10), line['count']))
    else:
        print('背包里空空如也')
    input('按任意键返回主界面')


def save_game(*args):
    '''
    保存游戏函数
    :param args:
    :return:
    '''
    global me
    global wanqing
    import shelve
    # 通过模块将猪脚和女猪脚的对象序列化保存
    sw = shelve.open('save/save.pkl')
    sw['me'] = me
    sw['wanqing'] = wanqing
    sw.close()

def new_game():
    '''
    新游戏函数，用来交代游戏背景，初始化猪脚和女猪脚对象
    :return:
    '''
    global me
    global wanqing

    me = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    wanqing = role.wanqing('木婉清')
    name = input('请输入玩家的姓名: ').strip()
    if name:
        me.name = name
    input('我叫%s,' % me.name)
    for item in conf.STORY:
        input(item)
    #wanqing = role.role('木婉清')
    wanqing.say('太好了你终于醒了')
    me.say('这里是哪儿？我为什么会在这里？')
    wanqing.say('这是我的家，我在上山采药的时候发现了你。')
    me.think('欧系吧！难道我穿越了？？')
    input('从后来的交谈中，我知道她叫木婉清，是个苦命的女子，父母双亡')
    wanqing.say('这里有现银%s，你拿去做个小生意吧' %me.get_info()[3])
    me.say('姑娘，我今生必不负你')
    input('木婉清脸上害羞的红了起来')
    wanqing.say('嗯，...')
    input('于是我出了姑娘的屋子，来到街上')
    # 调用主函数，开始游戏
    main()

def main():
    '''
    主函数，游戏各个函数的调用
    :return:
    '''
    global me
    flag = True
    while flag:
        is_game_over() # 执行游戏结束函数，如果符合结束条件则结束游戏，如果不符合继续
        play_main() # 显示主界面
        chose = input('>> ').strip() # 获取玩家输入的操作
        # 操作函数字典，用来通过通过输入调用不同的函数
        main_menu_do = {"1" : bank, "2" : market, "3" : home, "4" : market, "5" : market, "6" : hospital, "7" : market, "8": lichun, "s" : save_game, "p" : show_goods_list}
        if chose in main_menu_do.keys():
            main_menu_do[chose](chose)
        elif chose == 'r':
            flag = False
        else:
            input('输入错误，按回车继续')

def buy_goods(seller, goods, price):
    '''
    购买函数，用于市场函数调用
    :param seller: 商贩对象
    :param goods: 商品
    :param price: 价格
    :return:
    '''
    global me
    import re
    while True:
        count = seller.say('你要多少(返回r)>> ').strip() # 获取购买的数量
        if count == 'r': # 如果输出的是r退出循环
            return False
        me.say(count) #
        if re.match('^\d+$', count):
            # 获取空闲空间
            free_count = me.get_free_count()
            # 获取现金
            cash = me.get_cash()
            # 计算总价
            total = price * int(count)

            if int(total) <= cash:# 判断现金是否够
                if int(count) <= free_count: # 判断空闲空间是否够
                    # 调用主角buy_goods方法完成购买
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

def sale_goods( seller, goods, price):
    '''
    出售商品函数，用于市场函数调用
    :param seller: 商贩对象
    :param goods: 商品
    :param price: 价格
    :return:
    '''
    global me
    import re
    while True:
        count = seller.say('你要卖多少(返回r)>> ').strip() # 获取用户输入的出售悢
        if count == 'r':
            return False
        me.say(count)
        if re.match('^\d+$', count):
            # 获取包裹内该商品的数量
            max_count = me.find_goods_count(goods['name'])
            # 获取总价
            total = price * int(count)
            if int(count) <= max_count: # 判断用户是否有足够的该商品
                seller.say('好嘞，客官，这是您的%s两银子' %total)
                me.sale_goods(goods['name'], int(count), total) # 调用猪脚的sale_goods方法出售商品
                return True
            else:
                seller.say('客官，您的背包好像没有那么多%s吧' %goods['name'])
                me.say('对哦，我再考虑一下')
        else:
            seller.say('客官，我听不懂你说什么，Can you speak chinese？')


def hospital( *args):
    '''
    医馆函数，用户主函数的调用
    :param args: 无
    :return:
    '''
    global me
    doctor = role.role('江湖郎中')
    doctor.say('老夫人称华佗在世，当年可是御医，专门给后宫的娘娘看妇科的')
    me.think('妇科？？什么鬼？')
    doctor.say('这位客官，有何贵干')
    me.think('废话，找你当然是看病了')
    me.say('大夫，我不太舒服')
    doctor.say('来来来，我给你号号脉')
    input('过了一盏茶的功夫')
    if me.get_hp() == conf.MAX_HP: # 判断用户生命值是否是满的
        doctor.say('这位客官，我看你脉象平稳，不像得了什么病，您是来消遣老夫的吗？')
    else:
        doctor.say('这位客官，你没什么大碍，只是有些肾亏，我给你开几服药调养调养就好了')
        doctor.say('一共需要100两')
        # 判断猪脚现金是否够
        if me.get_cash() > 100:
            me.pay(100) # 支付银子
            me.add_hp(5) # 加生命值
            me.say('啥？这么贵，真是黑心')
            input('不情愿的交了银子走了')
        else:
            # 现金不够，赶出去
            me.say('我没那么多银子啊')
            doctor.say('没银子还来看病，滚')
            me.say('此处不留爷，自有留爷处')


def deposit(zhanggui):
    '''
    开银票（存款）函数，用于钱庄函数调用
    :param zhanggui: 掌柜对象
    :return:
    '''
    global me
    import re
    while True:
        money = zhanggui.say('您要开多少的银票>> ').strip()
        me.say(money)
        if re.match('^\d+$', money):
            if me.get_cash() >= int(money): # 判断现金是否够
                zhanggui.say('客官，这是您%s两的银票，您收好了，欢迎您再来' %money)
                me.depo(int(money)) # 调用猪脚存款方法
                return True
            else:
                zhanggui.say('客官，您的现银好像不够吧')
                me.say('是哦，我再想想')
        else:
            zhanggui.say('客官，我听不懂你说什么，Can you speak chinese？')

def take_cash(zhanggui):
    '''
    提现函数，用于钱庄函数调用
    :param zhanggui: 掌柜对象
    :return:
    '''
    global me
    import re
    while True:
        money = zhanggui.say('您要兑换多少现银>> ').strip() # 获取提现金额
        me.say(money)
        if re.match('^\d+$', money):
            if me.get_deposit() >= int(money): # 判断存款金额是否够
                zhanggui.say('客官，这是您%s两的银子，您收好了，欢迎您再来' %money)
                #print(me.deposit)
                me.take_cash(int(money)) # 调用猪脚提现函数
                return True
            else:
                zhanggui.say('客官，您的银票好像不够吧')
                me.say('是哦，我再想想')
        else:
            zhanggui.say('客官，我听不懂你说什么，Can you speak chinese？')

def bank(*args):
    '''
    钱庄函数，用于主函数调用
    :param args:
    :return: 无
    '''
    global me
    zhanggui = role.role('钱庄掌柜') # 定义掌柜对象
    chose = zhanggui.say('客官，您是开银票(1)还是兑换银票(2)(退出0)>> ').strip() # 获取用户交互输入，办什么业务
    chose_do = {"1" : deposit, "2" : take_cash} # 业务函数字典，用来执行对应的函数
    flag = True

    while flag:
        if chose in chose_do.keys(): # 获取用户业务选择
            if chose == '1':
                me.say('开银票')
                if chose_do[chose](zhanggui):
                    break
            else:
                me.say('兑换银票')
                if chose_do[chose](zhanggui):
                    break
        # 如果输入的0返回主界面
        elif chose == '0':
            zhanggui.say('啥都不干进来干毛线啊，出去')
            me.say('此处不留爷，自由留爷处')
            break
        else:
            chose = zhanggui.say('客官，我听不懂你说什么，Can you speak chinese？您是开银票(1)还是兑换银票(2)(退出0)>> ')


def market( market_id):
    '''
    市场函数，用于主函数调用
    :param market_id: 市场id，用来初始化不通市场的掌柜名
    :return:
    '''
    global me
    is_do = False # 用来判断猪脚是否买卖物品
    goods_list = conf.GOODS_list # 获取商品列表
    names = {"2" : "北市商贩", "4" : "西市商贩", "5" : "东市商贩", "7" : "南市商贩"} # 掌柜名字典
    seller = role.seller(names[market_id]) # 创建商贩列表
    seller.say_news() # 说新闻
    prices = seller.get_prices() # 获取价格列表
    seller.say('客官，您需要点什么，我这里应有皆有，价格公道')
    me.say('我看看')

    while True:
        # 遍历商品列表输出商品列表
        for num, goods in enumerate(goods_list, 1):
            print('%s %s %s' %(num, goods['name'], prices[num - 1]))
        print('0 退出')
        chose = input('>> ').strip() # 获取用户输入选项
        chose_do_menu = {'1' : buy_goods, '2' : sale_goods } # 操作字典（买或者卖）
        if chose in map(lambda x:str(x), range(1, len(goods_list))):  # 判断是否是商品序号
            chose_goods = goods_list[int(chose) - 1] # 获取序号对应的商品
            me.say('%s' %chose_goods['name'])
            chose_do = seller.say('%s？您是买(1)还是卖(2)(返回0) >>' %chose_goods['name']).strip() # 获取用户操作
            while True:
                if chose_do in chose_do_menu.keys():
                    if(chose_do_menu[chose_do](seller, chose_goods, prices[int(chose) - 1])): # 调用操作对应的函数
                        seller.say('客官您还看点啥')
                        is_do = True # 说明买卖商品了
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
                    chose_do = seller.say('客官，我听不懂你说什么，Can you speak chinese？您是买(1)还是卖(2)(返回0) >> ').strip()
        elif chose == '0':
            if is_do: # 判断是否进行过交易
                seller.say("客官，欢迎您下次再来")
            else:
                # 没有赶出去
                seller.say('啥都不干进来干吗，去去去')
                me.say('此处不留爷，自有留爷处')
            me.go_one_day() # 退出市场函数的话，调用猪脚的go_one_day()方法过去一天
            break
        else:
            me.say(chose)
            seller.say('客官，Can you speak chinese？')

def home(*args):
    '''
    木婉清家函数，用于主函数调用
    :param args:
    :return:
    '''
    global me
    global wanqing
    wanqing.say('%s哥哥，你回来了，人家一个人在家好无聊啊，每人陪我玩' %me.get_info()[0])
    me.say('%s妹妹，我也想你啊，我这不是回来看你了吗' %wanqing.get_name())
    wanqing.say('嗯嗯，这次回来你要好好陪人家玩')
    me.say('好的')
    input('于是%s，今天没有出外谋生，赔了%s一天' %(me.get_info()[0], wanqing.get_name()))
    wanqing.add_love(me.get_info()[0]) # 对猪脚爱慕增加
    me.go_one_day() # 过去一天

def lichun(*args):
    '''
    丽春院函数，用于主函数调用
    :param args:
    :return:
    '''
    global me
    laobao = role.role('老鸨') # 生成老鸨对象
    if me.get_cash() <= conf.PROSTITUTE_PRICE: # 判断金额是否够
        # 不够，赶出去
        laobao.say('去去去，我们这里招呼要饭的')
        me.say('此处不留爷，自有留爷处')
    else:
        # 够
        laobao.say('这位爷，进里面玩玩啊')
        me.say('把你们这里最漂亮的姑娘找来，大爷我有的是银子')
        laobao.say('这位爷，里面请，春花、秋月、如烟下来招呼这位大爷')
        ruyan = role.role('如烟')
        ruyan.say('大爷~~，里面请，奴家好好服侍您')
        me.say('是吗？？哈哈哈')
        add_rp = me.add_rp() # 调用猪脚的加声望函数
        input('一场风花雪月之后，%s的声望+%s' %(me.get_info()[0], add_rp))
        me.pay(conf.PROSTITUTE_PRICE) # 付款函数
        me.go_one_day() # 过了一天


def reload_game():
    '''
    读进度函数，通过shelve模块读取进度
    :return:
    '''
    global me
    global wanqing
    import shelve

    try:
        sr = shelve.open(conf.SAVE_FILE)
        me = sr['me']
        wanqing = sr['wanqing']

        sr.close()
        main()
    except Exception:
        input('对不起，进度读取失败，进度文件受存或不存在，按回车继续')

def exit_game():
    '''
    退出游戏函数
    :return: True,说明退出游戏了
    '''
    input('欢迎下次来玩，再见')
    return True
def print_game_info():
    '''
    打印游戏信息函数
    :return: 无
    '''
    game_info = '''
--------------------------------------
 版本：1.0
 作者：张晓宇
 Email：61411916@qq.com
 QQ：61411916
 Blog：http://www.cnblogs.com/zhangxiaxuan/
--------------------------------------
    '''
    input(game_info)


def print_main_menu():
    '''
    打印游戏总菜单函数
    :return:
    '''
    main_menu = ['新的游戏', '旧的记忆', '制作人员', '退出游戏']
    game_info='''
**********************************
 穿越明朝之明朝那些事儿
 Version 1.0
 作者：张晓宇
**********************************'''
    print(game_info)
    for menu in enumerate(main_menu):
        print(menu[0]+1, menu[1])

def is_game_over():
    '''
    判断游戏是否结束函数，如果结束输出结局
    :return:
    '''
    global me
    global wanqing
    info = me.get_info()
    is_go_bak = False
    if info[7] == conf.OVER_DAY:
        input('这一天，晚上%s做了一个梦' %info[0])
        chose = input('梦里有个声音对他说“%s 你可以回去了，你是否愿意回到你的世界（y/n）”>> ' %info[0])
        while True:
            if chose == 'y':
                is_go_bak = True
                input('%s看了一眼%s，满脸泪水的说' %(info[0], wanqing.get_name()))
                me.say('对不起，我要回去，这些银两够你过后半辈子了，找个好人家嫁了吧')
                wanqing.say('不要，为了我留下来吧')
                me.say('对不起，我做不到，我更爱我的女朋友，对不起')
                wanqing.say('......')
                input('于是，%s追随者声音的方向回到了他的时代' %info[0])
                input('和他的韩梅梅结婚，一起幸福到老')
                exit(0)
            elif chose == 'n':
                input('%s看了一眼%s，坚定的说' %(info[0], wanqing.get_name()))
                me.say('我不回去了，这里挺好')
                input('于是%s留到了明朝' %info[0])
                if info[2] >= conf.MAX_RP:
                    input('这里%s非常受到人们的爱戴' %info[0])
                if me.get_total() >= conf.WIN_CASH:
                    input('由于%s的努力经营，成为一个富商' %info[0])
                if wanqing.get_love() >= conf.WIN_LOVE:
                    input('最终和%s幸福的在一起' %wanqing.get_name())
                exit(0)
            else:
                chose = input('你说什么，Can you speak chinese？>>')
    if info[1] <= conf.LOSE_HP:
        input('由于%s太拼命挣钱，不注意身体，最终晕倒在街头，再也没有起来' %info[0])





def run():
    '''
    run函数，整个模块的入口，用于主文件调用
    :return:
    '''
    # role_1 = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    # print(role_1.get_name)

    # role_1.say('testing')
    main_menu_do = {"1":new_game, "2":reload_game, "3":print_game_info, "4":exit_game} # 主材单函数列表

    flag = True
    while flag:
        print_main_menu()
        chose = input('\n>> ')
        if chose in main_menu_do.keys():
            if main_menu_do[chose]():
                break
        else:
            input('输入错误，按回车继续')