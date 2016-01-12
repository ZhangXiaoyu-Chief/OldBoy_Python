#!/usr/bin/env python3
# coding:utf-8

class MyHelper(object):
    def __init__(self):
        pass
    def alignment(str1, space, align = 'left', chars = None):
        if chars == None:
            chars = ' '
        length = len(str1.encode('gb2312'))
        space = space - length if space >=length else 0
        if align == 'left':
            str1 = str1 + chars * space
        elif align == 'right':
            str1 = chars* space +str1
        elif align == 'center':
            str1 = chars * (space //2) +str1 + chars* (space - space // 2)
        return str1

