#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 2.0

Description: 65商城主程序

Help:
'''
from model.customer import customer
from model.shopping import shopping
from model.goods import goods
from model.atm import atm
from libs import mylib
import conf


if __name__ == '__main__':
    shopping = shopping()
    goo = goods()
    logger = mylib.mylog(conf.SHOPPING_LOG)
    cu = customer()
    atm = atm()
    def print_menu(menu_list):
        '''
        输出菜单函数，用于显示菜单和获取用户输入
        :param menu_list: 菜单列表
        :return: 返回用户输入的选项
        '''
        for item in enumerate(menu_list, 1):
            print('%s、 %s' %item) # 通过遍历打印菜单项
        chose = input('请选择：').strip() # 获取用户输入
        return chose #返回用户输入

    def print_welcome():
        '''
        输出系统信息和用户信息
        :return: 无
        '''
        customer = shopping.get_crurrent_customer() # 获取当前用户所有信息
        if not customer:
            customer = {
                "name": "游客",
                "cart": []
            }
        #print(account)
        welcome_info = '''
**********************************
* %s *
* %s *
* %s *
**********************************''' %(mylib.myljust('欢迎来到65商城', 30), mylib.myljust('Version: 2.0', 30), mylib.myljust('%s 您好' %customer['name'], 30))
        print(welcome_info)

    def register():
        '''
        注册用户函数
        :return: 无
        '''
        customer = shopping.get_crurrent_customer() # 获取当前用户
        # 判断当前用户是否存在，如果存在说明已经登录，将不能注册新的用户
        if not customer:
            flag = True
            while flag:
                # 获取用户输入的基本信息，任何一个环节输入r将取消注册，返回主菜单
                username = mylib.validate_input(r'^\w{1,15}$','用户名:', '输入提示: 用户名必须是数字和字母的组合，长度不超过15个字符，输入r返回上级菜单')
                if username == 'r':
                    flag = False
                    continue
                if cu.check_username(username):
                    input('用户名已经存在，请重新输入，按任意键继续')
                    continue

                while True:
                    password = mylib.validate_input(r'^.{6,15}$', '密码: ', '输入提示: 密码长度介于6~15个字符，输入r返回上级菜单', is_pass=True)
                    if password == 'r':
                        flag = False
                        break
                    confirm_password = mylib.validate_input(r'^.{6,15}$', '确认密码: ', '输入提示: 确认密码必须与密码一致，输入r返回上级菜单', is_pass=True)
                    if password == 'r':
                        flag = False
                        break
                    if password == confirm_password:
                        break
                    else:
                        input('密码与确认密码不一致，按任意键重新输入')
                if not flag:
                    continue

                name = mylib.validate_input(r'^.{1,10}$', '姓名: ', '输入提示: 姓名不能为空，长度不能超过10个字符，输入r返回上级菜单')
                if name == 'r':
                    flag = False
                    continue

                tel = mylib.validate_input(r'^1([358]\d{9})$', '联系电话: ', '输入提示: 联系电话为手机号，长度为11位，输入r返回上级菜单')
                if tel == 'r':
                    flag = False
                    continue

                mail = mylib.validate_input(r'^[0-9.a-z]{0,26}@[0-9.a-z]{0,20}.[0-9a-z]{0,8}$', '邮箱: ', '输入提示: 邮箱不能为空，输入r返回上级菜单')
                if mail == 'r':
                    flag = False
                    continue

                address = mylib.validate_input(r'^.+$', '住址: ', '输入提示: 住址不能为空，输入r返回上级菜单')
                if address == 'r':
                    flag = False
                # 调用cu对象的insert_customer方法创建用户
                res, msg = cu.insert_customer(username, password, name, tel, mail, address)
                input('%s，按任意键继续' %msg)
                logger.info('注册用户：%s，%s' %(username, msg))
        else:
            input('您已经登录商城，如需要注册请退出登录')

    def login():
        '''
        登录函数
        :return: 无
        '''
        import getpass
        # 获取当前用户
        customer = shopping.get_crurrent_customer()
        # 判断是否获取当前用户，如果当前用户不存在说明还没有登录，没登录的情况下才能登录
        if not customer:
            flag = True
            while flag:
                # 获取用户名
                username = mylib.validate_input(r'^\w{1,15}$','用户名(输入r返回主菜单): ')
                if username == 'r':
                    flag = False
                    continue
                # 获取密码
                #password = mylib.validate_input(r'^.{6,15}$', '密码: ', is_pass = True)
                password = getpass.getpass('密码: ').strip()
                #print(password)
                # 调用shopping对象的login方法，验证用户名和密码
                res = shopping.login(username, password)
                if res:
                    # 验证成功显示欢迎信息并退出循环
                    input('登录成功，按任意键返回主菜单')
                    logger.info('用户登录：%s' %(username))
                    flag = False
                else:
                    input('用户名或密码错误，按任意键继续')
        else:
            input('您已经登录，不能重复登录，按任意键继续')

    def logout():
        '''
        注销函数
        :return: 无
        '''
        # 获取当前用户
        customer = shopping.get_crurrent_customer()
        # 判断是否的登录，只有登录的情况下才能注销
        if customer:
            # 调用shopping对象的logout方法退出登录
            shopping.logout()
            input('注销成功，按任意键继续')
            logger.info('用户退出登录：%s' %(customer['username']))
        else:
            input('您还没有登录，按任意键继续')

    def show_goods_info(goods):
        '''
        显示商品详细信息函数
        :return: 无
        '''
        goods_info = '''
