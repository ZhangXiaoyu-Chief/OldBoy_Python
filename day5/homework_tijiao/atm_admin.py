#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: ATM后台主程序

Help:
'''
# import logging
# import logging.config
from model.account import account
from model.atm import atm
import conf
import libs.mylib as mylib
if __name__ == '__main__':
    ac = account()
    atm = atm()
    logger = mylib.mylog(conf.ATM_LOG)

    def print_welcome():
        welcome_info = '''
**********************************
* %s *
* %s *
* %s *
**********************************''' %(mylib.myljust('欢迎来到65银行后台系统', 30), mylib.myljust('Version: 1.0', 30), mylib.myljust('admin 您好', 30))
        print(welcome_info)

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


    def show_account_info(account):
        '''
        显示账户信息函数
        :param account: 账户对象
        :return: 无
        '''
        account_info = '''
用户详细信息
-----------------------------------------------------
     卡号: %s
     户名: %s
     地址: %s
     电话: %s
     邮箱: %s
 可用余额: %s
 提现余额: %s
 可用额度: %s
     状态: %s
-----------------------------------------------------
''' %(account['cardid'], account['name'], account['address'], account['tel'], account['mail'],account['balance'], account['cash'], account['max_balance'], account['status'])
        print(mylib.myfind(account_info, '用户详细信息'))
        logger.info('atm_admin：查看账户%s详细信息' %account['cardid'])



    def add_account():
        '''
        添加账户函数
        :return: 无
        '''
        flag = True
        while flag:
            # 获取用户输入的账户信息，任何一个输入项，输入r取消添加用户
            cardid = mylib.validate_input(r'^\d{9}$','卡号: ', '输入提示: 卡号必须是9位数字，并且不能重复，输入r返回上级菜单')
            if cardid == 'r':
                flag = False
                continue
            if ac.check_cardid(cardid): # 判断卡号是否存在
                input('卡号已经存在，请重新输入，按任意键继续')
                continue
            name = mylib.validate_input(r'^.{1,10}$', '账户名: ', '输入提示: 账户名不能为空，长度不能超过10个字符，输入r返回上级菜单')
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
            # 调用ac对象的insert_account方法添加用户
            res, msg = ac.insert_account(cardid, name, tel, mail, address)
            input('%s，按任意键继续' %msg)
            logger.info('atm_admin添加账户：%s，%s' %(cardid, msg))

    def freeze_account(account):
        '''
        冻结账户函数
        :param account: 欲冻结的账户
        :return: 无
        '''
        # 判断当前状态是否为非冻结状态，已冻结的账户不能再冻结
        if account['status'] != '冻结':
            # 修改用户状态为冻结，并调用ac对象的update_account方法更新账户信息
            account['status'] = '冻结'
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经被冻结，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
            logger.info('atm_admin冻结账户：%s，%s' %(account['cardid'], msg))
        else:
            input('操作错误: 卡号为%s的用户已经是冻结状态' %account['cardid'])

    def unfreeze_account(account):
        '''
        解冻用户函数
        :param account: 欲解冻的账户
        :return: 无
        '''
        # 判断用户是否为冻结状态，只有冻结的账户才能解冻
        if account['status'] == '冻结':
            # 修改用户状态，并解冻用户
            account['status'] = '正常'
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经解冻，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
            logger.info('atm_admin解冻账户：%s，%s' %(account['cardid'], msg))
        else:
            input('操作错误: 卡号为%s的用户不是冻结状态' %account['cardid'])

    def change_max_balance(account):
        '''
        修改可用额度函数
        :param account: 欲修改的函数
        :return: 无
        '''
        new_max_balance = mylib.validate_input('^\d+[.]{0,1}\d+$', '请输入新的用户额度: ') # 获取用户输入的新的可用额度
        if new_max_balance != 'r':
            # 修改用户可用额度，并更新
            account['max_balance'] = float(new_max_balance)
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户额度已经调整为%s，按任意键继续' %(msg, account['cardid'], account['max_balance']))
                logger.info('atm_admin调整用户额度：%s，%s，调整为%s' %(account['cardid'], msg,account['max_balance']))
            else:
                input('%s，按任意键继续' %msg)
                logger.info('atm_admin调整用户额度：%s，%s' %(account['cardid'], msg))


    def unlock_account(account):
        '''
        解锁账户函数
        :param account: 欲解锁的账户
        :return: 无
        '''
        # 判断是否为锁定状态，只有锁定的账户才能解除锁定状态
        if account['status'] == '锁定':
            # 修改用户状态为正常、清空输入错误技术器并更新用户信息
            account['status'] = '正常'
            account['error_count'] = 0
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经解锁，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
            logger.info('atm_admin解锁账户：%s，%s' %(account['cardid'], msg))
        else:
            input('操作错误: 卡号为%s的用户为非锁定状态' %account['cardid'])

    def lock_account(account):
        '''
        锁定用户函数
        :param account: 欲锁定的用户
        :return: 无
        '''
        # 判断用户状态是否为正常，只有正常的用户才可以被锁定
        if account['status'] == '正常':
            # 修改状态为锁定输入错误次数改为最多可输入错误的次数，并更新用户信息
            account['status'] = '锁定'
            account['error_count'] = conf.MAX_ERROR_COUNT
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经锁定，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
            logger.info('atm_admin锁定账户：%s，%s' %(account['cardid'], msg))
        else:
            input('操作错误: 卡号为%s的用户已经是锁定状态' %account['cardid'])

    def show_accounts():
        '''
        查看所有账户信息函数
        :return: 无
        '''
        page = 1 # 初始化页码
        flag = True
        while flag:
            # 获取所有账户
            accounts = ac.get_accounts()
            if accounts:
                # 分页，获取分页后的列表和最多可以分多少页
                res_list, max_page = mylib.pagination(accounts, conf.MAX_PER_PAGE, page)
                # 打印分页后的用户列表
                print(mylib.mycenter('查看用户', 65))
                print('-' * 65)
                print(' %s %s %s %s %s %s' %(mylib.myljust('序号', 6), mylib.myljust('卡号', 11), mylib.myljust('账户名', 12), mylib.myljust('电话', 13), mylib.myljust('状态', 6), mylib.myljust('可用额度', 8)))
                for num, account in enumerate(res_list, 1):
                    print(' %s   %s %s %s %s %s' %(mylib.myrjust(str(num), 4), mylib.myljust(account['cardid'], 11), mylib.myljust(account['name'], 12), mylib.myljust(account['tel'], 13), mylib.myljust(account['status'], 6), mylib.myljust(str(account['max_balance']), 8)))
                print('-' * 65)
                print(mylib.myrjust('当前第%s页/共%s页' %(page, max_page), 65))
                print()
                chose = input('操作提示：\n 输入相应序号选择用户\n 输入n进入下一页，输入b进入上一页，输入r返回主菜单\n 请输入: ').strip()
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
                    # 如果用户输入的是列表的编号，相当于选定改用进行相应操作
                    chose_account = res_list[int(chose) - 1] # 获取输入的序号对应的账户
                    do_flag = True
                    while do_flag:
                        show_account_info(chose_account) # 显示该用户信息
                        do_chose = print_menu(['冻结账户', '解冻账户', '调整账户额度', '锁定账户', '解锁账户','注销账户', '返回'])
                        if do_chose == '1':
                            freeze_account(chose_account)
                        elif do_chose == '2':
                            unfreeze_account(chose_account)
                        elif do_chose == '3':
                            change_max_balance(chose_account)
                        elif do_chose == '4':
                            lock_account(chose_account)
                        elif do_chose == '5':
                            unlock_account(chose_account)
                        elif do_chose == '6':
                            if remove_account(chose_account):
                                do_flag = False
                        elif do_chose == '7':
                            do_flag = False
                        else:
                            input('输入错误，按任意键继续')
                else:
                    input('输入错误，任意键')
            else:
                input('账户列表为空，请先添加账户，按任意键返回上级菜单')
                flag = False

    def remove_account(account):
        '''
        注销用户函数
        :param account: 欲注销的账户
        :return: 是否删除了账户，包括取消注销，如果取消注销账户也返回False
        '''
        # 获取确认
        chose = mylib.validate_input('^[y]$', '请确认是否注销卡号为%s的用户(y/n): ' %account['cardid'], back_str = 'n')
        if chose == 'y':
            # 调用ac对象的del_account方法删除账户
            res, msg = ac.del_account(account['cardid'])
        else:
            # 如果用户输入的是n说明要取消注销用户
            return False
        if res:
            input('%s，卡号为%s的用户已经删除，按任意键返回账户列表' %(msg, account['cardid']))
            logger.info('atm_admin注销账户：%s，%s' %(account['cardid'], msg))
            return True
        else:
            input('%s，按任意键继续' %msg)
            logger.info('atm_admin注销账户：%s，%s' %(account['cardid'], msg))
            return False

    if atm.admin_auth():
        logger.info('atm_admin启动')
        flag = True
        while flag:
            print_welcome()
            # 打印主菜单并获取用户输入的选项
            chose = print_menu(['添加账户', '查看并管理账户', '退出系统'])
            if chose == '1':
                add_account()
            elif chose == '2':
                show_accounts()
            elif chose == '3':
                flag = False
                input('谢谢您的使用，再见！按任意键结束')
                logger.info('atm_admin退出')
            else:
                input('输入错误，按也意见继续')