import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QFileDialog, QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class App(QWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        #从文件夹中选择图片
        selectImageBtn = QPushButton("选择图片", self)
        selectImageBtn.setGeometry(100, 50, 200, 50)
        selectImageBtn.setStyleSheet("font-family:'宋体';font-size:14px;color:red;")
        selectImageBtn.clicked.connect(self.selectImage);

        #相机
        takePhotoBtn = QPushButton("相机", self)
        takePhotoBtn.setGeometry(500, 50, 200, 50)
        takePhotoBtn.setStyleSheet("font-family:'宋体';font-size:14px;color:red;")
        selectImageBtn.clicked.connect(self.takePhoto);

        self.label = QLabel(self)
        self.label.setText("请选择图片")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(350, 400)
        self.label.move(25, 150)
        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(0,0,0,255);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        self.deepLabel = QLabel(self)
        self.deepLabel.setText("处理后的图片")
        self.deepLabel.setAlignment(Qt.AlignCenter)
        self.deepLabel.setFixedSize(350, 400)
        self.deepLabel.move(425, 150)
        self.deepLabel.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(0,0,0,255);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

    def selectImage(self):
        print("selct image")
        imgName, filetype = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        print(imgName, filetype)
        jpg = QtGui.QPixmap(imgName)
        self.label.setPixmap(jpg)


    def takePhoto(self):
        print("take photo")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = App()
    widget.resize(800, 600)#界面大小
    widget.move(0, 0)#位置
    widget.setWindowTitle("DeepLabV3+")
    widget.show()

    btn = QPushButton("按键1", widget)




    sys.exit(app.exec_())