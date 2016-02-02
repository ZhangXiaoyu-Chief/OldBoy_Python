

def auth(settings):
    if settings.DATABASE['user'] == 'root' and settings.DATABASE['password'] == '123':
        print('db auth passed...')
        return True

import sys
import os
res = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

print(res)
sys.path.append(res)
from config import settings
def select(table):
    if auth(settings):
        if table == 'user':
            user_info = {
                "001" : ['zhangxiaoyu', 35, 'beijing'],
                "002" : ['xiaoyu', 20, 'hebei']
            }
            return user_info