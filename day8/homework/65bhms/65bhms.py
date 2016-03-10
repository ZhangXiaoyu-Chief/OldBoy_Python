from conf import conf
from model import manager
import os
import time

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-g", "--group", dest = "group", help = 'group name', type = "string")
parser.add_option("-c", "--commend", dest = "cmd", help = 'commend', type = "string")
parser.add_option("-m", "--module", dest = "module", help = 'module', type = "string")
parser.add_option("-s", "--src", dest = "src", help = 'source file or path', type = "string")
parser.add_option("-d", "--dst", dest = "dst", help = 'destination file or path', type = "string")
parser.add_option("-a", "--action", dest = "action", help = 'action for module file, [get/put]', type = "string")


(options, args) = parser.parse_args()
if options.module == 'shell':
    if options.group and options.cmd:
        if options.group in conf.GROUPS.keys():
            hosts = conf.GROUPS[options.group]
            manager.mult_run(hosts, options.cmd, manager.run_cmd)
        else:
            print(conf.CODE_LIST['101'] %options.group)
    else:
        print(conf.CODE_LIST['103'])
elif options.module == 'file':
    if not(options.group and options.action):
        print(conf.CODE_LIST['103'])
        exit(1)
    if not (options.group in conf.GROUPS.keys()):
        exit(1)
        print(conf.CODE_LIST['101'] %options.group)
    if not (options.src):
        print(conf.CODE_LIST['107'])
        exit(1)
    hosts = conf.GROUPS[options.group]
    if options.action == 'get' or options.action == 'put':
        if not options.dst and options.action == 'get':
            dst_path = os.path.abspath('.')
        elif options.dst:
            dst_path = options.dst
        else:
            print(conf.CODE_LIST['106'])
            exit(1)
        if options.action == 'get':
            if os.path.isdir(dst_path):
                dst_path = os.path.join(dst_path, time.strftime("%Y%m%d%H%M%S", time.localtime()))
                try:
                    os.mkdir(dst_path)
                except IOError as e:
                    print(e)
                manager.mult_run(hosts, [options.src, dst_path], manager.get_file)
            else:
                print(conf.CODE_LIST['106'] %options.dst)
                exit(1)
        else:
            if os.path.isfile(options.src):
                manager.mult_run(hosts, [options.src, options.dst], manager.put_file)
            else:
                print(conf.CODE_LIST['107'] %options.src)
                exit(1)
    else:
        print(conf.CODE_LIST['103'])
        exit(1)
else:
    print(conf.CODE_LIST['105'] %options.module)

