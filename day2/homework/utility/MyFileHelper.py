#!/usr/bin/env python3
# coding:utf-8
import codecs
import conf
import os
class MyFileHelper(object):
    def __init__(self, file):
        self.__file = file

    def getfile(self):
        return self.__file

    def getdict(self):
        if os.path.exists(self.__file):
            dict = {}
            with codecs.open(self.__file, "r", "utf-8") as f:
                for line in f.readlines():
                    line = line.strip().split()
                    dict[line[0]] = line[1:]
                return dict
        else:
            print('Error: file "%s" is not exit, please check!' %self.__file)
            exit(1)

    def getlist(self):
        if os.path.exists(self.__file):
            li = []
            with codecs.open(self.__file, "r", "utf-8") as f:
                for line in f.readlines():
                    li.append(line.strip().split())
            return li
        else:
            print('Error: file "%s" is not exit, please check!' %self.__file)
            exit(1)

    def dict_to_file(self,dict):
        f = open(self.__file, 'w')
        for key,val in dict.items():
            line = []
            line.append(key)
            line.extend(val)
            #print(' '.join(line))
            f.write(' '.join(line) + '\n')
        f.close()