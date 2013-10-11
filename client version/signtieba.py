#!/usr/bin/env python
#!---coding=utf8---
import requests
import bs4

urlt='http://tieba.baidu.com/f?kw='
signurl='http://tieba.baidu.com/sign/add'

tieba=[]
f=open('tiebas.txt','r')
tieba=f.read().splitlines()
f.close()


headers={}
f=open('configs.txt','r')
for line in f:
    if line[0]=='#':
        continue
    line=line.rstrip('\n')
    key,value=line.split('=',1)
    headers[key]=value
f.close()

data={}
data['ie']='utf-8'

for t in tieba:
    #data['kw']=t.decode('gbk').encode('utf-8')#on windows
    #on linux
    data['kw']=t
    t=t.decode('utf-8').encode('gbk')
    url=urlt+t
    r=requests.get(url,headers=headers)
    data['tbs']=bs4.BeautifulSoup(r.text).body.find('script').string.split('"')[1].encode('utf-8')
    r=requests.post(signurl,headers=headers,data=data)
    print r.text
    if r.url==signurl:
        print t+'吧签到成功'


a=raw_input('Press Enter to exit:')





