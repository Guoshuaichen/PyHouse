import tkinter as tk
from tkinter import messagebox
from sever_db import db_user
from clnt_MainPage import MainPage
class LoginPage:
    def __init__(self,master):
        self.root=master
        self.root.geometry('500x280')
        self.root.title('登录页')
        self.username=tk.StringVar()
        self.password=tk.StringVar()
        self.page=tk.Frame(root)
        self.page.pack()
        #tk.Label(self.page).grid(row=0,column=0)
        tk.Label(self.page,text='欢迎使用二手房信息查询系统',font=("宋体",18)).place(x=0,y=10)
        tk.Label(self.page,text='    用户名：',font=("宋体",18)).grid(row=2,column=1,pady=50)
        tk.Entry(self.page,textvariable=self.username).grid(row=2,column=2)
        tk.Label(self.page,text='     ',font=("宋体",18)).grid(row=2,column=3,pady=50)
        tk.Label(self.page,text='    密码：',font=("宋体",18)).grid(row=3,column=1)
        tk.Entry(self.page,textvariable=self.password,show='*').grid(row=3,column=2)
        tk.Label(self.page,text='     ',font=("宋体",18)).grid(row=3,column=3)
        tk.Button(self.page,text='登录',command=self.login,width=10,height=2).grid(row=4,column=1,pady=40)
        tk.Button(self.page,text='注册',command=self.sign,width=10,height=2).grid(row=4,column=2,pady=40)
        tk.Button(self.page,text='退出',command=self.page.quit,width=10,height=2).grid(row=4,column=3,pady=40)
    def login(self):
        name=self.username.get()
        pwd=self.password.get()
        flag,message=db_user.check_login(name,pwd)
        if flag:
            self.page.destroy()
            MainPage(self.root)
        else:
            messagebox.showwarning(title='警告',message=message)
    def sign(self):
        name=self.username.get()
        pwd=self.password.get()
        flag,message=db_user.sign(name,pwd)
        if flag:
            messagebox.showwarning(title='新用户注册',message=message)
        else:
            messagebox.showwarning(title='警告',message=message)
if __name__=='__main__':
    root=tk.Tk()
    login=LoginPage(master=root)
    root.mainloop()
    


