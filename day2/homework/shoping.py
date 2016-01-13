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



goods = goods(conf.goods_file)
#print(goods.get_list())
customer = customer(conf.customer_file)

def alignment(str1, space, align = 'left', chars = None):
        if chars == None:
            chars = ' '
        length = len(str1.encode('gb2312'))
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
    print('欢迎%s，祝您购物愉快\n------------------------------------')
    for i in range(len(MAIN_MENU)):
        print(" %s、%s " %(str(i+1).rjust(2), MAIN_MENU[i]))

def print_goods_list(goods_list, page = 1):
    list_index = []
    goods_list_page = goods_list[((page-1)*5):((page-1)*5+5)]
    print(' %s    %s%s    %s\n%s' %(alignment('商品编号',8), alignment('商品名称',50, ), alignment('价格',8, 'right'), '分类', ('-'*85)))
    for goods in goods_list_page:
        print(' %s    %s%s    %s' %(goods['id'].center(8), alignment(goods['name'],50), goods['price'].rjust(8), goods['class']))
        list_index.append(str(goods_list.index(goods)))
    print('-'*85)

    return list_index


def shopping():
    goods_list = goods.get_all_list()
    goods_count = len(goods_list)
    max_page = divmod(goods_count,5)[0] if divmod(goods_count,5)[1] == 0 else divmod(goods_count,5)[0]+1
    flag = True
    page = 1
    while flag:

        select_list = print_goods_list(goods_list, page)
        #print(select_list)
        print('当前是%s页/共%s页   %s' %(page, max_page, '退出血拼返回主菜单(r)  上一页(b)  下一页(n)'))
        chose = input('请输入商品编号加入购物车：')
        if chose in map(lambda x:str(int(x)+1),select_list):
            goods_name = goods_list[int(chose)-1]['name']
            goods_id = goods_list[int(chose)-1]['id']
            #print(goods_list[int(chose)-1])
            while True:

                confirm = input('您选择的是%s，请确认是否将其放入购物车(y/n)：' %goods_name)
                if confirm == 'y':
                    goods.add_to_shopping_cart(goods_id)
                    input('%s已放入购物车，按任意键继续购物' %goods_name)
                    break
                elif confirm == 'n':
                    input('%s已取消放入购物车，按任意键继续购物' %goods_name)
                    break
                else:
                    print('输入错误，请重新输入')
        elif chose == 'n':
            if page < max_page:
                page = page + 1
            else:
                input("已经是最后一页了，按任意键继续")
        elif chose == 'b':
            if page == 1:
                input("已经是第一页了，按任意键继续")
            else:
                page = page - 1
        elif chose == 'r':
            flag = False
        else:
            input("输入错误，按任意键继续")





def show_shopping_cart():
    total = 0
    print(goods.get_shopping_cart())
    print(' %s    %s%s    %s%s\n%s' %(alignment('商品编号',8), alignment('商品名称',50), alignment('单价',8, 'right'), alignment('个数',8, 'right'), alignment('小计',8, 'right'), '-'*95))
    for cart_list in goods.get_shopping_cart():
        total = total + cart_list['subtotal']
        print(' %s    %s%s    %s%s' %(cart_list['id'].center(8), alignment(cart_list['name'],50), str(cart_list['price']).rjust(8), str(cart_list['num']).rjust(8), str(cart_list['subtotal']).rjust(9)))
    print('-'*95)
    print('总计：%s'.rjust(95-len(str(total))) % total)




if __name__ == '__main__':
    print(conf.app_info)
    print('请先登录：')
    #if customer.authenticate():
    if True:
        current_user_info = customer.get_current_customer_info()
        flag = True
        while flag:
            print_main_menu()
            chose = input("请输入菜单编号：").strip()
            if chose == '1':
                shopping()
            elif chose == '2':
                show_shopping_cart()
            elif chose == '3':
                flag = False
                print('欢迎您下次再来，再见！')
            else:
                input('输入错误，请重新输入，按任意键继续')