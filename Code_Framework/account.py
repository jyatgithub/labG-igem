"""
用户的登录和注册功能
"""
import tkinter.messagebox
from tkinter import *

from CRUD_database import CRUD  # 导入GUI模块
from connect_database import connect_database  # 导入数据库链接模块
import uuid
conn, cursor = connect_database()  # 创建数据库操作对象，链接数据库
my_salt = "iGEM2024"  # 密码加盐，放在这作个提醒


class Main:
    def __init__(self):  # 窗口初始化
        self.window = Tk()  # 创建窗口
        self.window.title('中国科带学生信息管理系统-iGEM2024专属版:登录界面')  # 设置窗口标题
        self.window.geometry('600x400')  # 设置窗口大小
        self.window.resizable(False, False)  # 设置窗口大小不可变
        self.canvas = Canvas(self.window, height=400, width=600)  # 创建画布
        self.lb1 = Label(self.window, text='用户名：', width=7, height=2).place(x=200, y=150)  # 创建标签
        self.lb2 = Label(self.window, text=' 密码：', width=7, height=2).place(x=200, y=200)  # 创建标签
        self.get_user_name = StringVar()  # 创建字符串变量
        self.en_user_name = Entry(self.window, textvariable=self.get_user_name)  # 创建输入框
        self.en_user_name.place(x=260, y=150, height=40)  # 设置输入框位置
        self.get_user_pwd = StringVar()  # 创建字符串变量
        self.en_user_pwd = Entry(self.window, textvariable=self.get_user_pwd, show='*')  # 创建输入框
        self.en_user_pwd.place(x=260, y=200, height=40)  # 设置输入框位置
        self.bt_login = Button(self.window, text='登录', command=self.user_sign_in, width=10, height=2)  # 创建按钮
        self.bt_login.place(x=150, y=300)  # 设置按钮位置
        self.bt_logup = Button(self.window, text='注册', command=self.user_sign_up_window, width=10, height=2)
        self.bt_logup.place(x=250, y=300)
        self.bt_quit = Button(self.window, text='退出', command=self.window.destroy, width=10, height=2)
        self.bt_quit.place(x=350, y=300)
        self.window.mainloop()

    def user_sign_up_window(self):  # 用户注册功能GUI
        window_sign_up = tkinter.Toplevel(self.window)  # 创建注册窗口
        window_sign_up.title("中国科带学生信息管理系统-iGEM2024专属版:注册界面")
        window_sign_up.geometry('600x400')
        window_sign_up.resizable(False, False)
        lb3 = Label(window_sign_up, text="用户名：", width=7, height=2).place(x=200, y=100)
        lb4 = Label(window_sign_up, text="密码：", width=7, height=2).place(x=200, y=150)
        lb5 = Label(window_sign_up, text="确认密码:", width=7, height=2).place(x=200, y=200)
        self.new_user_name = tkinter.StringVar()
        en_new_name = Entry(window_sign_up, textvariable=self.new_user_name)
        en_new_name.place(x=260, y=100, height=40)
        self.new_user_pwd = tkinter.StringVar()
        en_use_pwd = Entry(window_sign_up, textvariable=self.new_user_pwd, show='*')
        en_use_pwd.place(x=260, y=150, height=40)
        self.new_cfrm_pwd = tkinter.StringVar()
        en_pwd_again = Entry(window_sign_up, textvariable=self.new_cfrm_pwd, show='*')
        en_pwd_again.place(x=260, y=200, height=40)
        bt1 = Button(window_sign_up, text="注册", command=self.user_sign_up, width=10, height=2)
        bt1.place(x=200, y=280)
        bt2 = Button(window_sign_up, text="取消", command=self.user_sign_up_cancel, width=10, height=2)
        bt2.place(x=300, y=280)

    def user_sign_up(self):  # 用户注册功能实现
        new_name = self.new_user_name.get()
        new_pwd = self.new_user_pwd.get()
        new_confirm_pwd = self.new_cfrm_pwd.get()
        try:
            cursor.execute("SELECT * FROM adm_account WHERE username=%(n1)s", {"n1": new_name})  # 例子：字典用法
            result = cursor.fetchone()  # 获取单条查询数据
            if new_pwd == "" or new_confirm_pwd == "" or new_name == "":  # 判断用户名或密码是否为空
                tkinter.messagebox.showerror(title="注册时出现错误", message="用户名或密码不能为空")
            elif result is not None:  # 判断用户名是否已被注册
                tkinter.messagebox.showerror(title="注册时出现错误", message="用户名已被注册")
            elif new_pwd == new_confirm_pwd:  # 两次密码是否一致，允许注册
                try:
                    sql = "SET @salt = UUID()"  # 生成盐，存储于salt字段
                    cursor.execute(sql)
                    sql = "SET @key = CONCAT(@salt, 'iGEM2024')"  # 生成密钥
                    cursor.execute(sql)
                    sql = "INSERT INTO adm_account(username, password, salt) values (%(n1)s, AES_ENCRYPT(%(n2)s, @key), @salt)"# TODO:生成加密密码的SQL语句
                    cursor.execute(sql, {"n1": new_name, "n2": new_pwd})  # 参考这里编写SQL语句
                    conn.commit()  # SQL的部分语句需要这么提交一下才能生效
                    tkinter.messagebox.showinfo(title="注册成功", message=f"恭喜{new_name}注册成功，请前往登陆!")
                    self.window.destroy()
                    Main()  # 重新打开登录窗口
                except Exception as e:
                    tkinter.messagebox.showerror(e)
            else:  # 两次密码不一致
                tkinter.messagebox.showerror(title="注册时出现错误", message="两次密码不一致")
        except Exception as e:
            tkinter.messagebox.showerror(e)

    def user_sign_up_cancel(self):  # 取消注册
        conn.close()  # 关闭数据库连接
        self.window.destroy()
        Main()  # 重新打开登录窗口

    def user_sign_in(self):  # 用户登录功能实现
        user_name = self.get_user_name.get()  # 获取用户名
        user_pwd = self.get_user_pwd.get()  # 获取密码
        try:
            cursor.execute("SELECT salt FROM adm_account WHERE username = %(n1)s", {"n1": user_name})
            salt_result = cursor.fetchone()
            if salt_result:
                salt = salt_result[0]
                cursor.execute("SET @key = CONCAT(%s, 'iGEM2024')", (salt,))

            sql = "SELECT username, AES_DECRYPT(password, @key) FROM adm_account WHERE username = %(n1)s"  # TODO：编写查询账户——密码的SQL语句，用于获取查询账户——密码元组
            cursor.execute(sql, {"n1": user_name})
            acc_pwd_tuple = cursor.fetchall()  # 获取账户——明文密码元组
            print(acc_pwd_tuple)  # 调试用：在终端打印账户——明文密码元组

            if user_name == "" or user_pwd == "":  # 判断用户名或密码是否为空
                tkinter.messagebox.showerror(title="Error", message="用户名或密码不能为空！")
            else:  # 用户名和密码不为空，开始验证
                flag = None
                for row in acc_pwd_tuple:
                    db_username, db_password = row[0], row[1]
                    db_password = db_password.decode('utf-8')
                    if user_name == db_username and user_pwd == db_password:
                        flag = True
                        break
                # TODO: 请在这里编写验证账户——密码的代码。
                # 提示：遍历账户——密码元组，将账户——密码元组（acc_pwd_tuple）中的账户和密码分别与用户输入的账户和密码进行比对，
                # 假如找到了账户和密码都匹配的元组，就将flag置为True，然后跳出循环。

                if flag is not None:  # 用户名和密码正确
                    tkinter.messagebox.showinfo(title="Welcome!", message="欢迎" + str(user_name))
                    self.window.destroy()
                    CRUD()
                else:  # 用户名或密码错误
                    tkinter.messagebox.showerror(title="Error", message="用户名或密码错误，再试一次吧！")

        except Exception:
            tkinter.messagebox.showerror("登录异常！")
