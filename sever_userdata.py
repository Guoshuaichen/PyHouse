import sqlite3

# 创建与数据库的连接
conn = sqlite3.connect('user.db')
#创建一个游标 cursor
cur = conn.cursor()
a="DROP TABLE user"
cur.execute(a)
# 建表的sql语句
createtb = "CREATE TABLE user(username TEXT,密码 TEXT,primary key(username));"
#执行sql语句
cur.execute(createtb)


# 插入单条数据
sql_text_2 = "INSERT INTO user VALUES('neuer','12345')"
cur.execute(sql_text_2)
# 提交改动的方法
conn.commit()
sql_text_3 = "SELECT * FROM user"
cur.execute(sql_text_3)
# 获取查询结果
a=cur.fetchall()
print(a)

# 关闭游标
cur.close()
# 关闭连接
conn.close()
