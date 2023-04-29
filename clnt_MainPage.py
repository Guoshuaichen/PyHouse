import tkinter as tk
from tkinter import messagebox
from sever_db import db_house
from clnt_views import AboutFrame,SearchFrame,StaticsFrame,PredictFrame
from PIL import ImageTk
from PIL import Image
from tkinter import *
import socket
class MainPage:
    def __init__(self,master):
        self.root=master
        self.root.geometry('900x400')
        self.root.title('二手房数据分析系统 v0.0.1')
        self.create_page()
    def create_page(self):
        self.about_frame=AboutFrame(self.root)
        self.search_frame=SearchFrame(self.root)
        self.statics_frame=StaticsFrame(self.root)
        self.predict_frame=PredictFrame(self.root)
        self.show_search()
        menubar=tk.Menu(self.root)
        menubar.add_command(label='查询',command=self.show_search)
        menubar.add_command(label='统计',command=self.show_statics)
        menubar.add_command(label='预测',command=self.show_predict)
        menubar.add_command(label='关于',command=self.show_about)
        self.root['menu']=menubar
    def show_search(self):
        self.search_frame.pack()
        self.statics_frame.pack_forget()
        self.predict_frame.pack_forget()
        self.about_frame.pack_forget()

    
    def show_statics(self):
        self.search_frame.pack_forget()
        self.statics_frame.pack()
        self.predict_frame.pack_forget()
        self.about_frame.pack_forget()
    
    def show_predict(self):
        self.search_frame.pack_forget()
        self.statics_frame.pack_forget()
        self.predict_frame.pack()
        self.about_frame.pack_forget()

    def show_about(self):
        self.search_frame.pack_forget()
        self.statics_frame.pack_forget()
        self.predict_frame.pack_forget()
        self.about_frame.pack()

    
        

        

if __name__=='__main__':
    root=tk.Tk()
    MainPage(master=root)
    root.mainloop()
    


