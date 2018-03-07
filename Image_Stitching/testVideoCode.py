# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:07:35 2018

@author: Sunny
"""

import numpy as np
import cv2

print(cv2.__version__)

TOTAL_CAMERAS=1
HEIGHT = 240
WIDTH = 320

RECORD_WIDTH = WIDTH*3
RECORD_HEIGHT = HEIGHT
FPS = 90
cam = []
frame = []
ret = []
rgb = []

i = 0
rgb_current=0
cam = cv2.VideoCapture(0)
#cam1 = cv2.VideoCapture(1)
#cam2 = cv2.VideoCapture(2)

cam.set(3,WIDTH)
cam.set(4,HEIGHT)
cam.set(cv2.CAP_PROP_FPS,FPS)


print(cam.get(3))
print(cam.get(4))
print(cam.get(5))
print(cam.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('C:\\Users\\Sunny\\Desktop\\saveOutput.avi',fourcc, FPS, (RECORD_WIDTH,RECORD_HEIGHT))
x=0
rgb_previous = 0
cv2.namedWindow("Live Feed")

flag_record=True

while(True):
    final_frame=0
    j = 0
    ret_current, frame_current = cam.read()
    # Our operations on the frame come here
    
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    rgb_current = cv2.cvtColor(frame_current, cv2.COLOR_RGBA2RGB)        
    rgb_current = cv2.resize(rgb_current,(WIDTH,HEIGHT),interpolation=cv2.INTER_CUBIC);
    horizontal_img = cv2.flip(rgb_current, 1 )

    # Display the resulting frame
    numpy_horizontal = np.hstack((horizontal_img, rgb_current, horizontal_img))
    numpy_vertical = np.vstack((numpy_horizontal,numpy_horizontal))
    
    if(flag_record == True ):
        out.write(numpy_horizontal)
    
    cv2.imshow("Live Feed",numpy_horizontal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('r'):
        if(flag_record==False):
            flag_record = True
        else:
            flag_record = False

cam.release()
if(flag_record==True):
    out.release()
cv2.destroyAllWindows()