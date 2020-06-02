import tkinter as tk
from src.queryX.AnsForQ_v2 import mainSys

# 顶级窗口
topwindow = tk.Tk()
topwindow.title("Query Paper")
topwindow.geometry("570x500")


# 按钮状态全局变量
# on_hit = False

# 标签
# label = tk.Label(topwindow, textvariable=var, bg='green', font=('Arial', 12), width=15, height=2)
# label.pack()

# 嵌套框架
frm_qb = tk.Frame(topwindow)
frm_qb.pack()

# .place(x=10, y=100, anchor='nw')      north west 左上角

# 输入查询的文本框
entry = tk.Entry(frm_qb, width=60, show=None)
entry.pack(side='left')


# 点击按钮出发的事件
def search_b():
    # 输入的查询语句
    query = entry.get()

    # 返回的结果
    ans2query = mainSys(query)

    # 实现清空 从 第一行第0下标 到 end 清空 然后 插入结果
    text.delete('1.0', 'end')
    text.insert('insert', ans2query)


# 按钮
button = tk.Button(frm_qb, text="Search", width=10, height=1, command=search_b)
button.pack(side='right')

# 显示查询结果的文本框
text = tk.Text(topwindow, height=50)
text.pack()











# 进入消息循环
topwindow.mainloop()