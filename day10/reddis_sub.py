#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''

#!/usr/bin/env python
# -*- coding:utf-8 -*-

from redis_helper import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()

while True:
    msg= redis_sub.parse_response()
    print(msg)
