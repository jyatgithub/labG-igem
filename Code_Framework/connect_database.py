"""
本模块已经由我实现，大家只需要按照TODO填上用户名和密码就可以了
"""

import pymysql  # 导入pymysql模块，用于连接数据库


# 数据库链接
def connect_database():
    conn = pymysql.connect(host='localhost',
                           user='root',  # TODO：请改成你的数据库用户名，默认应该是'root'
                           password='2005jy0326',  # TODO：请改成你的数据库密码，即注册时设置的密码，如'123456'
                           database='igem001',  # 这个我们统一吧。。。
                           )  # 连接数据库
    cursor = conn.cursor()  # 创建游标，用于执行SQL语句。我们后面的操作都是通过该对象来实现的
    return conn, cursor  # 返回连接对象和游标对象


# 连接数据库测试
conn, cursor = connect_database()

sql = "SELECT * FROM adm_account"  # 查询数据的SQL语句，还记得“MySQL基础”吗？

cursor.execute(sql)  # 执行SQL语句

result = cursor.fetchall()  # 获取查询数据
cursor.close()
conn.close()

print(result)  # 打印下查询结果
