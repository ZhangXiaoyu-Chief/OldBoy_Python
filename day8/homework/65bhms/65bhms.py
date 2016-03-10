from conf import conf
from model import manager
import os
import time

from optparse import OptionParser

if __name__ == '__main__':
    # 定义OptionParser及相应参数
    parser = OptionParser()
    parser.add_option("-g", "--group", dest = "group", help = 'group name', type = "string")
    parser.add_option("-c", "--commend", dest = "cmd", help = 'commend', type = "string")
    parser.add_option("-m", "--module", dest = "module", help = 'module', type = "string")
    parser.add_option("-s", "--src", dest = "src", help = 'source file or path', type = "string")
    parser.add_option("-d", "--dst", dest = "dst", help = 'destination file or path', type = "string")
    parser.add_option("-a", "--action", dest = "action", help = 'action for module file, [get/put]', type = "string")

    # 获取参数列表
    (options, args) = parser.parse_args()
    if options.module == 'shell':
        # shell，用来对远程主机执行shell命令
        if options.group and options.cmd: # 判断是否包含必要的参数
            # 判断组是否存在
            if options.group in conf.GROUPS.keys():
                # 获取主机列表，并调用manager模块的mult_run函数执行远程命令
                hosts = conf.GROUPS[options.group]
                manager.mult_run(hosts, options.cmd, manager.run_cmd) #调用mangager的mult_run函数启动多进程任务
            else:
                print(conf.CODE_LIST['101'] %options.group)
        else:
            print(conf.CODE_LIST['103'])
    elif options.module == 'file':
        # file，用来执行远程文件操作，根据action参数判断是上传还是下载get（下载）/put（上传）
        if not(options.group and options.action): # 如果不含group和action参数报错退出
            print(conf.CODE_LIST['103'])
            exit(1)
        if not (options.group in conf.GROUPS.keys()): # 如果组不存在报错退出
            exit(1)
            print(conf.CODE_LIST['101'] %options.group)
        if not (options.src): # src（源文件或目录）参数不存在报错退出
            print(conf.CODE_LIST['107'])
            exit(1)
        hosts = conf.GROUPS[options.group]
        if options.action == 'get' or options.action == 'put': # action只能是get/put
            if not options.dst and options.action == 'get': # get默认dst是当前目录
                dst_path = os.path.abspath('.')
            elif options.dst:
                dst_path = options.dst
            else:
                print(conf.CODE_LIST['106']) # put如果不指定dst则报错退出
                exit(1)
            if options.action == 'get':
                if os.path.isdir(dst_path): # 判断目标目录是否存在
                    dst_path = os.path.join(dst_path, time.strftime("%Y%m%d%H%M%S", time.localtime()))
                    try:
                        os.mkdir(dst_path) # 创建时间戳目录
                        manager.mult_run(hosts, [options.src, dst_path], manager.get_file) #调用mangager的mult_run函数启动多进程任务
                    except IOError as e:
                        print(e)

                else:
                    print(conf.CODE_LIST['106'] %options.dst)
                    exit(1)
            else:
                if os.path.isfile(options.src): # action是put的话要先判断源文件（要上传的文件是否存在）
                    manager.mult_run(hosts, [options.src, options.dst], manager.put_file)
                else:
                    print(conf.CODE_LIST['107'] %options.src)
                    exit(1)
        else:
            print(conf.CODE_LIST['103'])
            exit(1)
    else:
        print(conf.CODE_LIST['105'] %options.module)

