#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib2
import json
from mytools import AlchemyEncoder
# 创建对象的基类:
Base = declarative_base()

# 定义Tdlt对象:
class Tdlt(Base):
    # 表的名字:
    __tablename__ = 'DLT'

    # 表的结构:
    qh      = Column(Integer, primary_key=True)
    rq      = Column(String(10))
    qq1     = Column(Integer) 
    qq2     = Column(Integer) 
    qq3     = Column(Integer) 
    qq4     = Column(Integer) 
    qq5     = Column(Integer) 
    hq1     = Column(Integer) 
    hq2     = Column(Integer) 
    tzze    = Column(Integer) 
    grxq    = Column(Integer) 
    zj1     = Column(Integer) 
    jj1     = Column(Integer) 
    zj2     = Column(Integer) 
    jj2     = Column(Integer) 
    zj3     = Column(Integer) 
    jj3     = Column(Integer) 
    zj4     = Column(Integer) 
    jj4     = Column(Integer) 
    zj5     = Column(Integer) 
    jj5     = Column(Integer) 
    zj6     = Column(Integer) 
    jj6     = Column(Integer) 
    zj7     = Column(Integer) 
    jj7     = Column(Integer) 
    zj8     = Column(Integer) 
    jj8     = Column(Integer) 
    zjzj1   = Column(Integer) 
    zjjj1   = Column(Integer) 
    zjzj2   = Column(Integer) 
    zjjj2   = Column(Integer) 
    zjzj3   = Column(Integer) 
    zjjj3   = Column(Integer) 
    fjwftze = Column(Integer) 
    fjwfzj1 = Column(Integer) 
    fjwfjj1 = Column(Integer) 

    # 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:wang3@lottofirm.net:3306/lottofirm')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

#从17500取最新开奖信息存到数据库
def retrieve_data():
# 创建session对象:
    session = DBSession()
    response = urllib2.urlopen('http://www.17500.cn/getData/dlt.TXT', timeout=10)
    html = response.read()
    data = html.split('\n')
    for line in reversed(data):
        record = line.split(' ')
        if(len(record) > 7):
            dlt = Tdlt()
            dlt.qh      = record[0]
            dlt.rq      = record[1]
            dlt.qq1     = record[2]
            dlt.qq2     = record[3]
            dlt.qq3     = record[4]
            dlt.qq4     = record[5]
            dlt.qq5     = record[6]
            dlt.hq1     = record[7]
            dlt.hq2     = record[8]
            dlt.tzze    = record[9] 
            dlt.grxq    = record[10] 
            dlt.zj1     = record[11] 
            dlt.jj1     = record[12] 
            dlt.zj2     = record[13] 
            dlt.jj2     = record[14] 
            dlt.zj3     = record[15] 
            dlt.jj3     = record[16] 
            dlt.zj4     = record[17] 
            dlt.jj4     = record[18] 
            dlt.zj5     = record[19] 
            dlt.jj5     = record[20] 
            dlt.zj6     = record[21] 
            dlt.jj6     = record[22] 
            dlt.zj7     = record[23] 
            dlt.jj7     = record[24] 
            dlt.zj8     = record[25] 
            dlt.jj8     = record[26] 
            dlt.zjzj1   = record[27] 
            dlt.zjjj1   = record[28] 
            dlt.zjzj2   = record[29] 
            dlt.zjjj2   = record[30] 
            dlt.zjzj3   = record[31] 
            dlt.zjjj3   = record[32] 
            dlt.fjwftze = record[33] 
            dlt.fjwfzj1 = record[34] 
            dlt.fjwfjj1 = record[35] 
            session.add(dlt)
            try:
                session.commit()
            except exc.IntegrityError:
                #最新的一条都要插进去，或者更新
                try:
                    session.rollback()
                    session.merge(dlt)
                    session.commit()
                except exc.SQLAlchemyError:
                    pass
                #这里加上break就会只更新最后一条
                break
            else:
                pass

    session.commit()
    session.close()


# 分发最新50期数据给用户
def dispatch_data(qh):
# 创建session对象:
    session = DBSession()
    data = session.query(Tdlt).filter(Tdlt.qh >= qh).all()
    session.close()
    return json.dumps(data, cls = AlchemyEncoder)

if __name__=='__main__':
    retrieve_data()


# 0 14120
# 1 2014-10-13
# 2 01
# 3 04
# 4 06
# 5 18
# 6 33
# 7 05
# 8 11
# 9 177861722
# 10 901617720
# 11 2
# 12 10000000
# 13 27
# 14 339635
# 15 352
# 16 10406
# 17 17872
# 18 200
# 19 353682
# 20 10
# 21 3786338
# 22 5
# 23 0
# 24 0
# 25 0
# 26 0
# 27 0
# 28 0
# 29 8
# 30 203781
# 31 86
# 32 6243
# 33 0
# 34 0
# 35 60
