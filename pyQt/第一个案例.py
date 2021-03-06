# 利用本案例感受 pySide2 的具体示例，看看他具体能做什么

# 配置环境变量，手动配置似乎不行···
# import os
# import PySide2
# dirname = os.path.dirname(PySide2.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# print(plugin_path)
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

# 主程序
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QMessageBox

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 300)
        self.window.setWindowTitle('量子芯片设计')

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("请输入Qubit类型")
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 350)

        self.button = QPushButton('提交', self.window)
        self.button.move(380, 80)

        self.button.clicked.connect(self.handleCalc)


    def handleCalc(self):
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
            name,salary,age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.window,
                    '统计结果',
                    f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                    )
if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.window.show()
    app.exec_()