-----------------------------------------------------
         编号: %s
     商品名称: %s
         价格: %s
         分类: %s
 商品详细信息:
-----------------------------------------------------
    %s
-----------------------------------------------------
''' %( goods['id'],  goods['name'], goods['price'], goods['class'], goods['info'])
        print(goods_info)

    def shop():
        '''
        购物函数
        :return: 无
        '''
        # 获取所有商品列表
        all_goods = goo.get_all_goods()
        # 初始化页码
        page = 1
        flag = True
        while flag:
            #all_goods = goods.get_all_goods()
            if all_goods:
                # 如果商品列表不为空显示商品信息
                # 分页商品列表，获取分页后的商品列表及最多可以分多少页
                res_list, max_page = mylib.pagination(all_goods, conf.MAX_PER_PAGE, page)
                # 输出分页后的商品列表
                print("商品列表")
                print('-' * 80)
                print(' %s %s %s %s %s' %(mylib.myljust('序号', 6), mylib.myljust('编号', 7), mylib.myljust('商品名', 45), mylib.myljust('价格', 10), mylib.myljust('分类', 8)))
                for num, goods in enumerate(res_list, 1):
                    print(' %s   %s %s %s %s' %(mylib.myrjust(str(num), 4), mylib.myljust(goods['id'], 7), mylib.myljust(goods['name'], 45), mylib.myljust(str(goods['price']), 10), mylib.myljust(goods['class'], 6)))
                print('-' * 80)
                print(mylib.myrjust('当前第%s页/共%s页' %(page, max_page), 80))
                print()
                # 获取用户输入的操作选项，输入序号表示选定商品
                chose = input('操作提示：\n 输入相应序号选择商品\n 输入n进入下一页，输入b进入上一页，输入r返回上一级菜单\n 请输入: ').strip()
                if chose == 'n':
                    # 选择n下一页，页码加1
                    if page < max_page:
                        page = page + 1
                    else:
                        input("已经是最后一页了，按任意键继续")
                elif chose == 'b':
                    # 选择b上一页，页码减1
                    if page == 1:
                        input("已经是第1页了，按任意键继续")
                    else:
                        page = page - 1
                elif chose == 'r':
                    # 选择r，退出循环返回主菜单
                    flag = False
                elif  chose in list(map(lambda x: str(x), range(1, len(res_list) + 1))):
                    # 如果选择的是商品序号，说明选定该商品
                    # 获取选定的商品
                    chose_goods = res_list[int(chose) - 1]
                    do_flag = True
                    while do_flag:
                        # 显示商品信息
                        show_goods_info(chose_goods)
                        # 获取用户操作选项
                        do_chose = print_menu(['加入购物车', '返回'])
                        if do_chose == '1':
                            # 调用shopping对象add_to_shopping_cart将选定的商品加入到购物车
                            shopping.add_to_shopping_cart(chose_goods, 1)
                            if shopping.get_crurrent_customer():
                                logger.info('用户%s将%s添加到购物车' %(shopping.get_crurrent_customer()['username'], chose_goods['name']))
                            else:
                                logger.info('游客将%s添加到购物车' %chose_goods['name'])
                            input('成功将%s加入购物车，按任意键继续' %chose_goods['name'])
                        elif do_chose == '2':
                            do_flag = False
                        else:
                            input('输入错误，按任意键继续')
                else:
                    input('输入错误，任意键')
            else:
                input('商品列表为空')
                flag = False

    def show_shopping_cart():
        '''
        打印购物车函数
        打印购物车列表和操作选项
        :return: 返回total总金额
        '''
        total = 0 # 初始化购物总金额
        print('%s %s    %s%s    %s%s\n%s' %(mylib.myljust('序号',8),mylib.myljust('商品编号',8), mylib.myljust('商品名称',50), mylib.myrjust('单价',8), mylib.myrjust('个数',8), mylib.myrjust('小计',8), '-'*100))
        cart_list = shopping.get_cart()# 获取购物车列表
        if len(cart_list) != 0: # 判断购物车是否为空
            # 不为空
            for cart_item in enumerate(cart_list, 1): #遍历购物车
                total = total + cart_item[1]['subtotal'] # 购物总金额累加
                print('%s %s    %s%s    %s%s' %(str(cart_item[0]).center(8),cart_item[1]['id'].center(8), mylib.myljust(cart_item[1]['name'],50), str(cart_item[1]['price']).rjust(8), str(cart_item[1]['num']).rjust(8), str(cart_item[1]['subtotal']).rjust(9)))
        else:
            print('您的购物车空空如也，快去血拼吧')
        print('-'*100)
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
            chose = input("请选择您的操作：").strip() # 获取用户输入操作选项
            if chose == 'e': # 判断用户输入
                # 选择e，清空购物车
                if total != 0: # 判断购物车是否为空
                    # 购物车不为空
                    confirm = mylib.validate_input('^[y]$', '请确认是否清空购物车(y/n): ', back_str = 'n') #获取用户确认
                    if confirm == 'y': # 判断用户确认
                        # 确认清空
                        shopping.empty_cart() # 调用goods对象的del_all_cart方法清空购物车
                        if shopping.get_crurrent_customer():
                            logger.info('用户%s清空购物车' %(shopping.get_crurrent_customer()['username']))
                        else:
                            logger.info('游客清空购物车')
                        input('购物车已经清空，按任意键继续')
                    else:
                        input('清空购物车已经取消，按任意键继续')
                else:
                    input('购物车是空的，快去血拼吧，按任意键继续')
            elif chose == 'p':
                # 选择p，支付
                if shopping.get_crurrent_customer():
                    if total != 0:
                        res = atm.pay_api('65商城购物', total)
                        if res:
                            shopping.empty_cart()
                            logger.info('用户%s成功支付%s' %(shopping.get_crurrent_customer()['username'], total))
                            input('支付成功，按任意键返回上级菜单')
                            break
                        else:
                            input('支付失败，按任意键继续')
                    else:
                        input('您的购物车还是空空如也，快去血拼吧！，按任意键继续')
                else:
                    input('您还没有登录，请先登录')
            elif chose == 'r':
                # 选择r退出购物车循环，返回上一级菜单
                break
            elif chose == 'd':
                del_chose = mylib.validate_input('^\d$', '请输入编号(输入r返回): ')
                if del_chose == 'r':
                    continue
                else:
                    cart_list = shopping.get_cart()
                    gname = cart_list[int(del_chose) - 1]['name']
                    confirm = mylib.validate_input('^[y]$', '请确认删除1个%s(y/n): ' %gname, back_str = 'n')
                    if confirm == 'y':
                        gid = cart_list[int(del_chose) - 1]['id']
                        res, msg = shopping.del_goods_from_cart(gid)
                        if shopping.get_crurrent_customer():
                            logger.info('用户%s删除购物车内%s ' %(shopping.get_crurrent_customer()['username'], gname))
                        else:
                            logger.info('游客删除购物车内%s' %gname)
                        input(msg)
                    else:
                        input('删除操作已经取消，按任意键继续')

    def change_password():
        '''
        修改密码函数
        :return: 无
        '''
        flag = True
        while flag:
            customer = shopping.get_crurrent_customer()
            if not customer:
                input('您还没有登录，不能修改密码，请先登录，按任意键继续')
                flag = False
                continue
            # 获取用户输入的旧密码
            old_password = mylib.validate_input(r'^.{6,15}$', '原密码: ', '输入提示: 输入r返回上级菜单', is_pass=True)
            # 判断用户输入的是否是r，如果是r退出循环
            if old_password == 'r':
                flag = False
                continue
            # 获取用户输入的新密码及确认密码
            new_password = mylib.validate_input(r'^.{6,15}$', '密码: ', '输入提示: 密码长度介于6~15个字符，输入r返回上级菜单', is_pass=True)
            confirm_password = mylib.validate_input(r'^.{6,15}$', '确认密码: ', '输入提示: 密码长度介于6~15个字符，输入r返回上级菜单', is_pass=True)
            old_password = mylib.jiami(old_password)
            # 判断旧密码是否正确
            if old_password == customer['password']:
                # 判断新密码是否和确认密码一致
                if new_password == confirm_password:
                    new_password = mylib.jiami(new_password)
                    # 判断新密码是否和旧密码不一样
                    if new_password != old_password:
                        # 修改密码
                        customer['password'] = new_password
                        res, msg = cu.update_customer(customer)
                        input('密码%s，按任意键返回上级菜单' %msg)
                        logger.info('用户%s修改密码，%s' %(customer['username'], msg))
                        flag = False
                    else:
                        input('新密码和旧密码不能一样，按任意键继续')
                else:
                   input('新密码和确认密码不一致，按任意键继续')
            else:
                input('原密码错误，按任意键继续')
    flag = True
    while flag:
        print_welcome()
        chose = print_menu(['血拼','注册', '登录', '注销', '修改密码','查看购物车', '退出'])
        if chose == '1':
            shop()
        elif chose == '2':
            register()
        elif chose == '3':
            login()
        elif chose == '4':
            logout()
        elif chose == '5':
            change_password()
        elif chose == '6':
            shopping_cart()
        elif chose == '7':
            flag = False
        else:
            input('输入错误，按任意键继续')