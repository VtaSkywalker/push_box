from PyQt5 import QtWidgets, uic
from display import Display

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./mainwindow.ui")
        self.ui.show()
        # 初始化spinbox的值与最大值
        max_unlock_level = 1
        self.ui.spinBox.setMaximum(max_unlock_level)
        self.ui.spinBox.setValue(max_unlock_level)
        # 按钮关联动作
        self.ui.pushButton.clicked.connect(self.start_level)

    def start_level(self):
        d = Display()
        d.load_level(self.ui.spinBox.value())
