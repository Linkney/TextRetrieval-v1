from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        qfile_query = QFile("../ui/query.ui")
        qfile_query.open(QFile.ReadOnly)
        qfile_query.close()

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_query)

        self.ui.searchPushButton.clicked.connect(self.handleCalc)

    def handleCalc(self):
        info = self.ui.queryLineEdit.text()
        QMessageBox.about(self.ui, 'info:', info)


if __name__ == "__main__":
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()