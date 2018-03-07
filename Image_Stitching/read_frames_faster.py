# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:07:07 2018

@author: Sunny
"""

# import the necessary packages
from FileVideoStream import FileVideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
 
print("[INFO] starting video file thread...")
fvs = FileVideoStream(0).start()
time.sleep(3.0)
 
# start the FPS timer
fps = FPS().start()

# loop over frames from the video file stream
while fvs.more():
    print("In Loop")
    frame = fvs.read()
    #frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])
    
    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)	
    cv2.imshow("Frame", frame)
    time.sleep(0.01)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Break")
        break
    fps.update()
    print("End of Loop")
    
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
fvs.stream.release()
cv2.destroyAllWindows()
fvs.stop()