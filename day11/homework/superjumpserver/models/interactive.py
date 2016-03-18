# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import socket
import sys
from paramiko.py3compat import u
import re
import select
from models import auditlog

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False

vim_flag = False
vim_data = ''
ps1_pattern = re.compile('.*@.*[\$#]')
cmd = ''

def interactive_shell(user, hostuser, chan, client):
    if has_termios:
        posix_shell(user, hostuser,  chan, client)
    else:
        windows_shell(user, hostuser, chan, client)


def is_output(strings):
    newline_char = ['\n', '\r', '\r\n']
    for char in newline_char:
        if char in str(strings, 'utf8'):
            return True
    return False


def remove_obstruct_char(cmd_str):
    '''删除一些干扰的特殊符号'''
    control_char = re.compile(r'\x07 | \x1b\[1P | \r ', re.X)
    cmd_str = control_char.sub('',cmd_str.strip())
    patch_char = re.compile('\x08\x1b\[C')      #删除方向左右一起的按键
    while patch_char.search(cmd_str):
        cmd_str = patch_char.sub('', cmd_str.rstrip())
    return cmd_str


def deal_backspace(match_str, result_command, pattern_str, backspace_num):
    '''
    处理删除确认键
    '''
    if backspace_num > 0:
        if backspace_num > len(result_command):
            result_command += pattern_str
            result_command = result_command[0:-backspace_num]
        else:
            result_command = result_command[0:-backspace_num]
            result_command += pattern_str
    del_len = len(match_str)-3
    if del_len > 0:
        result_command = result_command[0:-del_len]
    return result_command, len(match_str)


def deal_replace_char(match_str,result_command,backspace_num):
    '''
    处理替换命令
    '''
    str_lists = re.findall(r'(?<=\x1b\[1@)\w',match_str)
    tmp_str =''.join(str_lists)
    result_command_list = list(result_command)
    if len(tmp_str) > 1:
        result_command_list[-backspace_num:-(backspace_num-len(tmp_str))] = tmp_str
    elif len(tmp_str) > 0:
        if result_command_list[-backspace_num] == ' ':
            result_command_list.insert(-backspace_num, tmp_str)
        else:
            result_command_list[-backspace_num] = tmp_str
    result_command = ''.join(result_command_list)
    return result_command, len(match_str)

def remove_control_char(result_command):
    """
    处理日志特殊字符
    """
    global  vim_flag
    control_char = re.compile(r"""
            \x1b[ #%()*+\-.\/]. |
            \r |                                               #匹配 回车符(CR)
            (?:\x1b\[|\x9b) [ -?]* [@-~] |                     #匹配 控制顺序描述符(CSI)... Cmd
            (?:\x1b\]|\x9d) .*? (?:\x1b\\|[\a\x9c]) | \x07 |   #匹配 操作系统指令(OSC)...终止符或振铃符(ST|BEL)
            (?:\x1b[P^_]|[\x90\x9e\x9f]) .*? (?:\x1b\\|\x9c) | #匹配 设备控制串或私讯或应用程序命令(DCS|PM|APC)...终止符(ST)
            \x1b.                                              #匹配 转义过后的字符
            [\x80-\x9f] | (?:\x1b\]0.*) | \[.*@.*\][\$#] | (.*mysql>.*)      #匹配 所有控制字符
            """, re.X)
    result_command = control_char.sub('', result_command.strip())

    if not vim_flag:
        if result_command.startswith('vi') or result_command.startswith('fg'):
            vim_flag = True
        #return result_command.decode('utf8',"ignore")
        return result_command
    else:
        return ''

def deal_command(str_r):
    """
        处理命令中特殊字符
    """
    str_r = remove_obstruct_char(str_r)

    result_command = ''             # 最后的结果
    backspace_num = 0               # 光标移动的个数
    reach_backspace_flag = False    # 没有检测到光标键则为true
    pattern_str = ''
    while str_r:
        tmp = re.match(r'\s*\w+\s*', str_r)
        if tmp:
            str_r = str_r[len(str(tmp.group(0))):]
            if reach_backspace_flag:
                pattern_str += str(tmp.group(0))
                continue
            else:
                result_command += str(tmp.group(0))
                continue

        tmp = re.match(r'\x1b\[K[\x08]*', str_r)
        if tmp:
            result_command, del_len = deal_backspace(str(tmp.group(0)), result_command, pattern_str, backspace_num)
            reach_backspace_flag = False
            backspace_num = 0
            pattern_str = ''
            str_r = str_r[del_len:]
            continue
        tmp = re.match(r'\x08+', str_r)
        if tmp:
            str_r = str_r[len(str(tmp.group(0))):]
            if len(str_r) != 0:
                if reach_backspace_flag:
                    result_command = result_command[0:-backspace_num] + pattern_str
                    pattern_str = ''
                else:
                    reach_backspace_flag = True
                backspace_num = len(str(tmp.group(0)))
                continue
            else:
                break

        tmp = re.match(r'(\x1b\[1@\w)+', str_r)                           #处理替换的命令
        if tmp:
            result_command,del_len = self.deal_replace_char(str(tmp.group(0)), result_command, backspace_num)
            str_r = str_r[del_len:]
            backspace_num = 0
            continue

        if reach_backspace_flag:
            pattern_str += str_r[0]
        else:
            result_command += str_r[0]
        str_r = str_r[1:]

    if backspace_num > 0:
        result_command = result_command[0:-backspace_num] + pattern_str

    result_command = remove_control_char(result_command)
    return result_command

def posix_shell(user, hostuser, chan,ssh):
    #     """
    #     Use paramiko channel connect server interactive.
    #     使用paramiko模块的channel，连接后端，进入交互式
    #     """
    global vim_data
    global vim_flag
    global cmd
    import time
    import os
    import sys
    import fcntl
    data = ''
    is_tab = False
    input_mode = False
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        while True:
            try:
                r, w, e = select.select([chan, sys.stdin], [], [])
                # flag = fcntl.fcntl(sys.stdin, fcntl.F_GETFL, 0)
                # fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flag|os.O_NONBLOCK)
            except Exception:
                pass

            if chan in r:
                try:
                    x = chan.recv(10240)
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    if vim_flag:
                        vim_data += str(x, 'utf8')
                    index = 0
                    len_x = len(x)
                    while index < len_x:
                        try:
                            n = os.write(sys.stdout.fileno(), x[index:])
                            sys.stdout.flush()
                            index += n
                        except OSError as msg:
                            print(msg)

                    if input_mode and not is_output(x):
                        data += str(x, 'utf8')

                except socket.timeout:
                    pass

            if sys.stdin in r:
                try:
                    x = os.read(sys.stdin.fileno(), 4096)
                except OSError:
                    pass
                input_mode = True
                #print(type(x))
                #print(str(x, 'utf8'))
                if str(x, 'utf8') in ['\r', '\n', '\r\n']:
                    if vim_flag:
                        match = ps1_pattern.search(vim_data)
                        if match:
                            vim_flag = False
                            data = deal_command(data)[0:200]
                            if len(data) > 0:
                                pass
                    else:
                        data = deal_command(data)[0:200]
                        # print(data)
                        # print(type(data))
                        if len(data) > 0:
                            auditlog.insert_log(user, hostuser, u'cmd', data)
                            pass
                    data = ''
                    vim_data = ''
                    input_mode = False
                if str(x, 'utf8') == '\t':
                    pass
                if len(x) == 0:
                    break
                chan.send(x)
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

def windows_shell(user, hostuser, chan, ssh):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
