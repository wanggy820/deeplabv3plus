import sys

from PyQt5.QtWidgets import QApplication
from App import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = App()
    widget.resize(800, 600)#界面大小
    widget.move(100, 100)#位置
    widget.setWindowTitle("DeepLabV3+")
    widget.show()
    sys.exit(app.exec_())