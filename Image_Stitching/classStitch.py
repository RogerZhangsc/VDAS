# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2


stitcher = cv2.createStitcher(False)
f1 = cv2.imread("img1.png")
f1 = cv2.cvtColor(f1,cv2.COLOR_BGRA2GRAY)

f2 = cv2.imread("img2.png")

f2 = cv2.cvtColor(f2,cv2.COLOR_BGRA2GRAY)

result = stitcher.stitch((f1,f2))

f3 = cv2.imread("img3.png")

f3= cv2.cvtColor(f3,cv2.COLOR_BGRA2GRAY)

cv2.imshow("Result", result[1])
cv2.imshow("f3", f3)

result2 = stitcher.stitch((result[1],f3))

print(result2)

cv2.imshow("Result_2", result2[1])
cv2.imwrite("result1.jpg", result2[1])