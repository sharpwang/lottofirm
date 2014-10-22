#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import sqlite3
import smtplib
import traceback
from email.mime.text import MIMEText  

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')   

def get_content_url(home_url):
    try:
        response = urllib2.urlopen(home_url, timeout=30)
        html = response.read()
        soup = BeautifulSoup(html)
        a = soup.find('td', class_='table_bottom01 suh').div.a
        rel = a['href']
        title = a['title'].encode('utf-8')
        url = urljoin(blog, rel)
        return url, title
    except Exception, e:
        traceback.print_exc()
        print 'get content url failed'

def get_content_body(url):
    try:
        response = urllib2.urlopen(url, timeout=30)
        html = response.read()
        soup = BeautifulSoup(html)
        content = soup.select('#first')[0].encode('utf-8')
        return content
    except Exception, e:
        traceback.print_exc()
        print 'get content failed'

def load_log(file, url):
    try:
        conn = sqlite3.connect(file)
        try:
            conn.execute('''CREATE TABLE LOG 
                (URL VARCHAR(256) PRIMARY KEY NOT NULL,
                TITLE VARCHAR(256) NOT NULL);''')
        except:
            pass
        stmt = "select * from LOG where URL = '%s'" % url
        cur = conn.execute(stmt)
        rows = cur.fetchall()
        return len(rows)
    except Exception, e:
        traceback.print_exc()
        print 'load log failed'
        return 0
    finally:
        conn.close()

def send_message(recipients, subject, body):
    mailboxs = [{'smtp' : 'mail.gmx.com', 'port' : 587, 'user' : 'wangzhen@gmx.com', 'pass' : 'miAujv8R', 'tls' : True, 'ssl' : False},  \
    {'smtp' : 'my.inbox.com', 'port' : 465, 'user' : 'wangzhen@inbox.com', 'pass': 'Duv7irYd', 'tls' : False, 'ssl' : True}]
    msg = MIMEText(body,'html','utf-8')
    msg['Subject'] = subject
    for mailbox in mailboxs:
        smtpserver = mailbox['smtp']
        port = mailbox['port']
        sender = mailbox['user']
        password = mailbox['pass']
        try:
            smtp_connect = lambda ssl, server: smtplib.SMTP_SSL(server) if ssl else smtplib.SMTP(server)
            smtp = smtp_connect(mailbox['ssl'],smtpserver)
            smtp.set_debuglevel(1)
            if mailbox['tls'] == True:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
            smtp.login(sender, password)
            smtp.sendmail(sender, recipients, msg.as_string())
            smtp.quit()
            #print "send mail using " + sender + " succeed"
            return True
        except Exception, e:
            traceback.print_exc()
            print "send mail using " + sender + " failed"
            continue
    return False

def save_log(file, url, title):
    try:
        conn = sqlite3.connect(file)
        stmt = "INSERT INTO LOG VALUES('%s', '%s')" % (url, title)
        conn.execute(stmt)
        conn.commit()
    except Exception, e:
        traceback.print_exc()
        print stmt
        print 'save to log failed'
    finally:
        conn.close()



blog = 'http://www.taoguba.com.cn/blog/252069'
#通过首页得到最新博客的地址
url, title = get_content_url(blog)
#得到最新博客的内容
content = get_content_body(url)
log = 'log.db'
#看看这条博客是不是已经发送过了
row = load_log(log, url)
if row > 0:
    pass
    #print 'mail already sent do not send again'
else:
    recipients = ['831261@qq.com','20891206@qq.com','13619633@qq.com']
    #没有发送过，发送内容到上述地址
    if send_message(recipients, title, content) == True:
        #print 'send a messge to recipients'
        save_log(log, url, title)


