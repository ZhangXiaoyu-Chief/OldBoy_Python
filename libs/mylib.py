#!/usr/bin/env python3
# coding:utf-8


def myljust(str1, width, fillchar = None):
    '''
    中英文混合左对齐
    :param str1: 欲对齐字符串
    :param width: 宽度
    :param fillchar: 填充字符串
    :return: 新的经过左对齐处理的字符串对象
    '''
    if fillchar == None:
        fillchar = ' '
    length = len(str1.encode('gb2312'))
    fill_char_size = width - length if width >= length else 0
    return "%s%s" %(str1, fillchar * fill_char_size)


def myrjust(str1, width, fillchar = None):
    '''
    中英文混合右对齐
    :param str1: 欲对齐字符串
    :param width: 宽度
    :param fillchar: 填充字符串
    :return: 新的经过右对齐处理的字符串对象
    '''
    if fillchar == None:
        fillchar = ' '
    length = len(str1.encode('gb2312'))
    fill_char_size = width - length if width >= length else 0
    return "%s%s" %(fillchar * fill_char_size, str1)

def mycenter(str1, width, fillchar = None):
    '''
    中英文混合居中对齐
    :param str1: 欲对齐字符串
    :param width: 宽度
    :param fillchar: 填充字符串
    :return: 新的经过居中对齐处理的字符串对象
    '''
    if fillchar == None:
        fillchar = ' '
    length = len(str1.encode('gb2312'))
    fill_char_size = width - length if width >= length else 0
    if length%2 == 0:
        return "%s%s%s" %(fillchar * (fill_char_size //2), str1, fillchar* (fill_char_size // 2))
    else:
        return "%s%s%s" %(fillchar * (fill_char_size //2 + 1), str1, fillchar* (fill_char_size // 2))

def color(str1, color_id = 37):
    '''
    字符串颜色高亮
    :param str1: 源字符串
    :param color_id: 颜色id：30:黑 31:红 32:绿 33:黄 34:蓝色 35:紫色 36:深绿 37:白色
    :return: 返回高亮字符串
    '''
    return "\33[%sm%s\033[0m" %(color_id, str1)

def myfind(str1, sub, color_id = None):
    if color_id == None:
        color_id = 31
    return str1.replace(sub, color(sub, color_id))


def jiami(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

import msvcrt
def pwd_input():
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
        if newChar in '\r\n': # 如果是换行，则输入结束
             break
        elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号
             if chars:
                 del chars[-1]
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
                 msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
    return (''.join(chars) )

def pagination(li, max_per_page, page = 1):
    li_count = len(li) # 列表元素的数量
    page_div = divmod(li_count, max_page)
    max_page = page_div[0] if page_div[1] == 0 else page_div[0]+1 # 计算需要多少页
    if page <= max_page:
        start = ((page - 1) * max_per_page)
        end = start + max_per_page
        return li[start:end], max_page
    else:
        return [], max_page


# print(myljust('中文',20,'*'))
# print(myljust('abc',20,'*'))
# print(myljust('中文abc',20,'*'))
# print(myrjust('中文',20,'*'))
# print(myrjust('abc',20,'*'))
# print(myrjust('中文abc',20,'*'))
# print(mycenter('中文',20,'*'))
# print(mycenter('abc',20,'*'))
# print(mycenter('中文abc',20,'*'))
#
# print(color('红色', 31))
# print(color('黄色', 33))
# print(color('绿色', 32))
# print(color('蓝色', 34))
#
# print(myfind('Pythonathon', 'thon'))
# print(jiami('123.com'.encode('utf-8')))


