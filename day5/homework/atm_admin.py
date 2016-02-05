#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

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
    # logging.config.fileConfig("atm_logger.conf")
    logger = mylib.mylog('atm.log')
    # handler = logging.FileHandler(filename='atm.log',encoding = "UTF-8")
    # logger.addHandler(handler)
    # logging.basicConfig(level=logging.DEBUG, format = u'%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='atm.log', filemode='a', encoding = "UTF-8")

    def print_welcome():
        # menu = ['查看详细信息', '查看账单', '提现', '同行转账', '查看消费流水', '修改密码', '退出']
        #account = atm.get_crurrent()
        #print(account)
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
        :return:
        '''
        for item in enumerate(menu_list, 1):
            print('%s、 %s' %item) # 通过遍历打印菜单项
        chose = input('请选择：').strip() # 获取用户输入
        return chose #返回用户输入


    def show_account_info(account):

        account_info = '''
+--------------------用户详细信息---------------------+
+-----------------------------------------------------+
| %s %s |
| %s |
| %s %s |
| %s %s |
| %s %s |
+-----------------------------------------------------+''' %(mylib.myljust('卡号: %s' %account['cardid'], 25), mylib.myljust('户名: %s' %account['name'], 25), mylib.myljust('地址: %s' %account['address'], 51), mylib.myljust('电话: %s' %account['tel'], 25) , mylib.myljust('email: %s' %account['mail'], 25), mylib.myljust('余额: %s' %account['balance'], 25), mylib.myljust('提现余额: %s' %account['cash'], 25), mylib.myljust('状态: %s' %account['status'], 25), mylib.myljust('可用额度: %s' %account['max_balance'], 25))
        print(mylib.myfind(account_info, '用户详细信息'))



    def add_account():
        flag = True
        while flag:
            cardid = mylib.validate_input(r'^\d{9}$','卡号:', '输入提示: 卡号必须是9位数字，并且不能重复，输入r返回上级菜单')
            if cardid == 'r':
                flag = False
                continue
            if ac.check_cardid(cardid):
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

            res, msg = ac.insert_account(cardid, name, tel, mail, address)
            input('%s，按任意键继续' %msg)

    def freeze_account(account):
        if account['status'] != '冻结':
            account['status'] = '冻结'
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经被冻结，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
        else:
            input('操作错误: 卡号为%s的用户已经是冻结状态' %account['cardid'])

    def unfreeze_account(account):
        if account['status'] == '冻结':
            account['status'] = '正常'
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经解冻，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
        else:
            input('操作错误: 卡号为%s的用户不是冻结状态' %account['cardid'])

    def change_max_balance(account):
        new_max_balance = mylib.validate_input('^\d+[.]{0,1}\d+$', '请输入新的用户额度: ')
        if new_max_balance == 'r':
            flag = False
        else:
            account['max_balance'] = float(new_max_balance)
            flag = False
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户额度已经调整为%s，按任意键继续' %(msg, account['cardid'], account['max_balance']))
            else:
                input('%s，按任意键继续' %msg)


    def unlock_account(account):
        if account['status'] == '锁定':
            account['status'] = '正常'
            account['error_count'] = 0
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经解锁，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
        else:
            input('操作错误: 卡号为%s的用户为非锁定状态' %account['cardid'])

    def lock_account(account):
        if account['status'] == '正常':
            account['status'] = '锁定'
            account['error_count'] = 3
            res, msg = ac.update_account(account)
            if res:
                input('%s，卡号为%s的用户已经锁定，按任意键继续' %(msg, account['cardid']))
            else:
                input('%s，按任意键继续' %msg)
        else:
            input('操作错误: 卡号为%s的用户已经是锁定状态' %account['cardid'])

    def show_accounts():

        page = 1
        flag = True
        while flag:
            accounts = ac.get_accounts()
            res_list, max_page = mylib.pagination(accounts, conf.MAX_PER_PAGE)
            print(mylib.mycenter('查看用户', 65))
            print('-' * 65)
            print(' %s %s %s %s %s %s' %(mylib.myljust('序号', 6), mylib.myljust('卡号', 11), mylib.myljust('账户名', 12), mylib.myljust('电话', 13), mylib.myljust('状态', 6), mylib.myljust('可用额度', 8)))
            for num, account in enumerate(res_list, page):
                print(' %s   %s %s %s %s %s' %(mylib.myrjust(str(num), 4), mylib.myljust(account['cardid'], 11), mylib.myljust(account['name'], 12), mylib.myljust(account['tel'], 13), mylib.myljust(account['status'], 6), mylib.myljust(str(account['max_balance']), 8)))
            print('-' * 65)
            print(mylib.myrjust('当前第%s页/共%s页' %(page, max_page), 65))
            print()
            chose = input('操作提示：\n 输入相应序号选择用户\n 输入n进入下一页，输入b进入上一页，输入r返回上一级菜单\n 请输入: ').strip()
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
                chose_account = res_list[int(chose) - 1]
                do_flag = True
                while do_flag:
                    show_account_info(chose_account)
                    do_chose = print_menu(['冻结用户', '解冻用户', '调整用户额度', '解锁用户', '锁定用户','注销用户', '返回'])
                    if do_chose == '1':
                        freeze_account(chose_account)
                    elif do_chose == '2':
                        unfreeze_account(chose_account)
                    elif do_chose == '3':
                        change_max_balance(chose_account)
                    elif do_chose == '4':
                        unlock_account(chose_account)
                    elif do_chose == '5':
                        lock_account(chose_account)
                    elif do_chose == '6':
                        if remove_account(chose_account):
                            do_flag = False
                    elif do_chose == '7':
                        do_flag = False
                    else:
                        input('输入错误，按任意键继续')
            else:
                input('输入错误，任意键')




        # validate_input(re_str, title, hint = '', back_str = 'r', error_str = '输入错误'
        # insert_account(self, cardid, name, tel, mail, address, max_balance = 0)
        pass
    def remove_account(account):
        chose = mylib.validate_input('^[y]', '请确认是否注销卡号为%s的用户(y/n): ' %account['cardid'], back_str = 'n')
        if chose == 'y':
            res, msg = ac.del_account(account['cardid'])
        else:
            return False
        if res:
            input('%s，卡号为%s的用户已经删除，按任意键返回账户列表' %(msg, account['cardid']))
            return True
        else:
            input('%s，按任意键继续' %msg)
            return False



    if atm.admin_auth():
        logger.info('atm_admin启动')
        flag = True
        while flag:
            print_welcome()
            chose = print_menu(['添加用户', '查看并管理账户', '退出系统'])

            if chose == '1':
                add_account()
            elif chose == '2':
                show_accounts()
            elif chose == '3':
                flag = False
                input('谢谢您的使用，再见！按任意键结束')
            else:
                input('输入错误，按也意见继续')