import csv
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from openpyxl import Workbook
from openpyxl import load_workbook
import time
import datetime
from sever_getdata import name_let_list
import numpy as np
import re

class Database_user:
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.cur = self.conn.cursor()
        
    def check_login(self,username,password):
        sql_text_3 = "SELECT * FROM user"
        self.cur.execute(sql_text_3)
        self.user=self.cur.fetchall()
        for user in self.user:
            if username==user[0]:
                if password==user[1]:
                    return True,'登录成功'
                else:
                    return False,'登录失败，密码错误'
        return False,'登录失败，用户不存在'
    def sign(self,username,password):
        sql_text_3 = "SELECT * FROM user"
        self.cur.execute(sql_text_3)
        self.user=self.cur.fetchall()
        for user in self.user:
            if username==user[0]:
                return False,"注册失败，用户名已存在"
            else:
                if username=='':
                    return False,"注册失败，用户名不能为空"
                elif password=='':
                    return False,"注册失败，密码不能为空"
                else:
                    self.cur.execute("INSERT INTO user VALUES('{}','{}')".format(username,password))
                    self.conn.commit()
                    return True,'注册成功'

class Database_house:
    def __init__(self):
        self.conn = sqlite3.connect('house.db')
        self.cur = self.conn.cursor()
        self.wb=load_workbook('log.xlsx')
        self.sheet=self.wb['Sheet1']
        
    def search(self,city,sql_text_1,order):
        self.cur.execute(sql_text_1)
        result=self.cur.fetchall()
        now=datetime.datetime.now() 
        if len(result)==0 and city!='':
            #messagebox.showwarning(title='警告',message="暂无该城市二手房信息")
            count=0
            self.sheet.append(["查询{}二手房信息".format(city),"失败",order,now.strftime("%Y-%m-%d %H:%M:%S"),"暂无该城市二手房信息"])#添加日志
        elif city=='':
            #messagebox.showwarning(title='警告',message="未输入具体城市，系统将显示全部城市房源")
            count=0
            self.sheet.append(["查询{}二手房信息".format(city),"失败",order,now.strftime("%Y-%m-%d %H:%M:%S"),"未输入城市名称"])#添加日志
        else:
            sql_text_2 = "SELECT count(*) FROM house WHERE 城市 like '%{}%'".format(city)
            self.cur.execute(sql_text_2)
            count=self.cur.fetchall()[0][0]
            self.sheet.append(["查询{}二手房信息".format(city),"成功",order,now.strftime("%Y-%m-%d %H:%M:%S"),"共查询到{}套房源信息".format(count)])#添加日志
        self.wb.save('log.xlsx')
        return result,count
    
    def statistic(self):
        name_let=name_let_list("name-let.txt")
        cityname=[x[0] for x in name_let]
        x=np.arange(len(cityname))
        housenum=[]
        for i in range(len(cityname)):
            SQL="SELECT count(*) FROM house WHERE 城市='{}'".format(cityname[i])
            self.cur.execute(SQL)
            result=self.cur.fetchall()
            housenum.append(result[0][0])
        return housenum
    
    def create_data(self,city):
        sql_text_3 = "SELECT 户型,面积,朝向,装修,楼层,结构,总价 FROM house WHERE 城市='{}'".format(city)
        self.cur.execute(sql_text_3)
        a=self.cur.fetchall()
        data=[]
        for i in range(len(a)):
            a[i]=list(a[i])
        for i in range(len(a)):
            for j in range(7):
                if j==0:
                    find_1=re.findall(r'[0-9]+',a[i][j])
                    room=[int(x) for x in find_1]
                    data.append(room)
                elif j==1:
                    data[i].append(a[i][j])
                elif j==2:
                    #data[i].append(len(a[i][j]))
                    flag_N=0
                    flag_S=0
                    flag_W=0
                    flag_E=0
                    for k in a[i][j]:
                        if k=="北":
                            data[i].append(1)
                            flag_N=1
                            break
                    if flag_N==0:
                        data[i].append(0)
                    for k in a[i][j]:
                        if k=="南":
                            data[i].append(1)
                            flag_S=1
                            break
                    if flag_S==0:
                        data[i].append(0)
                    for k in a[i][j]:
                        if k=="东":
                            data[i].append(1)
                            flag_E=1
                            break
                    if flag_E==0:
                        data[i].append(0)
                    for k in a[i][j]:
                        if k=="西":
                            data[i].append(1)
                            flag_W=1
                            break
                    if flag_W==0:
                        data[i].append(0)
                elif j==3:
                    if a[i][j]=="简装":
                        data[i].append(0)
                    elif a[i][j]=="精装":
                        data[i].append(1)
                    else:
                        data[i].append(2)
                elif j==4:
                    find_2=re.search(r"共[0-9]+层",a[i][j])
                    find_3=re.search(r"[0-9]+",a[i][j])
                    if find_2!=None:
                        if "低楼层" in a[i][j]:
                            data[i].append(int(int(find_3.group())/6))
                        elif "中楼层" in a[i][j]:
                            data[i].append(int(int(find_3.group())/2))
                        elif "高楼层" in a[i][j]:
                            data[i].append(int(int(find_3.group())*5/6))
                        elif "顶层" in a[i][j]:
                            data[i].append(int(int(find_3.group())))
                        elif "底层" in a[i][j]:
                            data[i].append(1)
                        else:
                            data[i].append(a[i][j])
                            data[i].append(a[i][j])
                    else:
                        data[i].append(int(int(find_3.group())))
                elif j==6:
                    data[i].append(a[i][j])
        delete=[]
        j=0
        for i in range(len(data)):
            if len(data[i])>10:
                delete.append(i)
        for i in delete:
            del data[i-j]
            j=j+1
        return data
    def suggest(self,city,num):
        name_let=name_let_list("name-let.txt")
        for i in range(len(name_let)):
            if name_let[i][0]==city:
                let=name_let[i][1]
                break
        result=[]
        for i in range(5):
            sql_text_3 = "SELECT 位置,户型,面积,朝向,装修,楼层,结构,总价 FROM house WHERE 编号='{}{}'".format(let,str(num[i]+1))
            self.cur.execute(sql_text_3)
            a=self.cur.fetchall()
            result.append(a[0])
        now=datetime.datetime.now() 
        self.sheet.append(["预测{}二手房价格".format(city),"成功","",now.strftime("%Y-%m-%d %H:%M:%S"),""])#添加日志
        self.wb.save('log.xlsx')
        return result


db_user=Database_user()
db_house=Database_house()
if __name__=='__main__':
    print(db.check_login('neuer','12345'))
