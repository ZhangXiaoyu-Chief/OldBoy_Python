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
    # res, msg = ac.insert_account('123456780', '张晓宇', '13800138000', '61411916@qq.com', '北京市通州区')
    # print(res)
    # print(msg)
    # cardid = '1234567891234567890'
    # res = ac.check_cardid(cardid)
    # print(res)
    # res,msg = ac.find_by_id('12345678011')
    # print(res)
    # print(msg)
    # res = ac.find_accounts_by_cardid('78467')
    # res = ac.find_accounts_by_name('张晓宇')
    # for i in res:
    #
    #     print(output.myfind(i.get('name'), '张晓宇'))
    # res = ac.find_accounts_by_cardid('2345')
    # for i in res:
    #
    #     print(output.myfind(i.get('cardid'), '2345'))

    # res = ac.del_account('123456789')
    # print(res)

    # atm = atm()
    # res = atm.pay_api('sss', 500)
    # print(res)
    atm = atm()
    import re
    amount_re = re.compile('^\d+[.]{0,1}\d$')



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

    def print_welcome():
        # menu = ['查看详细信息', '查看账单', '提现', '同行转账', '查看消费流水', '修改密码', '退出']
        account = atm.get_crurrent()
        print(account)
        welcome_info = '''
**********************************
* %s *
* %s *
* %s *
* %s *
**********************************''' %(mylib.myljust('欢迎来到65银行', 30), mylib.myljust('Version: 1.0', 30), mylib.myljust('%s 您好' %account['name'], 30), mylib.myljust('当前余额: %s' %account['balance'], 30))
        print(welcome_info)
        #items = list(enumerate(menu))
        #print(range(len(items), 2))
        # for i in range(0, len(list(items)), 2):
        #     print('%s、 %s %s、 %s' %(items[i][0], mylib.myljust(items[i][1], 20), items[i+1][0], mylib.myljust(items[i+1][1], 20)))

    def show_account_info():
        account = atm.get_crurrent()
        account_info = '''
+--------------------用户详细信息---------------------+
+-----------------------------------------------------+
| %s |
| %s %s |
| %s %s |
| %s %s |
+-----------------------------------------------------+
''' %(mylib.myljust('卡号: %s' %account['cardid'], 51), mylib.myljust('户名: %s' %account['name'], 25), mylib.myljust('地址: %s' %account['address'], 25), mylib.myljust('电话: %s' %account['tel'], 25) , mylib.myljust('email: %s' %account['mail'], 25), mylib.myljust('余额: %s' %account['balance'], 25), mylib.myljust('提现余额: %s' %account['cash'], 25))
        print(mylib.myfind(account_info, '用户详细信息'))
        input('按任意键继续')

    def show_bill():
        import time
        account = atm.get_crurrent()
        bill_info = '''
+--------------------------------本期账单------------------------------------+
+----------------------------------------------------------------------------+
| %s %s |
+----------------------------------------------------------------------------+
| 应还款金额  =  上期账单金额  -  上期还款金额  +  本期账单金额  +  利息     |
| %s     %s     %s     %s     %s |
+----------------------------------------------------------------------------+''' %(mylib.myljust('账单日: %s' %time.strftime("%Y-%m-%d",time.localtime(account['bill']['bill_date'])), 37), mylib.myljust('还款日: %s' %time.strftime("%Y-%m-%d",time.localtime(account['bill']['payment_date'])), 36), mylib.myljust(str(account['bill']['new_balance']), 10), mylib.myljust(str(account['bill']['balance_bf']), 12), mylib.myljust(str(account['bill']['payment']), 12), mylib.myljust(str(account['bill']['new_charges']), 12), mylib.myljust(str(account['bill']['interest']), 8))
        print(bill_info)
        input('按任意键继续')

    def repayment():
        pass

    def take_cash():
        '''
        提现函数
        :return:
        '''
        flag = True
        while flag:
            cash = input('操作提示：\n  取现金额必须是100的整数倍\n  输入r返回上级菜单\n请输入提现金额: ').strip()
            if cash != 'r':
                if amount_re.match(cash):
                    if float(cash)%100 == 0:
                        res, msg = atm.take_cash(float(cash))
                        input('%s，按任意键继续' %msg)
                    else:
                        input('输入金额必须是100的整数倍')
                else:
                    input('输入错误，请重新输入，按任意键继续')
            else:
                flag = False

    def show_transaction_detail():
        '''
        查看消费流水函数
        :return:
        '''
        import time
        account = atm.get_crurrent()
        res_list, max_page = mylib.pagination(account['transaction_detail'], conf.MAX_PER_PAGE)
        page = 1
        flag = True
        while flag:
            print(mylib.mycenter('消费流水', 65))
            print('-' * 65)
            print(' %s %s %s %s' %(mylib.myljust('序号', 6), mylib.myljust('时间', 25), mylib.myljust('项目', 20), mylib.myljust('金额', 20)))
            for num, item in enumerate(res_list, page):
                print(' %s   %s %s %s' %(mylib.myrjust(str(num), 4), mylib.myljust(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item['date'])), 25), mylib.myljust(item['description'], 20), mylib.myljust(str(item['amount']), 20)))
            print('-' * 65)
            print(mylib.myrjust('当前第%s页/共%s页' %(page, max_page), 65))
            print()
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

        flag = True
        while flag:
            account = atm.get_crurrent()
            old_password = input('原密码(输入r返回上级菜单): ').strip()
            new_password = input('新密码: ').strip()
            confirm_password = input('确认密码: ').strip()
            if old_password == 'r':
                flag = False
            else:
                old_password = mylib.jiami(old_password)
                if old_password == account['password']:
                    if new_password == confirm_password:
                        new_password = mylib.jiami(new_password)
                        if new_password != old_password:
                            account['password'] = new_password
                            res, msg = ac.update_account(account)
                            input('密码%s，按任意键返回上级菜单' %msg)
                            flag = False
                        else:
                            input('新密码和和旧密码不能一样，按任意键继续')
                    else:
                       input('新密码和确认密码不一致，按任意键继续')
                else:
                    input('原密码错误，按任意键继续')


    if atm.auth():
        flag = True

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
                pass
            elif chose == '5':
                pass
            elif chose == '6':
                show_transaction_detail()
            elif chose == '7':
                change_password()
            elif chose == '8':
                flag = False
                input('谢谢您的使用，再见！按任意键结束')
            else:
                input('输入错误，按也意见继续')