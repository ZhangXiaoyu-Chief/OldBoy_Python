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
if __name__ == '__main__':
    import logging
    # logging.warning('is warning')
    # logging.critical('is critical')
    #logging.basicConfig(filename = 'access.log', level = logging.INFO)
    # logging.basicConfig(filename = 'access.log', level = logging.INFO, format = '%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
    #
    # logging.debug('is debug')
    # logging.error('is error')
    logger = logging.getLogger('log_demo')
    logger.setLevel(logging.ERROR) # 全局的优先于其他的

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fh = logging.FileHandler('access.log')
    formatter = logging.Formatter(fmt = '%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')



