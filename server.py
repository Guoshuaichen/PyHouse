#!/usr/bin/env python
# coding=utf-8
import socket
from sever_db import db_house
import sever_getdata
import time
import datetime
from threading import Timer
import numpy as np
from sklearn.linear_model import LinearRegression
import sklearn.linear_model as lm
#响应查询功能
def search_city(data):
    city=data[0]
    sql=data[1]
    order=data[2]
    result,count=db_house.search(city,sql,order)
    #print(result[1:10])
    #print(len(result))
    clnt.sendall(str(count).encode())
    if count!=0: 
        for i in range(count):
            for j in range(11):
                if j==4 or j==9 or j==10:
                    clnt.send(str(result[i][j]).encode())
                    clnt.send("?".encode())
                else:
                    clnt.send(result[i][j].encode())
                    clnt.send("?".encode())
                if i==count-1 and j==10:
                    clnt.send("end".encode())
#响应统计功能
def statistic_city():
    housenum=db_house.statistic()
    str_num=""
    for num in housenum:
        str_num=str_num+str(num)+"?"
    str_num=str_num+"end"
    clnt.send(str_num.encode())

#响应预测功能
def predict_price(data):
    data.remove("predict")
    #print(data)
    city=data[0]
    method=int(data[7])
    data.pop(-1)
    data.pop(0)
    #print(data)
    pred=[]
    for i in range(0,6):
        if i==3:
            flag_N=0
            flag_S=0
            flag_W=0
            flag_E=0
            for k in data[i]:
                 if k=="北":
                    pred.append(1)
                    flag_N=1
                    break
            if flag_N==0:
                pred.append(0)
            for k in data[i]:
                if k=="南":
                    pred.append(1)
                    flag_S=1
                    break
            if flag_S==0:
                pred.append(0)
            for k in data[i]:
                if k=="东":
                    pred.append(1)
                    flag_E=1
                    break
            if flag_E==0:
                pred.append(0)
            for k in data[i]:
                if k=="西":
                    pred.append(1)
                    flag_W=1
                    break
            if flag_W==0:
                pred.append(0)
        elif i==4:
            if data[i]=="简装":
                pred.append(0)
            elif data[i]=="精装":
                pred.append(1)
            elif data[i]=="其他":
                pred.append(2)
        elif i==2:
            pred.append(float(data[i]))
        else:
            pred.append(int(data[i]))
    
    print(pred)
    train=db_house.create_data(city)
    print(train)
    if method==1:
        price=int(MLR(train,pred))
    else:
        price=int(Ridge(train,pred))
    #print(price)
    clnt.send(str(price).encode())
    number=distance(train,pred)
    result=db_house.suggest(city,number)
    #print(result)
    for i in range(5):
        for j in range(8):
            if j==2 or j==7:
                clnt.send(str(result[i][j]).encode())
                clnt.send("?".encode())
            else:
                clnt.send(result[i][j].encode())
                clnt.send("?".encode())
        if i==4:
            clnt.send("end".encode())


    
#多元线性回归
def MLR(train,pred):
    train=np.array(train)
    x_train=train[0:int(train.shape[0]*0.8),0:-1]
    y_train=train[0:int(train.shape[0]*0.8),-1]
    x_test=train[int(train.shape[0]*0.8)+1:-1,0:-1]
    y_test=train[int(train.shape[0]*0.8)+1:-1,-1]
    model=LinearRegression(n_jobs=2)
    model.fit(x_train,y_train)
    x_pred=[]
    x_pred.append(np.array(pred))
    predict=model.predict(x_pred)
    score=model.score(x_test,y_test)
    print("MLR模型评估分数：",score)
    return predict

#岭回归
def Ridge(train,pred):
    train=np.array(train)
    x_train=train[0:int(train.shape[0]*0.8),0:-1]
    y_train=train[0:int(train.shape[0]*0.8),-1]
    x_test=train[int(train.shape[0]*0.8)+1:-1,0:-1]
    y_test=train[int(train.shape[0]*0.8)+1:-1,-1]
    model=lm.Ridge(150,fit_intercept=True, max_iter=1000)
    model.fit(x_train,y_train)
    x_pred=[]
    x_pred.append(np.array(pred))
    predict=model.predict(x_pred)
    score=model.score(x_test,y_test)
    print("Ridge模型评估分数：",score)
    return predict



#相似性度量
def distance(sets,data):
    dis_list=[]
    index_list=[]
    for i in sets:
        dis=0
        for j in range(len(data)):
          dis=dis+(i[j]-data[j])*(i[j]-data[j])
        dis_list.append(int(dis))
    #print(dis_list)
    for i in range(5):
        index=dis_list.index(min(dis_list))
        dis_list[index]=max(dis_list)
        index_list.append(index)
    #print(index_list)
    return index_list
        
    

#定时启动爬虫
def time_printer():
    now=datetime.datetime.now()
    ts=now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func time:',ts)
    get_data()
    loop_monitor()


#爬虫更新数据
def loop_monitor():
    t=Timer(10,time_printer)
    t.start()


host='127.0.0.1'
port=5000
s=socket.socket()
s.bind((host,port))#绑定
s.listen(5)#监听
clnt,addr=s.accept()
print("cline address:",addr)

while True:
    data=clnt.recv(1024)
    if data.decode()!="":
        data=data.decode().split("?")
        if "search" in data:
            search_city(data)
        elif "statistic" in data:
            statistic_city()
        elif "predict" in data:
            predict_price(data)
    
s.close()   
