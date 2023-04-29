import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sever_db import db_house
from tkinter import *
import sqlite3
import time
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from sever_getdata import name_let_list
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import socket
from clnt_socket import clnt
import numpy as np
from sklearn.linear_model import LinearRegression
import re
class SearchFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.table_view=tk.Frame()
        self.table_view.pack()
        self.cityname=tk.StringVar()
        tk.Label(self,text='您想查询的省会城市',font=("宋体",12)).place(x=300,y=0)
        tk.Entry(self,textvariable=self.cityname,bd=3,width=10).place(x=460,y=0)
        tk.Button(self,text='按面积排序',width=10,height=1,command=self.show_area).place(x=600,y=0)
        tk.Button(self,text='按总价排序',width=10,height=1,command=self.show_total).place(x=685,y=0)
        tk.Button(self,text='按单价排序',width=10,height=1,command=self.show_unit).pack(anchor='e')
        self.label=tk.Label(self,text='请开始查询',font=("宋体",10))
        self.label.pack(anchor=tk.E,pady=10)
        self.progressbarOne = tk.ttk.Progressbar(self)
        self.progressbarOne.pack(side=tk.TOP)
        self.create_page()
        tk.Button(self,text='退出',width=5,height=1,command=self.quit).pack(anchor='se')

    def create_page(self):
        columns=("city","locate","shape","area","direction","level","floor","struct","total_price","unit_price")
        columns_values=("城市","位置","户型","面积","朝向","装修","楼层","结构","总价","单价")
        self.tree_view=ttk.Treeview(self,show='headings',columns=columns)
        self.tree_view.column('city',width=43,anchor='center')
        self.tree_view.column('locate',width=200,anchor='center')
        self.tree_view.column('shape',width=50,anchor='center')
        self.tree_view.column('area',width=80,anchor='center')
        self.tree_view.column('direction',width=70,anchor='center')
        self.tree_view.column('level',width=50,anchor='center')
        self.tree_view.column('floor',width=100,anchor='center')
        self.tree_view.column('struct',width=120,anchor='center')
        self.tree_view.column('total_price',width=60,anchor='center')
        self.tree_view.column('unit_price',width=80,anchor='center')
        self.tree_view.heading('city',text='编号')
        self.tree_view.heading('locate',text='位置')
        self.tree_view.heading('shape',text='户型')
        self.tree_view.heading('area',text='面积(平米)')
        self.tree_view.heading('direction',text='朝向')
        self.tree_view.heading('level',text='装修')
        self.tree_view.heading('floor',text='楼层')
        self.tree_view.heading('struct',text='结构')
        self.tree_view.heading('total_price',text='总价(万)')
        self.tree_view.heading('unit_price',text='单价(元/平)')
        self.tree_view.pack()
        self.VScroll1 = Scrollbar(self, orient='vertical', command=self.tree_view.yview)
        self.VScroll1.place(x=875,y=20)
        # 给treeview添加配置
        self.tree_view.configure(yscrollcommand=self.VScroll1.set)

    def show_area(self):
        for _ in map(self.tree_view.delete,self.tree_view.get_children('')):
            pass
        self.label.pack_forget()
        city=self.cityname.get()
        sql_text_1 = "SELECT * FROM house WHERE 城市 like '%{}%' order by 面积".format(city)
        order="按面积查询"
        self.search_db(city,sql_text_1,order)

    def show_total(self):
        for _ in map(self.tree_view.delete,self.tree_view.get_children('')):
            pass
        self.label.pack_forget()
        city=self.cityname.get()
        sql_text_1 = "SELECT * FROM house WHERE 城市 like '%{}%' order by 总价".format(city)
        order="按总价查询"
        self.search_db(city,sql_text_1,order)
    def show_unit(self):
        for _ in map(self.tree_view.delete,self.tree_view.get_children('')):
            pass
        self.label.pack_forget()
        city=self.cityname.get()
        sql_text_1 = "SELECT * FROM house WHERE 城市 like '%{}%' order by 单价".format(city)
        order="按单价查询"
        self.search_db(city,sql_text_1,order)
        
    def show(self):
        # 进度值最大值
        self.progressbarOne['maximum'] = 100
        # 进度值初始值
        self.progressbarOne['value'] = 0
        for i in range(100):
            time.sleep(0.005)
            self.progressbarOne['value'] += 1
            self.update()

    def search_db(self,city,sql_text_1,order):
        self.show()
        request=city+"?"+sql_text_1+"?"+order+"?"+"search"
        clnt.s.send(request.encode())
        count=clnt.s.recv(1024)
        result=""
        if int(count.decode())==0:
            messagebox.showwarning(title='警告',message="暂无该城市二手房信息")
        else:
            if city=="":
                messagebox.showwarning(title='警告',message="请输入具体城市")
            while True:
                data=clnt.s.recv(1024)
                data=data.decode("utf-8","ignore")
                result=result+data
                if "end" in data:
                    break
            result=result.split("?")
            result.remove("end")
            #print(result)
            #print(len(result))
        index=0
        x=0
        house=[]
        for info in result:
            house.append(info)
            x=x+1
            if x==11:
                self.tree_view.insert("",index+1,value=(house[0],house[2],house[3],house[4],house[5],house[6],house[7],house[8],house[9],house[10]))
                x=0
                house=[]
                index=index+1
        self.label=tk.Label(self,text='共查询到{}套房源信息'.format(index),font=("宋体",10))
        self.label.pack(anchor=tk.E,pady=10)

class StaticsFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        tk.Label(self,text='各城市二手房数量统计\n本系统共包含28个省会城市的二手房信息').pack()
        self.create_page()
        tk.Button(self,text='查看柱状图',width=15,height=1,command=self.chart).pack(anchor='s')
        tk.Button(self,text='退出',width=5,height=1,command=self.quit).pack(anchor='se')
    def create_page(self):
        columns=("city","number")
        columns_values=("城市","数量")
        self.tree_view=ttk.Treeview(self,show='headings',columns=columns)
        self.tree_view.column('city',width=80,anchor='center')
        self.tree_view.column('number',width=80,anchor='center')
        self.tree_view.heading('city',text='城市')
        self.tree_view.heading('number',text='数量')
        self.tree_view.pack()
        self.show_treeview()
        

    def show_treeview(self):
        for _ in map(self.tree_view.delete,self.tree_view.get_children('')):
            pass
        self.name_let=name_let_list("name-let.txt")
        self.cityname=[x[0] for x in self.name_let]
        request="statistic"
        clnt.s.send(request.encode())
        self.result=""
        while True:
            data=clnt.s.recv(1024)
            data=data.decode()
            self.result=self.result+data
            if "end" in data:
                break
        self.result=self.result.split("?")
        self.result.remove("end")
        for i in range(len(self.result)):
            self.tree_view.insert("",i+1,value=(self.cityname[i],str(self.result[i])))

        
    def chart(self):
        x=np.arange(len(self.cityname))
        housenum=[int(i) for i in self.result]
        mpl.rcParams["font.sans-serif"] = ["SimHei"]
        bar_width = 0.5
        plt.bar(x,housenum,bar_width, align="center", color="c", label="数量", alpha=0.5)
        plt.tight_layout(pad=0.4, w_pad=10.0, h_pad=3.0)
        plt.title('各市二手房数量统计表')
        plt.xlabel("城市")
        plt.ylabel("二手房数量")
        plt.xticks(x,self.cityname,size=8)
        plt.xticks(rotation=-45)
        plt.yticks(np.arange(0, 151, 30))
        plt.legend(loc="upper left")
        plt.show()
        
class PredictFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.city=tk.StringVar()
        self.room_s=tk.StringVar()
        self.room_t=tk.StringVar()
        self.area=tk.StringVar()
        self.dirc=tk.StringVar()
        self.fix=tk.StringVar()
        self.floor=tk.StringVar()
        self.method=tk.IntVar()
        self.method=0
        self.create_page()

        
    def create_page(self):
        city_label=tk.Label(self,text='城市',font=("宋体",12))
        city_label.grid(row=0,column=0,pady=30)
        city_com=ttk.Combobox(self,textvariable=self.city,width=5)
        city_com.grid(row=0,column=1)
        city_com["value"]=("北京","上海","广州")
        city_com.configure(state="readonly")
        
        room_s_com=ttk.Combobox(self,textvariable=self.room_s,width=3)
        room_s_com.grid(row=0,column=2,padx=(20,0))
        room_s_com["value"]=(1,2,3,4,5)
        room_s_label=tk.Label(self,text='室',font=("宋体",12))
        room_s_label.grid(row=0,column=3)
        room_s_com.configure(state="readonly")
        
        room_t_com=ttk.Combobox(self,textvariable=self.room_t,width=3)
        room_t_com.grid(row=0,column=4)
        room_t_com["value"]=(1,2,3,4,5)
        room_t_label=tk.Label(self,text='厅',font=("宋体",12))
        room_t_label.grid(row=0,column=5)
        room_t_com.configure(state="readonly")

        area_label=tk.Label(self,text='面积(m²)',font=("宋体",12))
        area_label.grid(row=0,column=6,padx=(20,0))
        area_entry=tk.Entry(self,textvariable=self.area,bd=3,width=8)
        area_entry.grid(row=0,column=7)

        dirc_label=tk.Label(self,text='朝向',font=("宋体",12))
        dirc_label.grid(row=0,column=8,padx=(20,0))
        dirc_com=ttk.Combobox(self,textvariable=self.dirc,width=5)
        dirc_com.grid(row=0,column=9)
        dirc_com["value"]=("东","南","西","北","东西","南北","西北","西南","东北","东南","东南北","西南北","东西北","东西南","东西南北")
        dirc_com.configure(state="readonly")

        fix_label=tk.Label(self,text='装修',font=("宋体",12))
        fix_label.grid(row=0,column=10,padx=(20,0))
        fix_com=ttk.Combobox(self,textvariable=self.fix,width=5)
        fix_com.grid(row=0,column=11)
        fix_com["value"]=("简装","精装","其他")
        fix_com.configure(state="readonly")
        
        floor_label=tk.Label(self,text='楼层',font=("宋体",12))
        floor_label.grid(row=0,column=12,padx=(20,0))
        floor_entry=tk.Entry(self,textvariable=self.floor,bd=3,width=8)
        floor_entry.grid(row=0,column=13)

        method1=Radiobutton(self,text="线性回归预测",variable=self.method,value=1,command=self.select1)
        method1.grid(row=1,column=6,columnspan=2)
        method2=Radiobutton(self,text="岭回归预测",variable=self.method,value=2,command=self.select2)
        method2.grid(row=1,column=8,columnspan=2)
        
        pred=tk.Button(self,text='预测',width=10,height=1,command=self.predict)
        pred.grid(row=1,column=10)

        self.progressbarOne = tk.ttk.Progressbar(self)
        self.progressbarOne.grid(row=2,column=7)
        
        quit_button=tk.Button(self,text='退出',width=5,height=1,command=self.quit)
        quit_button.grid(row=5,column=12,pady=20)
        
        
    def predict(self):
        city=self.city.get()
        room_s=self.room_s.get()
        room_t=self.room_t.get()
        area=self.area.get()
        dirc=self.dirc.get()
        fix=self.fix.get()
        floor=self.floor.get()      
        if city=="":
            messagebox.showwarning(title='警告',message="请选择城市")
        else:
            if room_s=="":
                messagebox.showwarning(title='警告',message="请选择户型")
            else:
                if room_t=="":
                    messagebox.showwarning(title='警告',message="请选择户型")
                else:
                    if area=="" or isreal(area)==False:
                        messagebox.showwarning(title='警告',message="请重新输入面积")
                    else:
                        if dirc=="":
                            messagebox.showwarning(title='警告',message="请选择朝向")
                        else:
                            if fix=="":
                                messagebox.showwarning(title='警告',message="请选择装修类别")
                            else:
                                if floor=="" or isint(floor)==False:
                                    messagebox.showwarning(title='警告',message="请重新输入楼层")
                                else:
                                    if self.method==0:
                                        messagebox.showwarning(title='警告',message="请选择预测方法")
                                    else:
                                        request=city+"?"+room_s+"?"+room_t+"?"+area+"?"+dirc+"?"+fix+"?"+floor+"?"+str(self.method)+"?"+"predict"
                                        clnt.s.send(request.encode())
                                        
                                        data=clnt.s.recv(1024)
                                        price=data.decode()
                                        self.show()
                                        self.create_treeview(price)
                                        self.show_treeview()
                                        

    def create_treeview(self,price):
        price_label=tk.Label(self,text='  估价：',font=("宋体",12))
        price_label.grid(row=1,column=11)
        price_text=tk.Label(self,text='{}万'.format(price),font=("宋体",12))
        price_text.grid(row=1,column=12)
        tk.Label(self,text='系统为您匹配的最相似的5个房源如下',font=("宋体",12)).grid(row=3,column=6,columnspan=4,pady=10)
        columns=("locate","shape","area","direction","level","floor","struct","total_price")
        columns_values=("位置","户型","面积","朝向","装修","楼层","结构","总价")
        self.tree_view=ttk.Treeview(self,show='headings',columns=columns,height=5)
        self.tree_view.column('locate',width=200,anchor='center')
        self.tree_view.column('shape',width=50,anchor='center')
        self.tree_view.column('area',width=80,anchor='center')
        self.tree_view.column('direction',width=70,anchor='center')
        self.tree_view.column('level',width=50,anchor='center')
        self.tree_view.column('floor',width=100,anchor='center')
        self.tree_view.column('struct',width=120,anchor='center')
        self.tree_view.column('total_price',width=60,anchor='center')
        self.tree_view.heading('locate',text='位置')
        self.tree_view.heading('shape',text='户型')
        self.tree_view.heading('area',text='面积(平米)')
        self.tree_view.heading('direction',text='朝向')
        self.tree_view.heading('level',text='装修')
        self.tree_view.heading('floor',text='楼层')
        self.tree_view.heading('struct',text='结构')
        self.tree_view.heading('total_price',text='总价(万)')
        self.tree_view.grid(row=4,column=0,columnspan=15,padx=20,pady=10)
        
    def show_treeview(self):
        for _ in map(self.tree_view.delete,self.tree_view.get_children('')):
            pass
        result=""
        while True:
            data=clnt.s.recv(1024)
            data=data.decode("utf-8","ignore")
            result=result+data
            if "end" in data:
                break
        result=result.split("?")
        result.remove("end")
        print(result)
        index=0
        x=0
        house=[]
        for info in result:
            house.append(info)
            x=x+1
            if x==8:
                self.tree_view.insert("",index+1,value=(house[0],house[1],house[2],house[3],house[4],house[5],house[6],house[7]))
                x=0
                house=[]
                index=index+1

    def select1(self):
        self.method=1

    def select2(self):
        self.method=2

    def show(self):
        # 进度值最大值
        self.progressbarOne['maximum'] = 100
        # 进度值初始值
        self.progressbarOne['value'] = 0
        for i in range(100):
            time.sleep(0.005)
            self.progressbarOne['value'] += 1
            self.update()


class AboutFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        tk.Label(self,text='关于作品：本作品使用tkinter制作\n旨在帮助用户查询二手房信息').pack()
        tk.Label(self,text='关于作者：计算机2006郭帅辰').pack()



def isreal(area):
    flag=0
    dot=0
    for i in area:
        if i>='0' and i<='9' or i=='.':
            if i=='.' and dot==0:
                dot=1
            elif i=='.' and dot==1:
                flag=1
                break
        else:
            flag=1
            break
    if flag==1:
        return False
    else:
        return True

def isint(floor):
    flag=0
    for i in floor:
        if i>='0' and i<='9':
            continue
        else:
            flag=1
            break
    if flag==1:
        return False
    else:
        return True

