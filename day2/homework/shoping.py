#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年1月12日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
import conf
from model.goods import goods
from model.customer import customer





def alignment(str1, space, align = 'left', chars = None):
    '''
    alignment用于中文英文混合模式字符串的对齐
    :param str1: 要对对齐的字符串
    :param space: 宽度
    :param align: 对齐方式：left左对齐、cente居中对齐、right右对齐
    :param chars: 填充字符
    :return: 返回调整后的字符串
    '''

    if chars == None:
        chars = ' '
    length = len(str1.encode('gb2312')) # 获取字符串转化为gb2312格式的编码后的长度，这样中文字符占用2个宽度，英文就占用1个宽度
    space = space - length if space >=length else 0
    if align == 'left':
        str1 = str1 + chars * space
    elif align == 'right':
        str1 = chars* space +str1
    elif align == 'center':
        str1 = chars * (space //2) +str1 + chars* (space - space // 2)
    return str1




def print_main_menu():
    MAIN_MENU = ['血拼','查看购物车','退出']
    print('欢迎%s，您当前余额为%s。祝您购物愉快\n------------------------------------' %(current_user_info['username'], current_user_info['balance']))
    for i in range(len(MAIN_MENU)):
        print(" %s、%s " %(str(i+1).rjust(2), MAIN_MENU[i]))

def print_goods_list(goods_list, page = 1):
    '''
    分页打印商品信息
    :param goods_list: 所有商品信息
    :param page: 页码
    :return: 当前页的商品的在商品列表的索引范围
    '''
    max_per_page = conf.max_per_page # 从配置文件获取每页最多显示多少个商品
    # list_index = [] # 初始化索引列表
    start = ((page - 1) * max_per_page)
    end = start + max_per_page
    goods_list_page = goods_list[start:end]
    # goods_list_page = goods_list[((page-1)*max_per_page):((page-1)*max_per_page+max_per_page)] # 通过每页最多显示的个数及页数计算范围进行切片
    print(' %s    %s%s    %s\n%s' %(alignment('商品编号',8), alignment('商品名称',50, ), alignment('价格',8, 'right'), '分类', ('-'*85)))
    for goods in goods_list_page:
        # 遍历切片后的商品列表进行输出
        print(' %s    %s%s    %s' %(goods['id'].center(8), alignment(goods['name'],50), goods['price'].rjust(8), goods['class']))
        #list_index.append(str(goods_list.index(goods))) # 将索引追加到索引列表，这个可以有更好的方法
    print('-'*85)
    return range(start,end) # 返回索引范围


def shopping():
    '''
    购物函数
    :return: 无
    '''
    goods_list = goods.get_all_list() # 调用商品对象的get_all_list方法，获取所有商品信息
    goods_count = len(goods_list) # 获取商品的数量
    page_div = divmod(goods_count,conf.max_per_page)
    max_page = page_div[0] if page_div[1] == 0 else page_div[0]+1 # 计算需要多少页
    flag = True
    page = 1 # 初始化页码
    while flag:
        # 购物主循环，当用户输入r的时候退出购物
        select_list = print_goods_list(goods_list, page) # 调用print_goods_list函数并返回当前页商品编号列表

        print('当前是%s页/共%s页   %s' %(page, max_page, '退出血拼返回主菜单(r)  上一页(b)  下一页(n)')) # 打印页码机操作选项
        chose = input('请输入商品编号加入购物车：') # 获取操作选项
        if chose in map(lambda x:str(int(x)+1),select_list): # 判断是否是商品编号
            # 输入的选项在返回的商品编号列表中
            goods_name = goods_list[int(chose)-1]['name'] # 获取商品名称
            # goods_id = goods_list[int(chose)-1]['id']
            while True: # 确认购买循环
                confirm = input('您选择的是%s，\n请确认是否将其放入购物车(y/n)：' %goods_name) # 打印用户选择的商品名称要求用户进行确认是否购买
                if confirm == 'y':
                    # 确认购买
                    goods.add_to_shopping_cart(chose) # 调用goods对象的add_to_shopping_cart方法将商品加入购物车
                    input('%s已放入购物车，\n按任意键继续购物' %goods_name)
                    break
                elif confirm == 'n':
                    # 购买退出确认购买循环
                    input('%s已取消放入购物车，\n按任意键继续购物' %goods_name)
                    break
                else:
                    print('输入错误，请重新输入')
        elif chose == 'n':
            # 选择n下一页，页码加1
            if page < max_page:
                page = page + 1
            else:
                input("已经是最后一页了，按任意键继续")
        elif chose == 'b':
            # 选择b上一页，页码减1
            if page == 1:
                input("已经是第一页了，按任意键继续")
            else:
                page = page - 1

        elif chose == 'r':
            # 选择r，退出购物主循环返回主菜单
            flag = False
        else:
            input("输入错误，按任意键继续")





def show_shopping_cart():
    '''
    打印购物车函数
    打印购物车列表和操作选项
    :return: 返回total总金额
    '''
    total = 0 # 初始化购物总金额

    #print(goods.get_shopping_cart())
    print(' %s    %s%s    %s%s\n%s' %(alignment('商品编号',8), alignment('商品名称',50), alignment('单价',8, 'right'), alignment('个数',8, 'right'), alignment('小计',8, 'right'), '-'*95))
    cart_list = goods.get_shopping_cart() # 获取购物车列表
    if len(cart_list) != 0: # 判断购物车是否为空
        # 不为空
        for cart_item in cart_list: #遍历购物车
            total = total + cart_item['subtotal'] # 购物总金额累加
            print(' %s    %s%s    %s%s' %(cart_item['id'].center(8), alignment(cart_item['name'],50), str(cart_item['price']).rjust(8), str(cart_item['num']).rjust(8), str(cart_item['subtotal']).rjust(9)))
    else:
        print('您的购物车空空如也，快去血拼吧')
    print('-'*95)
    print('总计：%s'.rjust(95-len(str(total))) % total) # 打印总计
    print('操作： 结账(p)    返回上级菜单(r)    清空购物车(e)    删除商品(d)') # 打印操作选项
    return total


def shopping_cart():
    '''
    购物车函数
    :return: 无
    '''
    while True:
        total = show_shopping_cart() # 调用打印购物车函数，并返回购物车总金额
        #print(total)
        chose = input("请选择您的操作：").strip() # 获取用户输入操作选项
        if chose == 'e': # 判断用户输入
            # 选择e，清空购物车
            if total != 0: # 判断购物车是否为空
                # 购物车不为空
                confirm = input('请确认是否清空购物车（y）：').strip() #获取用户确认
                if confirm == 'y': # 判断用户确认
                    # 确认清空
                    goods.del_all_cart() # 调用goods对象的del_all_cart方法清空购物车
                    input('购物车已经清空，按任意键继续')
                else:
                    input('清空购物车已经取消，按任意键继续')
            else:
                input('购物车是空的，快去血拼吧，按任意键继续')

        elif chose == 'p':
            # 选择p，支付
            if total != 0: # 判断购物车是否为空
                # 不为空
                if total <= int(current_user_info['balance']): # 判断余额是否大于购物总金额
                    # 余额大于购车总金额可以支付
                    customer.pay(total) # 调用customer对象的的pay方法完成支付
                    goods.del_all_cart() # 调用goods的del_all_cart方法清空购物车
                    input('完成支付，谢谢。按任意键返回主菜单')
                    break
                else:
                    # 不可以支付
                    input('您当前余额为%s，购物车总计为%s无法支付，\n请删除部分商品，按任意键继续' %(current_user_info['balance'], total))
            else:
                input('购物车是空的，快去血拼吧，按任意键继续')
        elif chose == 'r':
            # 选择r退出购物车循环，返回上一级菜单
            break
        elif chose == 'd':
            # 选择d，删除一个购物车商品
            cart_gid_list = goods.get_shopping_gid() # 获取购物车商品编号列表
            gid = input('请输入要删除的商品编号：').strip() # 获取用户输入的商品编号
            if gid in cart_gid_list: # 判断用户输入的是否在商品编号列表中
                # 在商品列表中
                goods_list = goods.get_all_list() # 获取所有商品列表
                goods_name = goods_list[int(gid)-1]['name'] # 获取商品编号对应的商品名称
                while True: # 确认删除循环
                    confirm = input('您选择的是%s，\n请确认是删除1个%s(y/n)：' %(goods_name, goods_name)) # 获取用户输入的确认信息
                    if confirm == 'y': # 判断用户的输入
                        # 用户选择y，确认删除
                        goods.del_goods_from_cart(gid) # 调用goods对象的del_goods_from_cart方法从购物车中删除
                        input('成功删除1个%s，\n按任意键继续' %goods_name)

                        break
                    elif confirm == 'n':
                        # 用户输入n取消删除
                        input('已取消删除1个%s，\n按任意键继续' %goods_name)
                        break
                    else:
                        print('输入错误，请重新输入')
                pass
            else:
                input("输入错误，按任意键继续")
        else:
            input("输入错误，按任意键继续")



if __name__ == '__main__':
    # 程序主入口
    # 创建购物车对象
    goods = goods(conf.goods_file)
    # 常见客户对象
    customer = customer(conf.customer_file)
    print(conf.app_info)
    print('请先登录：')
    # 调用客户对象的authenticate()进行登录验证
    if customer.authenticate():
        # 登录成功
    #if True:
        # 获取当前用户信息
        current_user_info = customer.get_current_customer_info()
        flag = True
        while flag:
            # 打印主菜单
            print_main_menu()
            # 获取输入的菜单编号
            chose = input("请输入菜单编号：").strip()
            if chose == '1':
                # 选择1，调用shopping()函数进入购物状态
                shopping()
            elif chose == '2':
                # 选择2，调用shopping_cart()函数进入购物车状态
                shopping_cart()
            elif chose == '3':
                # 选择3，退出循环结束程序
                flag = False
                print('欢迎您下次再来，再见！')
            else:
                input('输入错误，请重新输入，按任意键继续')