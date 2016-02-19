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
from model.account import account
from model.atm import atm
import conf
import libs.mylib as mylib
if __name__ == '__main__':
    ac = account()
    atm = atm()
    logger = mylib.mylog(conf.ATM_LOG)

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
        account = atm.get_crurrent() # 获取当前用户所有信息
        welcome_info = '''
**********************************
* %s *
* %s *
* %s *
* %s *
**********************************''' %(mylib.myljust('欢迎来到65银行', 30), mylib.myljust('Version: 1.0', 30), mylib.myljust('%s 您好' %account['name'], 30), mylib.myljust('当前余额: %s' %account['balance'], 30))
        print(welcome_info)

    def show_account_info():
        '''
        输出用户详细信息
        :return: 无
        '''
        account = atm.get_crurrent() # 获取当前用户所有信息
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
        input('按任意键继续')
        logger.info('atm_main：%s查看详细信息' %account['cardid'])

    def show_bill():
        '''
        显示账单函数
        :return: 无
        '''
        import time
        account = atm.get_crurrent()
        if account['bill']: # 判断是否有账单
            # 有账单显示账单信息
            bill_info = '''
--------------------------------本期账单------------------------------------
 账单日: %s 还款日: %s
----------------------------------------------------------------------------
 应还款金额  =  上期账单金额  -  上期还款金额  +  本期账单金额  +  利息
 %s     %s     %s     %s     %s
----------------------------------------------------------------------------''' %(time.strftime("%Y-%m-%d", time.localtime(account['bill']['bill_date'])), time.strftime("%Y-%m-%d",time.localtime(account['bill']['payment_date'])), mylib.myljust(str(account['bill']['new_balance']), 10), mylib.myljust(str(account['bill']['balance_bf']), 12), mylib.myljust(str(account['bill']['payment']), 12), mylib.myljust(str(account['bill']['new_charges']), 12), mylib.myljust(str(account['bill']['interest']), 8))
            print(bill_info)
        else:
            # 没有账单显示无
            print('还没有账单哦')
        input('按任意键继续')
        logger.info('atm_main：%s查看账单' %account['cardid'])


    def repayment():
        '''
        还款函数
        :return: 无
        '''
        # 获取用户输入的还款金额，并判判断是否合法
        amount = mylib.validate_input(r'^\d+[.]{0,1}\d+$','请输入还款金额: ', '操作提示：输入r返回主菜单')
        if amount != 'r': # 判断用户输入的是否是r
            # 如果不是说明输入的金额
            # 调用atm的repayment方法进行还款
            res, msg = atm.repayment(float(amount))
            input('%s，按任意键继续' %msg)
            logger.info('atm_main：%s还款%s，%s' %(atm.get_crurrent()['cardid'], amount, msg))

    def transfer_accounts():
        '''
        转账函数
        :return: 无
        '''
        flag = True
        while flag:
            # 获取转账的另一方的账号
            cardid_b = mylib.validate_input(r'^\d{9}$','请输入对方卡号: ', '输入提示: 卡号是9位数字，输入r返回上级菜单')
            # 判断输入的是否为r
            if cardid_b == 'r':
                # 输入的如果是r退出循环
                flag = False
                continue
            # 判断输入的账号是否是当前账号
            if cardid_b == atm.get_crurrent()['cardid']:
                # 提示错误，让用户重新输入
                input('卡号不能是当前卡号，按任意键继续')
                continue

            # 获取输入的账号的账户信息
            account_b,msg = ac.find_by_id(cardid_b)
            # 判断输入的账户是否存在
            if account_b:
                # 获取输入的转账金额
                amount = mylib.validate_input(r'^\d+[.]{0,1}\d+$','请输入转账金额: ', '输入提示：\n  金额不能大于余额')
                # 调用atm的transfer_accounts方法转账
                res, msg = atm.transfer_accounts(account_b, float(amount))
                logger.info('atm_main：%s转账%s：%s，%s' %(atm.get_crurrent()['cardid'], cardid_b, amount, msg))
                input('%s，按任意键继续' %msg)
                flag = False
            else:
                input('%s不存在，请重新输入，按任意键继续' %msg)



    def take_cash():
        '''
        提现函数
        :return: 无
        '''
        flag = True
        while flag:
            # 获取提现金额
            cash = mylib.validate_input(r'^\d+[.]{0,1}\d+$','请输入提现金额: ', '输入提示：\n  取现金额必须是100的整数倍\n  金额不能大于余额\n  输入r返回主菜单')
            # 如果输入的不是r
            if cash != 'r':
                # 判断输入的金额是否是100的整数倍
                if float(cash)%100 == 0:
                    # 如果输入的是100的整数倍调用atm的take_cash方法提现
                    res, msg = atm.take_cash(float(cash))
                    input('%s，按任意键继续' %msg)
                    logger.info('atm_main：%s提现%s，%s' %(atm.get_crurrent()['cardid'], cash, msg))
                else:
                    input('输入金额必须是100的整数倍')
            else:
                flag = False

    def show_transaction_detail():
        '''
        查看消费流水函数
        :return: 无
        '''
        import time
        account = atm.get_crurrent()

        page = 1
        flag = True
        logger.info('atm_main：%s查看消费流水' %(account['cardid']))
        while flag:
            # 调用mylib的pagination函数分页，或的分页后的列表和最多可以分多少页
            res_list, max_page = mylib.pagination(account['transaction_detail'], conf.MAX_PER_PAGE, page)
            # 打印分页后的消费流水
            print(mylib.mycenter('消费流水', 65))
            print('-' * 65)
            print(' %s %s %s %s' %(mylib.myljust('序号', 6), mylib.myljust('时间', 25), mylib.myljust('项目', 20), mylib.myljust('金额', 20)))
            for num, item in enumerate(res_list, 1):
                print(' %s   %s %s %s' %(mylib.myrjust(str(num), 4), mylib.myljust(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item['date'])), 25), mylib.myljust(item['description'], 20), mylib.myljust(str(item['amount']), 20)))
            print('-' * 65)
            print(mylib.myrjust('当前第%s页/共%s页' %(page, max_page), 65))
            # 获取用户的操作输入
            chose = input('操作提示：\n 输入n进入下一页，输入b进入上一页，输入r返回上一级菜单\n 请输入: ').strip()
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
            else:
                input('输入错误，任意键')


    def change_password():
        '''
        修改密码函数
        :return: 无
        '''
        flag = True
        while flag:
            account = atm.get_crurrent()
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
            if old_password == account['password']:
                # 判断新密码是否和确认密码一致
                if new_password == confirm_password:
                    new_password = mylib.jiami(new_password)
                    # 判断新密码是否和旧密码不一样
                    if new_password != old_password:
                        # 修改密码
                        account['password'] = new_password
                        res, msg = ac.update_account(account)
                        input('密码%s，按任意键返回上级菜单' %msg)
                        logger.info('atm_main：%s修改密码，%s' %(atm.get_crurrent()['cardid'], msg))
                        flag = False
                    else:
                        input('新密码和旧密码不能一样，按任意键继续')
                else:
                   input('新密码和确认密码不一致，按任意键继续')
            else:
                input('原密码错误，按任意键继续')

    if atm.auth():
        flag = True
        logger.info('atm_main：%s登录系统' %atm.get_crurrent()['cardid'])
        while flag:
            print_welcome()
            chose = print_menu(['查看详细信息', '查看账单', '提现', '还款', '同行转账', '查看消费流水', '修改密码', '退出'])
            if chose == '1':
                show_account_info()
            elif chose == '2':
                show_bill()
            elif chose == '3':
                take_cash()
            elif chose == '4':
                repayment()
            elif chose == '5':
                transfer_accounts()
            elif chose == '6':
                show_transaction_detail()
            elif chose == '7':
                change_password()
            elif chose == '8':
                flag = False
                input('谢谢您的使用，再见！按任意键结束')
            else:
                input('输入错误，按也意见继续')