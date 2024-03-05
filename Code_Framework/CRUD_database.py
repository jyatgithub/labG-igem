"""
数据库的增删改查操作
"""
# 导入所需模块
import tkinter
from tkinter import *
from tkinter import ttk, messagebox

from connect_database import connect_database

# 链接数据库
conn, cursor = connect_database()


# 主界面的初始化
class CRUD:
    def __init__(self):  # 主界面GUI设计
        self.window = Tk()  # 创建窗口
        self.window.title('中国科带学生信息管理系统-iGEM2024专属版')  # 设置窗口标题
        self.window.geometry('750x450')  # 设置窗口大小
        self.window.resizable(False, False)  # 设置窗口大小不可变
        bt1 = Button(self.window, text='添加学生信息', command=self.insert_window, width=10, height=2)  # 创建按钮
        bt1.place(x=70, y=190)  # 设置按钮位置
        bt2 = Button(self.window, text='删除学生信息', command=self.delete_item, width=10, height=2)
        bt2.place(x=70, y=260)
        bt3 = Button(self.window, text='修改学生信息', command=self.update_window, width=10, height=2)
        bt3.place(x=70, y=330)
        lb4 = Label(self.window, text='学号：', width=7, height=2).place(x=200, y=20)  # 创建标签
        lb5 = Label(self.window, text='姓名：', width=7, height=2).place(x=200, y=70)
        lb6 = Label(self.window, text='专业：', width=7, height=2).place(x=200, y=120)
        bt4 = Button(self.window, text='           查询           ', command=self.search, width=10, height=2).place(
            x=450, y=120)  # 创建按钮
        bt5 = Button(self.window, text="退出系统", width=10, height=2, command=self.exit)  # 创建按钮
        bt5.place(x=550, y=120)

        bt6 = Button(self.window, text="刷新数据", width=10, height=2, command=self.refresh)  # 创建按钮
        bt6.place(x=650, y=120)

        # 查询条件输入框
        self.stu_id = StringVar()  # 创建字符串变量
        self.en_stu_id = Entry(self.window, textvariable=self.stu_id)  # 创建输入框
        self.en_stu_id.place(x=270, y=20, height=40)  # 设置输入框位置

        self.stu_name = StringVar()
        self.en_stu_name = Entry(self.window, textvariable=self.stu_name)
        self.en_stu_name.place(x=270, y=70, height=40)

        self.stu_major = StringVar()
        self.en_stu_major = Entry(self.window, textvariable=self.stu_major)
        self.en_stu_major.place(x=270, y=120, height=40)

        self.tree = ttk.Treeview(self.window, show="headings")  # 创建表格
        self.tree["columns"] = ("0", "1", "2", "3", "4")  # 设置表格列名
        self.tree.place(x=200, y=180)  # 设置表格位置
        self.tree.column('0', width=100, anchor='center')  # 设置表格列宽和对齐方式
        self.tree.column('1', width=100, anchor='center')
        self.tree.column('2', width=100, anchor='center')
        self.tree.column('3', width=100, anchor='center')
        self.tree.column('4', width=100, anchor='center')
        self.tree.heading('0', text='姓名')  # 设置表头
        self.tree.heading('1', text='性别')
        self.tree.heading('2', text='学号')
        self.tree.heading('3', text='棘皮埃')
        self.tree.heading('4', text='专业')
        result = self.show()  # 查询除了id之外的所有信息
        for res in result:  # 将查询结果显示在表格中
            res_list = [res[0], res[1], res[2], res[3], res[4]]  # 将查询结果转换为列表
            self.tree.insert('', 'end', values=res_list)  # 将列表插入表格中
        self.window.mainloop()

    def insert_window(self):  # 添加学生信息的GUI
        window_insert = tkinter.Toplevel(self.window)
        window_insert.title("增加学生信息")
        window_insert.geometry('500x400')
        window_insert.resizable(False, False)
        Label(window_insert, text="学号：").place(x=100, y=70)
        Label(window_insert, text="姓名：").place(x=100, y=110)
        Label(window_insert, text="性别:").place(x=100, y=150)
        Label(window_insert, text="棘皮埃:").place(x=100, y=190)
        Label(window_insert, text="专业:").place(x=100, y=230)
        self.new_stu_id = tkinter.StringVar()  # 创建字符串变量
        en_new_id = Entry(window_insert, textvariable=self.new_stu_id)  # 创建输入框
        en_new_id.place(x=160, y=70)  # 设置输入框位置
        self.new_name = tkinter.StringVar()
        en_use_name = Entry(window_insert, textvariable=self.new_name)
        en_use_name.place(x=160, y=110)
        self.new_gender = tkinter.StringVar()
        en_new_sex = Entry(window_insert, textvariable=self.new_gender)
        en_new_sex.place(x=160, y=150)
        self.new_gpa = tkinter.StringVar()
        en_new_score = Entry(window_insert, textvariable=self.new_gpa)
        en_new_score.place(x=160, y=190)
        self.new_major = tkinter.StringVar()
        en_major = Entry(window_insert, textvariable=self.new_major)
        en_major.place(x=160, y=230)
        bt1 = Button(window_insert, text="添加", command=self.insert_item, width=10, height=2)
        bt1.place(x=100, y=290)
        bt2 = Button(window_insert, text="取消", command=window_insert.destroy, width=10, height=2)
        bt2.place(x=280, y=290)

    def insert_item(self):  # 添加学生信息的实现
        new_stu_id = self.new_stu_id.get()
        new_name = self.new_name.get()
        new_gender = self.new_gender.get()
        new_major = self.new_major.get()
        new_gpa = self.new_gpa.get()
        try:  # 先判断学生信息是否已存在
            cursor.execute("SELECT * FROM stu_info WHERE id=%(n1)s OR name=%(n2)s",
                           {"n1": new_stu_id, "n2": new_name})  #  TODO: 编写查询语句，通过学号和姓名查询学生信息是否已存在
            result = cursor.fetchone()  # 获取查询结果
            # print(result)
            if result is not None:
                tkinter.messagebox.showerror(title="Error", message="该学生信息已存在")
            else:
                try:
                    sql = "INSERT INTO stu_info (name, gender, stu_id, GPA, major) VALUES (%(n1)s, %(n2)s, %(n3)s, %(n4)s, %(n5)s )"  # TODO：编写插入语句，插入学生的名字、性别、学号、GPA、专业（注意按照顺序哦，否则和GUI对不上）
                    cursor.execute(sql,
                                   {"n1": new_name, "n2": new_gender, "n3": new_stu_id, "n4": new_gpa, "n5": new_major})
                    conn.commit()  # 插入数据需要提交
                    tkinter.messagebox.showinfo(title="添加成功", message=f"成功添加了学生{new_name}的信息")

                except Exception:
                    tkinter.messagebox.showerror("添加异常I！")

        except Exception:
            tkinter.messagebox.showerror("添加异常II！")

    def delete_item(self):  # 删除学生信息的实现
        if self.tree.selection() == ():  # 判断是否选中学生
            tkinter.messagebox.showinfo(title="提示", message="请先选择需要删除的学生")  # 未选中则提示
        for item in self.tree.selection():  # 获取所选行的值
            item_text = self.tree.item(item, "values")
            try:
                sql = "DELETE FROM stu_info WHERE stu_id=%(n1)s AND name=%(n2)s"  # TODO: 编写删除语句，通过学号和姓名删除学生信息
                cursor.execute(sql, {"n1": item_text[2], "n2": item_text[0]})
                # 注：试着用print研究一下这个item_text[2]和item_text[0]是什么
                print(item_text[2],item_text[0])
                conn.commit()

                # 从数据库中删除成功后，还要删除表格中的数据
                result = self.show()  # 查询所有信息
                all_items = self.tree.get_children()  # 获取表格中的所有数据
                for item2 in all_items:
                    self.tree.delete(item2)  # 删除表格中的所有数据
                for res in result:  # 重新将查询结果显示在表格中
                    list = [res[0], res[1], res[2], res[3], res[4]]
                    self.tree.insert('', 'end', values=list)
            except Exception:
                tkinter.messagebox.showerror("删除失败")
                conn.rollback()  # 回滚（数据库数据回到删除前的状态）

    def update_window(self):  # 修改学生信息的GUI
        if self.tree.selection() == ():  # 判断是否选中
            tkinter.messagebox.showinfo(title="提示", message="请先选择需要修改的学生")  # 未选中则提示
        else:
            for item in self.tree.selection():  # 获取所选行的值
                item_text = self.tree.item(item, "values")  # 获取所选行的数据，用于查询
                # print(f"item_text:{item_text}")
                window_insert = tkinter.Toplevel(self.window)
                window_insert.title("修改学生信息")
                window_insert.geometry('500x400')
                window_insert.resizable(False, False)
                Label(window_insert, text="学号：").place(x=100, y=70)
                Label(window_insert, text="姓名：").place(x=100, y=110)
                Label(window_insert, text="性别:").place(x=100, y=150)
                Label(window_insert, text="棘皮埃:").place(x=100, y=190)
                Label(window_insert, text="专业:").place(x=100, y=230)
                self.new_stu_id = tkinter.StringVar()  # 创建字符串变量
                en_new_id = Entry(window_insert, textvariable=self.new_stu_id)  # 创建输入框
                en_new_id.place(x=160, y=70)  # 设置输入框位置
                en_new_id.insert(10, item_text[2])  # 设置输入框的默认值
                self.new_name = tkinter.StringVar()
                en_use_name = Entry(window_insert, textvariable=self.new_name)
                en_use_name.place(x=160, y=110)
                en_use_name.insert(10, item_text[0])
                self.new_gender = tkinter.StringVar()
                en_new_sex = Entry(window_insert, textvariable=self.new_gender)
                en_new_sex.place(x=160, y=150)
                en_new_sex.insert(10, item_text[1])
                self.new_gpa = tkinter.StringVar()
                en_new_gpa = Entry(window_insert, textvariable=self.new_gpa)
                en_new_gpa.place(x=160, y=190)
                en_new_gpa.insert(10, item_text[3])
                self.new_major = tkinter.StringVar()
                en_major = Entry(window_insert, textvariable=self.new_major)
                en_major.place(x=160, y=230)
                en_major.insert(10, item_text[4])
                bt1 = Button(window_insert, text="修改", command=self.update_item, width=10, height=2)
                bt1.place(x=100, y=300)
                bt2 = Button(window_insert, text="取消", command=window_insert.destroy, width=10, height=2)
                bt2.place(x=300, y=300)

    def update_item(self):  # 修改学生信息的实现
        for item in self.tree.selection():  # 获取所选行的值
            item_text = self.tree.item(item, "values")  # 获取所选行的数据，用于查询
            print(f"item_text in update_database:{item_text}")
            new_stu_id = self.new_stu_id.get()  # 获取输入框的值
            new_name = self.new_name.get()
            new_gender = self.new_gender.get()
            new_major = self.new_major.get()
            new_gpa = self.new_gpa.get()
            try:
                print(f"new_stu_id:{new_stu_id}, new_name:{new_name}")
                search = "SELECT * FROM stu_info WHERE stu_id=%(n1)s AND name=%(n2)s"  # TODO: 编写查询语句，通过学号和姓名查询学生信息的id
                cursor.execute(search, {"n1": item_text[2], "n2": item_text[0]})
                result = cursor.fetchone()  # 获取查询结果：唯一的id构成的元组
                print(result)
                update = ('UPDATE stu_info SET name=%(n1)s, gender=%(n2)s, stu_id=%(n3)s, GPA=%(n4)s, major=%(n5)s WHERE id=%(n6)s')
                # TODO: 编写更新语句，通过id更新学生信息，更新的字段有：姓名、性别、学号、GPA、专业
                cursor.execute(update, {"n1": new_name, "n2": new_gender, "n3": new_stu_id,
                                        "n4": new_gpa, "n5": new_major, "n6": result[0]})
                conn.commit()
                tkinter.messagebox.showinfo(title="修改成功",
                                            message=f"修改学生{new_name}（编号{result[0]}）数据成功，请前往操作")
            except Exception:
                tkinter.messagebox.showerror("修改数据失败！")

    def search(self):  # 单条记录进行查询
        stu_id = self.stu_id.get()
        name = self.stu_name.get()
        stu_major = self.stu_major.get()
        if name == '' and stu_major == '' and stu_id == '':
            tkinter.messagebox.showinfo(title="提示", message="查询信息不能全为空！")
        else:
            try:
                sql = ("SELECT * FROM stu_info WHERE stu_id=%(n1)s OR name=%(n2)s OR major=%(n3)s")
                # TODO: 编写查询语句，通过学号、姓名、专业查询学生的全部信息（显然不含id）
                cursor.execute(sql, {"n1": stu_id, "n2": name, "n3": stu_major})  # 字典用法
                result = cursor.fetchall()  # 获取所有查询结果
                # print(result)  # 输出查询结果
                if result is None:  # 判断是否查询到结果
                    tkinter.messagebox.showinfo(title="提示", message="未查询到该学生")  # 未查询到则提示
                else:
                    all_items = self.tree.get_children()  # 获取表格中的所有数据
                    for item in all_items:
                        self.tree.delete(item)  # 删除表格中的所有数据
                    for res in result:  # 将查询结果显示在表格中
                        list = [res[0], res[1], res[2], res[3], res[4]]  # 将查询结果转换为列表
                        self.tree.insert('', 'end', values=list)  # 将列表插入表格中
            except Exception:
                tkinter.messagebox.showerror("搜索时数据查询异常！")

    def show(self):  # 查询所有信息
        try:
            sql = "SELECT name, gender, stu_id, GPA, major FROM stu_info"  # 查询学生的所有信息
            cursor.execute(sql)
            result = cursor.fetchall()  # 获取所有查询结果
            return result
        except Exception:
            tkinter.messagebox.showerror("查询异常！")

    def refresh(self):  # 刷新页面
        result = self.show()
        self.stu_major = StringVar()
        self.en_stu_major = Entry(self.window, textvariable=self.stu_major)
        self.en_stu_major.place(x=270, y=120, height=40)
        self.tree = ttk.Treeview(self.window, show="headings")
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree.place(x=200, y=180)
        self.tree.column('0', width=100, anchor='center')
        self.tree.column('1', width=100, anchor='center')
        self.tree.column('2', width=100, anchor='center')
        self.tree.column('3', width=100, anchor='center')
        self.tree.column('4', width=100, anchor='center')
        self.tree.heading('0', text='姓名')
        self.tree.heading('1', text='性别')
        self.tree.heading('2', text='学号')
        self.tree.heading('3', text='棘皮埃')
        self.tree.heading('4', text='专业')
        for res in result:
            list = [res[0], res[1], res[2], res[3], res[4]]
            self.tree.insert('', 'end', values=list)

    def exit(self):  # 退出系统
        conn.close()
        self.window.destroy()
