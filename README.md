# PyHouse
软件工程大作业：用python编写的“派豪室”—身边的二手房管家软件
文件介绍：
共有9个py文件，其中以clnt开头的5个文件为客户端界面相关文件，以sever开头的4个文件为服务器端文件。
客户端文件：
clnt_autotest.py文件为自动化测试脚本，用于软件测试时用
clnt_LoginPage.py文件为登录界面脚本
clnt_MainPage.py文件为主界面脚本
clnt_socket.py文件为socket通信脚本，用于客户端与服务器端通信
clnt_views.py文件为各个界面上的显示文件以及方法实现
服务器端文件：
sever.py文件为服务器端启动文件
sever_db.py文件为服务器端数据库相关操作脚本
sever_getdata.py文件为服务器端爬取数据脚本
sever_userdata.py文件为服务器端记录用户信息脚本
日志文件：
log.xlsx，记录了用户使用本软件的操作
name-let.txt记录了省会的中文与其对应的拼音首字母
数据库文件：
house.db：房源信息数据库
user.db:用户信息数据库
使用方法：
首先运行sever.py文件启动服务器，然后运行clnt_LoginPage登录即可。
