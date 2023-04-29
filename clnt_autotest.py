#!/usr/bin/env python
# coding=utf-8
import socket
from sever_getdata import name_let_list
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
def auto_search_request():
    name_let=name_let_list("name-let.txt")
    method=["面积","总价","单价"]
    #city=input('please input city:')
    city=name_let[random.randint(0,27)][0]
    rand=random.randint(0,2)
    sql="SELECT * FROM house WHERE 城市 like '%{}%' order by '{}'".format(city,method[rand])
    order="按面积查询"
    request=city+"?"+sql+"?"+order+"?"+"search"
    s.send(request.encode())
    count=s.recv(1024)
    if int(count.decode())!=0:
        result=""
        while True:
            data=s.recv(1024)
            data=data.decode("utf-8","ignore")
            result=result+data
            if "end" in data:
                break
        result=result.split("?")
        result.remove("end")
        print(result)
        print(len(result))

def auto_statistic_request():
    request="statistic"
    s.send(request.encode())
    result=""
    while True:
        data=s.recv(1024)
        data=data.decode()
        result=result+data
        if "end" in data:
            break
    result=result.split("?")
    result.remove("end")
    print(result)
    chart(result)

def chart(result):
    name_let=name_let_list("name-let.txt")
    cityname=[x[0] for x in name_let]
    x=np.arange(len(cityname))
    housenum=[int(i) for i in result]
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    bar_width = 0.5
    plt.bar(x,housenum,bar_width, align="center", color="c", label="数量", alpha=0.5)
    plt.tight_layout(pad=0.4, w_pad=10.0, h_pad=3.0)
    plt.title('各市二手房数量统计表')
    plt.xlabel("城市")
    plt.ylabel("二手房数量")
    plt.xticks(x,cityname,size=8)
    plt.xticks(rotation=-45)
    plt.yticks(np.arange(0, 151, 30))
    plt.legend(loc="upper left")
    plt.show()
    

s=socket.socket()
s.connect(('127.0.0.1',5000))
name_let=name_let_list("name-let.txt")
for i in range(5):
    auto_search_request()
auto_statistic_request()
s.close()
