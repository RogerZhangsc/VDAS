# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 15:08:54 2018

@author: Sunny
"""

import cv2

dev = 0


while(dev<10):
        try:
            cam = cv2.VideoCapture(dev)
            ret,frame = cam.read()
            print(cam.isOpened())
            print(type(ret))
            print(type(frame))
            print(dev)
            dev=dev+1
        except Exception as e:
            print(e)
            dev=dev+1
        