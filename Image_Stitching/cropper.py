# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 00:37:05 2018

@author: Sunny
"""
import cv2
import numpy as np
import os
from os.path import abspath

FPS = 30

OUTPUT_FRAME_WIDTH = 0 #SHOULD REMAIN SAME AS INPUT
OUTPUT_FRAME_HEIGHT = 0 #SHOULD BE 2x INPUT
MULTI_STITCH = 0 #OFF

##STEP 1 - Read EACH FRAME FROM VIDEO IN PATH FOLDER
path = 'testing/'
output_path = "C:\\Users\\Sunny\\Desktop\\VDAS\\StitchedVideos"

videoList = os.listdir(path) 
numberOfVideos = len(videoList)
i = 0
print('Check1')
while(i<numberOfVideos):
    input_path = path+'\\'+videoList[i]
    output_path_video=path+"\\"+videoList[i]+"_cropped.avi"
    videoCapture = cv2.VideoCapture(input_path)
    i+=1
    fps = videoCapture.get(5)
    frame_size = ((int(videoCapture.get(3)/3)),
            int(videoCapture.get(4)))
   
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
       
    videoWriter = cv2.VideoWriter(output_path_video, 
                                  fourcc,
                                  fps, 
                                  frame_size)
    
    success, frame = videoCapture.read()
    success, frame = videoCapture.read()
    
    print(success)
    
    count=0
    while success: 
        frame_1 = frame[0:frame_size[1], 0:frame_size[0]]
        frame_2 = frame[0:frame_size[1], frame_size[0]:frame_size[0]*2]
        frame_3 = frame[0:frame_size[1], frame_size[0]*2:frame_size[0]*3]
            
        videoWriter.write(frame_2)
        if(count%30==0):
            print("Footage Duration:",count)
        success, frame = videoCapture.read()
        count+=1

print("FINISHED")