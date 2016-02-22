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
------------------------------------------------------------------------
                              北市(2)
                        |                    |
            钱庄(1)     |                    |      当铺(3)
                        |                    |
    --------------------+                    +---------------------

西市(4)                           我                            东市(5)

    --------------------+                    +---------------------
                        |                    |
           妓院(6)      |                    |     出城(8)
                        |                    |
                             南市(7)
    ''' %(role_info[0], role_info[1], role_info[2], role_info[3], role_info[4], role_info[5], role_info[6], role_info[7], role_info[8], role_info[9])
    print(main_map)

def new_game(role_info):
    print('new_game')
    print_main(role_info)




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

    print(enumerate(main_menu))
    for menu in enumerate(main_menu):
        print(menu[0]+1, menu[1])


def run():
    role_1 = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    print(role_1.get_name)

    role_1.say('testing')
    main_menu_do = {"1":new_game, "2":reload_game, "3":print_game_info, "4":exit_game}

    flag = True
    while flag:
        print_main_menu()
        chose = input('\n>> ')
        if chose in main_menu_do.keys():
            main_menu_do[chose](role_1)
