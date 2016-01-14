#!/usr/bin/env python3
# coding:utf-8

# 配置文件
# 商品数据文件
goods_file = "goods.db"
# 用户数据文件
customer_file = "customer.db"
# 定义密码最多可以输入错误多少次
error_count_max = 3

# 应用及版权信息
app_info = '''
+-----------------------------------+
| 欢迎来到65年哥的小店              |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）            |
+-----------------------------------+'''

# 主菜单
main_menu = ['血拼','查看购物车','退出']

# 每一页最多显示几件商品
max_per_page = 6