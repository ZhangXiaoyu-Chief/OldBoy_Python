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
class Myexception(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
if __name__ == '__main__':
    try:
        a = 1
        assert a == 2
    except AttributeError as e:
        print('attrbute err: ', e)
    except ImportError as e:
        print('import err: ', e)
    except IOError as e:
        print('IO err', e)
    except IndexError as e:
        print('index err', e)
    except KeyError as e:
        print('key err', e)
    except KeyboardInterrupt as e:
        print('keyboard', e)
    except NameError as e:
        print('name err', e)
    except Myexception as e:
        print(e)
    except AssertionError as e:
        print('assert err ', e)

