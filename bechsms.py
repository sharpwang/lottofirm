# -*- coding: utf-8 -*-
import urllib2

content = '短信已经成功发送【乐透坊】'
url = 'http://sms.bechtech.cn/Api/send/data/json?accesskey=xxxx&secretkey=d13c732949545cfefdfb0&mobile=137xxxx1881&content=' + content
response = urllib2.urlopen(url)
print response.read()
