# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:06:28 2018

@author: Sunny
"""

from imutils.video import FPS
import numpy as np
import imutils
import cv2
import sys
from threading import Thread
if sys.version_info >= (3, 0):
    from queue import Queue
    
class FileVideoStream:
    def __init__(self, path, queueSize=256):
        print("Init")
        self.stream = cv2.VideoCapture(0)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)  
	
    def start(self):
		# start a thread to read frames from the file video stream
        print("Start")
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        print("Update")
        while True:
            if self.stopped:
                print("Stopped in update")
                return
            print("FULL QUEUE = "+ str(self.Q.full()))
            if not self.Q.full():
                (grabbed, frame) = self.stream.read()
                print(grabbed)
                if not grabbed:
                    self.stop()
                    return
                
            self.Q.put(frame)
            
    def read(self):
		# return next frame in the queue
        print("Read")
        return self.Q.get()
    
    def stop(self):
		# indicate that the thread should be stoppe
        print("stop")
        self.stopped = True
     
    def more(self):
		# return True if there are still frames in the queue
        print("More")
        return self.Q.qsize() > 0
