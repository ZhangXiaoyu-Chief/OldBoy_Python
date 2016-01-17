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


def mail(user):
    import smtplib
    from email.mime.text import MIMEText
    from email.utils import formataddr
    ret = True
    try:
        msg = MIMEText('邮件内容', 'plain', 'utf-8')
        msg['From'] = formataddr(["65年哥",'petterzhang@126.com'])
        msg['To'] = formataddr(["张晓宇",'61411916@qq.com'])
        msg['Subject'] = "主题"

        server = smtplib.SMTP("smtp.126.com", 25)
        server.login("petterzhang@126.com", "woailaopo")
        server.sendmail('petterzhang@126.com', [user,], msg.as_string())
        server.quit()
    except Exception:
        ret = False
    return ret

if __name__ == '__main__':
    if mail('61411916@qq.com'):
        print('发送成功')
    else:
        print('发送失败')

