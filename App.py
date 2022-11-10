from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QPushButton
import cv2


class App(QWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        # 从文件夹中选择图片
        self.showImage = None
        self.imagePath = None

        self.selectImageBtn = QPushButton("选择图片", self)
        self.selectImageBtn.setGeometry(100, 50, 200, 50)
        self.selectImageBtn.setStyleSheet("font-size:16px;color:red;")
        self.selectImageBtn.clicked.connect(self.selectImage);

        # 相机
        self.takePhotoBtn = QPushButton("打开摄像头", self)
        self.takePhotoBtn.setGeometry(500, 50, 200, 50)
        self.takePhotoBtn.setStyleSheet("font-size:16px;color:red;")
        self.takePhotoBtn.clicked.connect(self.takePhoto)

        self.leftWapper = QLabel(self);
        self.leftWapper.setFixedSize(350, 400)
        self.leftWapper.move(25, 150)
        self.leftWapper.setStyleSheet("QLabel{background:white;}")

        self.left = QLabel(self.leftWapper)
        self.left.setText("请选择图片")
        self.left.setAlignment(Qt.AlignCenter)
        self.left.setFixedSize(350, 400)
        self.left.move(0, 0)
        self.left.setScaledContents(True)
        self.left.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:12px;font-weight:bold;}")

        self.rightWapper = QLabel(self);
        self.rightWapper.setFixedSize(350, 400)
        self.rightWapper.move(425, 150)
        self.rightWapper.setStyleSheet("QLabel{background:white;}")

        self.deepLabel = QLabel(self.rightWapper)
        self.deepLabel.setText("处理后的图片")
        self.deepLabel.setAlignment(Qt.AlignCenter)
        self.deepLabel.setFixedSize(350, 400)
        self.deepLabel.move(0, 0)
        self.deepLabel.setScaledContents(True)
        self.deepLabel.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:12px;font-weight:bold;}")

        self.cap = cv2.VideoCapture()  # 初始化摄像头

        # 定时器让其定时读取显示图片
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.show_image)

        self.cameraIsOpen = False;

    '''从本地选择图片进行语义分割'''
    def selectImage(self):
        self.imagePath, filetype = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        print("select image:", self.imagePath, filetype)
        image = QtGui.QPixmap(self.imagePath)
        if image.width() == 0 or image.height() == 0:
            return

        height = self.left.width() * image.height() / image.width()
        self.left.setFixedHeight(height)
        self.left.setPixmap(image)
        self.left.move(0, (self.leftWapper.height() - height) / 2)

        # 分析图片
        imagePath = self.analysisImage()
        self.showAnalysisedImage(imagePath)
    '''使用相机拍照进行语义分割'''
    def takePhoto(self):
        if self.cameraIsOpen:
            self.cameraIsOpen = False
            if self.cap.isOpened():
                self.left.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                self.imagePath = "./images/picture_1.jpg"
                self.showImage.save(self.imagePath, "JPG", 100)

                '''关闭摄像头'''
                self.camera_timer.stop()  # 停止读取
                self.cap.release()  # 释放摄像头
                self.takePhotoBtn.setText("打开摄像头")

                # 分析图片
                imagePath = self.analysisImage()
                self.showAnalysisedImage(imagePath)
            else:
                QMessageBox.critical(self, '错误', '摄像头未打开！')
                return None
        else:
            self.takePhotoBtn.setText("拍照")
            self.cameraIsOpen = True
            print("take photo")

            height = self.left.width() * 720 / 1280
            self.left.setFixedHeight(height)
            self.left.move(0, (self.leftWapper.height() - height) / 2)

            self.cap = cv2.VideoCapture(0)  # 摄像头
            self.camera_timer.start(40)  # 每40毫秒读取一次，即刷新率为25帧
            self.show_image()

    '''显示图片'''
    def show_image(self):
        flag, self.image = self.cap.read()  # 从视频流中读取图片
        image_show = cv2.resize(self.image, (1280, 720))  # 把读到的帧的大小重新设置为 600*360
        # image_show = self.image
        width, height = image_show.shape[:2]  # 行:宽，列:高
        image_show = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)  # opencv读的通道是BGR,要转成RGB
        image_show = cv2.flip(image_show, 1)  # 水平翻转，因为摄像头拍的是镜像的。
        # 把读取到的视频数据变成QImage形式(图片数据、高、宽、RGB颜色空间，三个通道各有2**8=256种颜色)
        self.showImage = QtGui.QImage(image_show.data, height, width, QImage.Format_RGB888)
        self.left.setPixmap(QtGui.QPixmap.fromImage(self.showImage))  # 往显示视频的Label里显示QImage

        #如果需要分析视频流，则打开
        # self.imagePath = "./images/picture_1.jpg"
        # self.showImage.save(self.imagePath, "JPG", 100)
        # # 分析图片
        # imagePath = self.analysisImage()
        # self.showAnalysisedImage(imagePath)

    '''分析图片 ---  调用deeplabv3+进行语义分割'''
    def analysisImage(self):
        print("被分析的图片地址：", self.imagePath)
        print("调用deeplabv3+进行语义分割")
        return self.imagePath

    def showAnalysisedImage(self, imagePath):
        print("分析生成的图片地址：",imagePath)
        image = QtGui.QPixmap(imagePath)
        if image.width() == 0 or image.height() == 0:
            return

        height = self.deepLabel.width() * image.height() / image.width()
        self.deepLabel.setFixedHeight(height)
        self.deepLabel.setPixmap(image)
        self.deepLabel.move(0, (self.leftWapper.height() - height) / 2)