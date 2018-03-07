# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 16:00:36 2018

@author: Sunny
"""
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QAction
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QCheckBox
from PyQt5.QtWidgets import QProgressBar, QFormLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QCoreApplication,Qt,QTimer

from VideoCapture import VideoCapture

class VideoDisplayWidget(QWidget):
    def __init__(self,parent):
        super(VideoDisplayWidget, self).__init__(parent)
        self.hasCapture  = 0
        self.flag_paused = 0
        self.flag_record = 0
        ## HD RES- HEIGHT 720 WIDTH 1280
        ## FULL HD RES- HEIGHT 1080 WIDTH 1920
        ## VGA - HEIGHT 480 WIDTH 640
        self.CAM_HEIGHT = 480
        self.CAM_WIDTH = 640
        self.fliphlist = [0, 0, 0]
        self.flipvlist = [0, 0, 0]
        self.cam = []
        self.FPS = 60
        
        self.i=0
        try:
            while(cv2.VideoCapture(self.i).isOpened()):
                #self.cam[self.i-1].set(cv2.CV_CAP_PROP_SETTINGS, 0);
                self.cam.append(cv2.VideoCapture(self.i))
                self.cam[self.i].set(3,self.CAM_WIDTH)
                self.cam[self.i].set(4,self.CAM_HEIGHT)
                self.i=self.i+1
                print("camera -" +str(self.i) + " detected")
                print("Camera -" + str(self.i) + "Properties:")
                print(self.cam[self.i-1].get(3))
                print(self.cam[self.i-1].get(4))
        except Exception as e:
            print(e)
            print("All cameras detected.")
            
        if(self.i>1):    
            self.view_1=3
            self.view_2=2
            self.view_3=1
        else:
            self.view_1=0
            self.view_2=0
            self.view_3=0
        self.layout = QFormLayout(self)
        print("Pixmap created")
        self.label = QLabel()
        self.liveButton = QPushButton('Live', parent)
        self.liveButton.clicked.connect(self.start_live)
        self.liveButton.setFixedWidth(50)
        self.recordButton = QPushButton('Start Recording', parent)
        self.recordButton.setFixedWidth(100)
        self.pauseButton = QPushButton('Pause', parent)
        self.pauseButton.setFixedWidth(50)
        self.cam_view = QComboBox(self)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.liveButton)
        hbox.addWidget(self.recordButton)
        hbox.addWidget(self.pauseButton)
        hbox.addWidget(self.cam_view)
        self.layout.addRow(hbox)
        
        self.setLayout(self.layout)
        print("Layout Completed")
        self.cam_1_fliph = QCheckBox("FLIP CAM 1 Horz",self)
        self.cam_2_fliph = QCheckBox("FLIP CAM 2 Horz",self)
        self.cam_3_fliph = QCheckBox("FLIP CAM 3 Horz",self)
        
        self.cam_1_flipv = QCheckBox("FLIP CAM 1 Vert",self)
        self.cam_2_flipv = QCheckBox("FLIP CAM 2 Vert",self)
        self.cam_3_flipv = QCheckBox("FLIP CAM 3 Vert",self)
        
        hboxflip = QHBoxLayout()
        hboxflip.addWidget(self.cam_1_fliph)
        hboxflip.addWidget(self.cam_2_fliph)
        hboxflip.addWidget(self.cam_3_fliph)
        self.layout.addRow(hboxflip)
        
        vboxflip = QHBoxLayout()
        vboxflip.addWidget(self.cam_1_flipv)
        vboxflip.addWidget(self.cam_2_flipv)
        vboxflip.addWidget(self.cam_3_flipv)
        self.layout.addRow(vboxflip)
        
        self.cam_view_1 = QComboBox(self)
        self.cam_view_2 = QComboBox(self)
        self.cam_view_3 = QComboBox(self)
        count=0
        while(count<len(self.cam)):
            self.cam_view_1.addItem("CAM_"+str(count))
            self.cam_view_2.addItem("CAM_"+str(count))
            self.cam_view_3.addItem("CAM_"+str(count))
            count+=1
        
        box_cam = QHBoxLayout()
        box_cam.addWidget(self.cam_view_1)
        box_cam.addWidget(self.cam_view_2)
        box_cam.addWidget(self.cam_view_3)
        self.layout.addRow(box_cam)
        
        self.setLayout(self.layout)
        print("Layout Completed")
        
    
    def interface_view_1(self, text):
        if(text == "CAM_1"):
            self.view_1=1
        elif(text == "CAM_2"):
            self.view_1=2
            print("View Changed")
        elif(text == "CAM_3"):
            self.view_1=3
            print("View Changed") 
        elif(text == "CAM_0"):
            self.view_1=0
            print("View Changed") 
        self.capture.start("G",self.view_1,self.view_2,self.view_3)
    
    def interface_view_2(self, text):
        if(text == "CAM_1"):
            self.view_2=1
        elif(text == "CAM_2"):
            self.view_2=2
            print("View Changed")
        elif(text == "CAM_3"):
            self.view_2=3
            print("View Changed")
        elif(text == "CAM_0"):
            self.view_2=0
            print("View Changed") 
        self.capture.start("G",self.view_1,self.view_2,self.view_3)
    
    def interface_view_3(self, text):
        if(text == "CAM_1"):
            self.view_3=1
        elif(text == "CAM_2"):
            self.view_3=2
            print("View Changed")
        elif(text == "CAM_3"):
            self.view_3=3
            print("View Changed")
        elif(text == "CAM_0"):
            self.view_3=0
            print("View Changed") 
        self.capture.start("G",self.view_1,self.view_2,self.view_3)
            
    def change_live(self,text):
        self.capture.start("G",self.view_1,self.view_2,self.view_3)
            
    def start_live(self):
        self.hasCapture = 1
        self.capture = VideoCapture(self)
        self.pauseButton.clicked.connect(self.pause)
        self.recordButton.clicked.connect(self.record)
       
        self.cam_view_1.activated[str].connect(self.interface_view_1)
        self.cam_view_2.activated[str].connect(self.interface_view_2)
        self.cam_view_3.activated[str].connect(self.interface_view_3)

        self.cam_1_fliph.stateChanged.connect(self.fliph1)
        self.cam_2_fliph.stateChanged.connect(self.fliph2)
        self.cam_3_fliph.stateChanged.connect(self.fliph3)
        self.cam_1_flipv.stateChanged.connect(self.flipv1)
        self.cam_2_flipv.stateChanged.connect(self.flipv2)
        self.cam_3_flipv.stateChanged.connect(self.flipv3)
        #self.capture.start("G",self.view_1,self.view_2,self.view_3)
        self.change_live("G")
        
    def fliph1(self,state):
        if(self.fliphlist[0] == 0):
            self.fliphlist[0] = 1
        else:
            self.fliphlist[0] = 0
    def fliph2(self,state):
        if(self.fliphlist[1] == 0):
            self.fliphlist[1] = 1   
        else:
            self.fliphlist[1] = 0
    def fliph3(self,state):
        if(self.fliphlist[2] == 0):
            self.fliphlist[2] = 1
        else:
            self.fliphlist[2] = 0
       
    def flipv1(self,state):
        if(self.flipvlist[0] == 0):
            self.flipvlist[0] = 1
        else:
            self.flipvlist[0] = 0
    def flipv2(self,state):
        if(self.flipvlist[1] == 0):
            self.flipvlist[1] = 1
        else:
            self.flipvlist[1] = 0
    def flipv3(self,state):
        if(self.flipvlist[2] == 0):
            self.flipvlist[2] = 1
        else:
            self.flipvlist[2] = 0
            
    def record(self):
        if self.flag_record==0 :
            self.recordButton.setText("Stop Recording")
            self.capture.start_record()
            self.flag_record=1 
        else:
            self.recordButton.setText("Start Recording")
            self.capture.stop_record()
            self.flag_record=0 
            
    def pause(self):
        if(self.flag_paused == 0):
            self.pauseButton.setText("Unpause")
            self.pauseButton.setFixedWidth(80)
            self.capture.pause()
            self.flag_paused = 1
        else:
            self.pauseButton.setText("Pause")
            self.pauseButton.setFixedWidth(50)
            self.capture.start("G")
            self.flag_paused = 0
        
        
        
        
        