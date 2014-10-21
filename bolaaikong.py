#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import sqlite3
import smtplib
import trackback
from email.mime.text import MIMEText  

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
        trackback.print_exc()
        print 'get content url failed'

def get_content_body(url):
    try:
        response = urllib2.urlopen(url, timeout=30)
        html = response.read()
        soup = BeautifulSoup(html)
        content = soup.select('#first')[0].encode('utf-8')
        return content
    except Exception, e:
        trackback.print_exc()
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
        trackback.print_exc()
        print 'load log failed'
        return 0
    finally:
        conn.close()

def send_message(recipients, subject, body):
    try:
        smtpserver = 'smtp.126.com'
        smtp = smtplib.SMTP(smtpserver)

        sender = 'websecret@126.com'
        
        username = 'websecret@126.com'
        password = 'Message888'
        msg = MIMEText(body,'html','utf-8')
        msg['Subject'] = subject      
        smtp.docmd('ehlo','websecret@126.com')
        smtp.login(username, password)
        smtp.sendmail(sender, recipients, msg.as_string())
        return True
    except Exception, e:
        trackback.print_exc()
        print 'send mail failed'
        return False
    finally:
        smtp.quit()

def save_log(file, url, title):
    try:
        conn = sqlite3.connect(file)
        stmt = "INSERT INTO LOG VALUES('%s', '%s')" % (url, title)
        print stmt
        conn.execute(stmt)
        conn.commit()
    except Exception, e:
        trackback.print_exc()
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
    print 'mail already sent do not send again'
else:
    recipients = ['831261@qq.com','20891206@qq.com','13619633@qq.com']
    #没有发送过，发送内容到上述地址
    if send_message(recipients, title, content) == True:
        save_log(log, url, title)
    print 'send a messge to recipients done!'

