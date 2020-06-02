from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
import sys,os
import PySide2

# 以下三行 不写的话 会报错
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


# 一个界面一个类   类的构造函数里面 加控件 并 绑定控件属性   方法里写处理响应的函数
class Stats():
    def __init__(self):
        # 主窗口
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 300)
        self.window.setWindowTitle('薪资统计')
        # 纯文本框
        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("请输入薪资表")
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 350)
        # 按钮
        self.button = QPushButton('统计', self.window)
        self.button.move(380, 80)
        # 按钮绑定响应函数
        self.button.clicked.connect(self.handleCalc)

    def handleCalc(self):
        # 获取纯文本框里的内容
        info = self.textEdit.toPlainText()

        # 薪资20000 以上 和 以下 的人员名单
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.window, '统计结果',
                    f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}''')


if __name__ =='__main__':
    # 整个图形界面程序的底层管理
    app = QApplication([])
    # 调用 实例的主窗口 show
    stats = Stats()
    stats.window.show()
    # GUI死循环
    app.exec_()