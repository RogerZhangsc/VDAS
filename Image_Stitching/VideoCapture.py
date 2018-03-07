# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 16:02:03 2018

@author: Sunny
"""
import numpy as np
import cv2
import imutils
from imutils.video import FPS
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QAction
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QCheckBox
from PyQt5.QtWidgets import QProgressBar, QFormLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QCoreApplication,Qt,QTimer

class VideoCapture(QWidget):
    
    
    def __init__(self,parent):
        super(QWidget, self).__init__()
        self.cam = parent.cam
        self.fliphflags = parent.fliphlist
        self.flipvflags = parent.flipvlist
        self.video_frame = QLabel()
        self.FRAME_WIDTH = parent.CAM_WIDTH 
        self.FRAME_HEIGHT = parent.CAM_HEIGHT
        if(parent.i>1):
            self.RECORD_WIDTH = self.FRAME_WIDTH*(parent.i-1)
            self.interface_cam_count = parent.i-1
        else:
            self.RECORD_WIDTH = self.FRAME_WIDTH*3
            self.interface_cam_count = parent.i
        self.view_1 = parent.view_1
        self.view_2 = parent.view_2
        self.view_3 = parent.view_3
        
        self.RECORD_HEIGHT = self.FRAME_HEIGHT
        self.count=0
        self.flag_record = 0
        self.FPS = parent.FPS
        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        parent.layout.addWidget(self.video_frame)        

    def nextFrameSlot(self):
        
        no_of_cam = [self.view_1,self.view_2,self.view_3]
        final_frame = 0
        count=0
        if(self.vs=="G"):
            for x in no_of_cam:
                #print("Self.View_"+str(count)+" = "+str(x))
                if(count==0):
                    ret, frame = self.cam[x].read()
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
#==============================================================================
#                     if(self.fliphflags[x]==1):
#                         frame = cv2.flip(frame,1)

#                     if(self.flipvflags[x]==1):
#                         frame = cv2.flip(frame,0)    
#==============================================================================
                    final_frame = frame
                else:
                    ret, frame = self.cam[x].read()
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                    #frame = cv2.resize(frame,(self.FRAME_WIDTH, self.FRAME_HEIGHT),interpolation=cv2.INTER_CUBIC);
#==============================================================================
#                     if(self.fliphflags[x-1]==1):
#                         frame = cv2.flip(frame,1)
#                     if(self.flipvflags[x-1]==1):
#                         frame = cv2.flip(frame,0)  
#==============================================================================
                    final_frame = np.hstack((final_frame,frame))
                count+=1
           
        if(self.flag_record==1):
            self.out.write(final_frame)
            
        final_frame = cv2.resize(final_frame,(320*3, 240),interpolation=cv2.INTER_CUBIC);
        img = QImage(final_frame, final_frame.shape[1], final_frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
        self.count+=1
        self.fps.update()

        #if(self.count%90==0):
            #print(self.count)

    def start(self,view_style,view_1,view_2,view_3):
        self.timer = QTimer()
        self.view_1 = view_1
        self.view_2 = view_2
        self.view_3 = view_3
        
        self.fps = FPS().start()
        self.vs = view_style
        self.timer.timeout.connect(self.nextFrameSlot)      
        print(self.FPS)
        self.timer.start(1000.0/self.FPS)

    def pause(self):
        print(self.FPS)
        self.timer.stop()
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
 
        
    def start_record(self):
        print("Started recording")
        self.flag_record=1
        timestamp = datetime.datetime.now().strftime('%Y_%m_%d(%H %M %S)')
        file_name = 'C:\\Users\\Sunny\\Desktop\\TRAINING_VIDEOS\\'+ timestamp +'.avi'
        print(file_name)
        self.out = cv2.VideoWriter(file_name,self.fourcc, 15, (self.RECORD_WIDTH,self.RECORD_HEIGHT))

    
    def stop_record(self):
        print("Stopped recording")
        self.flag_record=0
        self.out.release()

    def deleteLater(self):
        self.cap.release()
        super(QWidget, self).deleteLater()


    def wide_angle_stitching(self):
        print("WORK IN PROGRESS")