import requests
import random
import parsel
import time
import csv
import sqlite3
import datetime
from threading import Timer
from csv import reader

class Nstr:
    def __init__(self, arg):
       self.x=arg
    def __sub__(self,other):
        c=self.x.replace(other.x,"")
        return c

def name_let_list(namefile):#得到城市名称-首字母列表
    ##读城市-拼音文件
    with open(namefile, 'r', encoding='utf-8') as name:
        name_let=[]
        #读省会名称
        for i in range(28):
            line=name.readline()
            curline=line.strip().split("\n")
            name_let.append(curline)
        #读省会拼音首字母
        for i in range(28):
            line=name.readline()
            curline=line.strip().split("\n")
            name_let[i].append(curline[0])
        name.close()
        return name_let

def downloadLianjia(url,city,page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 '
                      'Safari/537.36 '
    }
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    lis = selector.css('.sellListContent li')
    for li in lis:
        # 地址
        positionInfo = li.css('.positionInfo a::text').getall()
        community = ''
        address = ''
        if len(positionInfo):
            # 小区
            community = positionInfo[0]
            # 地名
            address = positionInfo[1]    
        locate = community+'-'+address
        # 房子基本信息
        houseInfo = li.css('.houseInfo::text').get()
        houseInfo = houseInfo.split('|')
        #户型
        room = Nstr(houseInfo[0])-Nstr(' ')
        #面积
        area = Nstr(houseInfo[1])-Nstr(' ')
        area = Nstr(area)-Nstr("平米")
        #朝向
        dirc = Nstr(houseInfo[2])-Nstr(' ')
        #装修
        level = Nstr(houseInfo[3])-Nstr(' ')
        #楼层
        floor = Nstr(houseInfo[4])-Nstr(' ')
        #结构
        struct = ""
        for temp in range(5,len(houseInfo)):
            houseInfo[temp]=Nstr(houseInfo[temp])-Nstr(' ')
            struct=struct+houseInfo[temp]
        # 房价
        txt = li.css('.totalPrice span::text').get()
        Price = ''
        if isinstance(txt, str):
            Price = li.css('.totalPrice span::text').get()
        if '.'in Price:
            Price=float(Price)
        else:
            Price=int(Price)
        # 单价
        txt = li.css('.unitPrice span::text').get()
        unitPrice = ''
        if isinstance(txt, str):
            unitPrice = li.css('.unitPrice span::text').get().replace('单价', '')
        unitPrice = Nstr(unitPrice)-Nstr(',')
        unitPrice = Nstr(unitPrice)-Nstr("元/平")
        unitPrice = int(unitPrice)
        #编号
        
        conn = sqlite3.connect('house.db')
        cur = conn.cursor()
        SQL_1="SELECT count(*) FROM house WHERE 城市='{}'".format(name_let[city][0])
        cur.execute(SQL_1)
        count=cur.fetchall()
        number = name_let[city][1]+str(count[0][0]+1)
        #城市
        cityname = name_let[city][0]
        dit = {
            '编号': number,
            '城市': cityname,
            '位置': locate,
            '户型': room,
            '面积': area,
            '朝向': dirc,
            '装修': level,
            '楼层': floor,
            '结构': struct,
            '房价': Price,
            '单价': unitPrice,
        }
        note=(number,cityname,locate,room,area,dirc,level,floor,struct,Price,unitPrice)
        SQL_2="SELECT * FROM house WHERE 城市='{}' and 位置='{}' and 面积={} and 总价={}".format(cityname,locate,str(area),str(Price))
        cur.execute(SQL_2)
        result_2=cur.fetchall()
        if len(result_2)==0:#新数据，要加入
            #conn = sqlite3.connect('house.db')
            #cur = conn.cursor()
            SQL_3 = "INSERT INTO house VALUES('{}','{}','{}','{}',{},'{}','{}','{}','{}',{},{})".format(number,cityname,locate,room,str(area),dirc,level,floor,struct,str(Price),str(unitPrice))
            cur.execute(SQL_3)
            # 提交改动的方法
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()
            f = open('{}二手房数据.csv'.format(name_let[city][0]), mode='a', encoding='utf-8', newline='')
            csv_writer = csv.DictWriter(f, fieldnames=['编号','城市','位置','户型','面积','朝向','装修','楼层','结构','房价','单价'])      
            csv_writer.writerow(dit)


def get_data():#爬虫
    for city in range(28):
        for page in range(1, 4):
            url = 'https://{}.lianjia.com/ershoufang/pg{}/'.format(name_let[city][1],page)
            downloadLianjia(url,city,page)

def create_house_tab():#创建house表
    conn = sqlite3.connect('house.db')
    cur = conn.cursor()
    createtb = """CREATE TABLE house(
    编号 TEXT,
    城市 TEXT,
    位置 TEXT,
    户型 TEXT,
    面积 NUMBER,
    朝向 TEXT,
    装修 TEXT,
    楼层 TEXT,
    结构 TEXT,
    总价 NUMBER,
    单价 NUMBER,
    primary key(编号));"""
    cur.execute(createtb)
    conn.commit()
    cur.close()
    conn.close()

def drop_house_tab():#删除house表
    conn = sqlite3.connect('house.db')
    cur = conn.cursor()
    a="DROP TABLE house"
    cur.execute(a)
    conn.commit()
    cur.close()
    conn.close()

def check_house_tab():#查看house表
    conn = sqlite3.connect('house.db')
    cur = conn.cursor()
    sql_text_3 = "SELECT count(*) FROM house"
    cur.execute(sql_text_3)
    a=cur.fetchall()
    print(a)


if __name__=='__main__':
    name_let=name_let_list("name-let.txt")
    #get_data()
    check_house_tab()


