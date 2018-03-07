# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:56:30 2018

@author: Sunny
"""
import subprocess
import os
import cv2
from os.path import abspath

def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename],
                            stdout = subprocess.PIPE, 
                            stderr = subprocess.STDOUT)
  return [x for x in result.stdout.readlines() if "Duration" in x]

path = 'C:\\Users\\Sunny\\Desktop\\VDAS\\Numbered Videos'
f_path = abspath("01.avi")
videoList = os.listdir(path) 
numberOfVideos = len(videoList)
i = 0
while(i<numberOfVideos):
    print(videoList[i])
    videoCapture = cv2.VideoCapture(videoList[i])
    i+=1