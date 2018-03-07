# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 20:18:02 2018

@author: Sunny
"""

import numpy as np
import sys
import cv2

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QAction
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QCheckBox
from PyQt5.QtWidgets import QProgressBar, QFormLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QCoreApplication,Qt,QTimer

from VideoDisplayWidget import VideoDisplayWidget
from VideoCapture import VideoCapture


    
    
class Window(QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        #Initialize members
        self.cam = []
        self.frame = []
        self.ret = []
        self.rgb = []
        self.record_flag = True
        self.i = 0
        self.rgb_current=0
        
        #Create Window
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("PyQt5 Tutorial")
        self.setWindowIcon(QIcon("testImg.jpg"))
        
        #creating Record item
        recordAction = QAction("&Record", self)
        recordAction.setShortcut("Ctrl+R")
        recordAction.setStatusTip("Start Recording")
        
        #creating Record item
        extractAction = QAction("&Quit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Closing the App")
        extractAction.triggered.connect(self.cleanup)
        
        self.statusBar()
        
        #creating menu bar menus
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(recordAction)
        fileMenu.addAction(extractAction)
       
        #Enable Cameras
        self.videoDisplayWidget = VideoDisplayWidget(self)
        self.setCentralWidget(self.videoDisplayWidget)
            
        
    def cleanup(self):
        print("Check 3")
        k =  0
        while(k<self.i):
              self.videoDisplayWidget.cam[k].release()
              print("releasing camera - "+str(k+1))
              k=k+1   
        if(self.videoDisplayWidget.hasCapture==1):
            if(self.videoDisplayWidget.capture.flag_record==1):
                  print("Releasing Video Save")
                  self.videoDisplayWidget.capture.out.release()
        print("Destroying All Windows")
        #cv2.destroyAllWindows()
        self.close()

def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    app.exec_()


run()

