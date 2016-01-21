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
        if os.path.exists(self.__file):
            f = open(self.__file, 'w')
            for key,val in dict.items():
                line = []
                line.append(key)
                line.extend(val)
                #print(' '.join(line))
                f.write(' '.join(line) + '\n')
            f.close()
        else:
            print('Error: file "%s" is not exit, please check!' %self.__file)
            exit(1)

    def get_all(self):
        if os.path.exists(self.__file):
            try:
                with codecs.open(self.__file, "r", "utf-8") as f:

                    all_lines = f.readlines()
                    return all_lines

            except Exception:
                exit(1)
        else:
            print('Error: file "%s" is not exit, please check!' %self.__file)
            exit(1)

    def write_all(self, file_str):
        try:
            with codecs.open(self.__file, "w", "utf-8") as f:

                f.write(file_str)

                return True
        except Exception:
            exit(1)
