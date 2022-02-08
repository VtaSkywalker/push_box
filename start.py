from PyQt5 import QtCore, QtWidgets
from mainform import MainWindow
import sys

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
