# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 16:48
# @Author  : Zeeland
# @File    : HomeController.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from views.home import Ui_MainWindow
import os
from service.covert2md import Covert2md

class HomeController(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 往空的QWidget里面放置UI内容
        self.setupUi(self)
        self.initAttr()
        self.initFun()

        # parameter init
        self.choose_file_path = ''
        self.covert_serivce = Covert2md()

    # 属性处理
    def initAttr(self):
        self.setWindowTitle("Yuque2md designed by Zeeland V1.0")

        # # 设置背景图片
        # palette = QtGui.QPalette()
        # palette.setBrush(QPalette.Background,QBrush(QPixmap(os.getcwd()+"\static\images\\bg1.jpg")))
        # self.setPalette(palette)

        # # 设置图表
        # self.setWindowIcon(QIcon(os.getcwd()+'\static\images\\tool.jpeg'))

    # 信号与槽绑定
    def initFun(self):
        # open file
        self.btn_chooseFile.clicked.connect(self.openFile)

        # covert data
        self.btn_covert.clicked.connect(self.covert)

    def openFile(self):
        print('[info] openfile')
        self.choose_file_path = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),"Markdown Files(*.md)")[0]
        print('[info] choose file : {}'.format(self.choose_file_path))
        self.covert_serivce.file_path = self.choose_file_path

        if self.covert_serivce.file_path is not '':
            self.textBrowser_before.setMarkdown(self.covert_serivce.get_original_text())


    def covert(self):
        print('begin to covert')
        self.covert_serivce.covert()
        self.textBrowser_after.setMarkdown(self.covert_serivce.get_after_text())
        QMessageBox.about(self, "提示", "转换成功")
