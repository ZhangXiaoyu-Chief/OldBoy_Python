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
    def print_welcome():
        menu = ['查看详细信息', '查看账单', '提现', '同行转账', '查看消费流水', '修改密码', '退出']
        account = atm.get_crurrent()
        welcome_info = '''
**********************************
* %s *
* %s *
* %s *
* %s *
**********************************
        ''' %(mylib.myljust('欢迎来到65银行', 30), mylib.myljust('Version: 1.0', 30), mylib.myljust('%s 您好' %account['name'], 30), mylib.myljust('当前余额: %s' %account['balance'], 30))
        print(welcome_info)
        #items = list(enumerate(menu))
        #print(range(len(items), 2))
        # for i in range(0, len(list(items)), 2):
        #     print('%s、 %s %s、 %s' %(items[i][0], mylib.myljust(items[i][1], 20), items[i+1][0], mylib.myljust(items[i+1][1], 20)))
        for item in enumerate(menu, 1):
            print('%s、 %s' %item)

        chose = input('请选择：')
        return chose
    if atm.auth():
        print_welcome()

