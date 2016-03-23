#!/usr/bin/env python
# coding:utf-8

import json
import urllib2
#auth function
def get_auth():
    zabbix_url="http://192.168.1.222/zabbix/api_jsonrpc.php"
    api_pass='zabbix'
    auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':'Admin','password':api_pass},'id':1}
    request=urllib2.Request(zabbix_url,json.dumps(auth_data))
    request.add_header('Content-Type','application/json')
    response=urllib2.urlopen(request)
    var1=json.loads(response.read())
    return var1['result']

def get_groups(auth_code):
    zabbix_url="http://192.168.1.222/zabbix/api_jsonrpc.php"
    api_pass='zabbix'
    data = {
       "jsonrpc":"2.0",
       "method":"hostgroup.get",
       "params":{
           "output":["groupid",group],
       },
       "auth":auth_code, # theauth id is what auth script returns, remeber it is string
       "id":1,
    }
    request=urllib2.Request(zabbix_url,json.dumps(data))
    request.add_header('Content-Type','application/json')
    response=urllib2.urlopen(request)
    var1=json.loads(response.read())
    return var1

auth_code = get_auth()
res = get_hosts('xxx', auth_code)
print(res)