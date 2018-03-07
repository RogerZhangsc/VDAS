# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 15:53:10 2018

@author: Sunny
"""

import cv2

videoCapture = cv2.VideoCapture('06.avi')

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            
success, frame = videoCapture.read()

videoWriter = cv2.VideoWriter('06_grayed.avi', 
                                      fourcc,
                                      30, 
                                      (frame.shape[1],frame.shape[0]))
print(success)
count = 0
while(success):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    videoWriter.write(frame)
    success, frame = videoCapture.read()    
    print(success)
    count+=1
    print(count)
    
videoCapture.release()
videoWriter.release()