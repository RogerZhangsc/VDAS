# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 00:37:05 2018

@author: Sunny
"""
import cv2
import numpy as np
import os
from os.path import abspath
from matplotlib import pyplot as plt
from time import sleep

FPS = 30

OUTPUT_FRAME_WIDTH = 0 #SHOULD REMAIN SAME AS INPUT
OUTPUT_FRAME_HEIGHT = 0 #SHOULD BE 2x INPUT
MULTI_STITCH = 0 #OFF

def get_sift(a,b):
    #intitate shift detector
    sift =  cv2.xfeatures2d.SIFT_create()

    #find keypoints and descriptors
    kps1, des1 = sift.detectAndCompute(a, None)
    kps2, des2 = sift.detectAndCompute(b, None)

    # Brute force to matcher for keypints
    FLANN_INDEX_KDTREE = 0
    bf = cv2.BFMatcher()
    raw_matches = bf.knnMatch(des1, des2, k=2)
    
    good_matches = []
    good = []
    for m,n in raw_matches:
        if m.distance < 0.85*n.distance: #Lowe's ratio
            good_matches.append(( m.trainIdx, m.queryIdx))
            good.append([m])
    img3 = cv2.drawMatchesKnn(a,kps1,b,kps2,good,None,flags=2)
#==============================================================================
#     plt.imshow(img3)
#     plt.show()
#     
#==============================================================================
    if len(good_matches) > 4: #Set Minimum number of matches
        kpsA = np.float32([kps1[i].pt for (_, i) in good_matches])
        kpsB = np.float32([kps2[i].pt for (i, _) in good_matches])
        H, status = cv2.findHomography(kpsB, kpsA, cv2.RANSAC)
        return H
    print('Error: Not enough matches')  
    exit()
        
def get_surf(a,b):
    #intitate shift detector
    sift =  cv2.xfeatures2d.SURF_create()

    #find keypoints and descriptors
    kps1, des1 = sift.detectAndCompute(a, None)
    kps2, des2 = sift.detectAndCompute(b, None)

    # Brute force to matcher for keypints
    bf = cv2.BFMatcher()
    raw_matches = bf.knnMatch(des1, des2, k=2)
    
    good_matches = []
    
    for m,n in raw_matches:
        if m.distance < 0.85*n.distance: #Lowe's ratio
            good_matches.append(( m.trainIdx, m.queryIdx))
    if len(good_matches) > 4: #Set Minimum number of matches
        kpsA = np.float32([kps1[i].pt for (_, i) in good_matches])
        kpsB = np.float32([kps2[i].pt for (i, _) in good_matches])
        H, status = cv2.findHomography(kpsB, kpsA, cv2.RANSAC)
        return H
        print('Error: Not enough matches')
        
        exit()
        
def get_sift_flann(a,b):
    #intitate shift detector
    sift =  cv2.xfeatures2d.SIFT_create()

    #find keypoints and descriptors
    kps1, des1 = sift.detectAndCompute(a, None)
    kps2, des2 = sift.detectAndCompute(b, None)

    # Brute force to matcher for keypints
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=30)
    
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    
    raw_matches = flann.knnMatch(des1,des2, k=2)
    
    good_matches = []
    
    for m,n in raw_matches:
        if m.distance < 0.85*n.distance: #Lowe's ratio
            good_matches.append(( m.trainIdx, m.queryIdx))
    if len(good_matches) > 4: #Set Minimum number of matches
        kpsA = np.float32([kps1[i].pt for (_, i) in good_matches])
        kpsB = np.float32([kps2[i].pt for (i, _) in good_matches])
        H, status = cv2.findHomography(kpsB, kpsA, cv2.RANSAC)
        return H
        print('Error: Not enough matches')
        
        exit()
        
def get_surf_flann(a,b):
    #intitate shift detector
    sift =  cv2.xfeatures2d.SURF_create()

    #find keypoints and descriptors
    kps1, des1 = sift.detectAndCompute(a, None)
    kps2, des2 = sift.detectAndCompute(b, None)

    # Brute force to matcher for keypints
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=30)
    
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    
    raw_matches = flann.knnMatch(des1,des2, k=2)
    
    good_matches = []
    
    for m,n in raw_matches:
        if m.distance < 0.85*n.distance: #Lowe's ratio
            good_matches.append(( m.trainIdx, m.queryIdx))
    if len(good_matches) > 4: #Set Minimum number of matches
        kpsA = np.float32([kps1[i].pt for (_, i) in good_matches])
        kpsB = np.float32([kps2[i].pt for (i, _) in good_matches])
        H, status = cv2.findHomography(kpsB, kpsA, cv2.RANSAC)
        return H
        print('Error: Not enough matches')
        
        exit()

def stitch_left_based(a, b, H):
    #image warping
    warp = cv2.warpPerspective(b, H, (a.shape[1]+b.shape[1] , b.shape[0]))
    warp[0:a.shape[0], 0:a.shape[1]] = a
    rows, cols = np.where(warp[:,:,0] !=0)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    final = warp[min_row:max_row,min_col:max_col,:]
    return final

def stitch_left_based_gray(a, b, H):
    #imag warping
    warp = cv2.warpPerspective(b, H, (a.shape[1]+b.shape[1] ,b.shape[0]))
    warp[0:a.shape[0], 0:a.shape[1]] = a
    rows, cols = np.where(warp !=0)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    final = warp[min_row:max_row,min_col:max_col]
    return final

frame_exception = []

##STEP 1 - Read EACH FRAME FROM VIDEO IN PATH FOLDER
try:
    path = 'C:\\Users\\Sunny\\Desktop\\VDAS\\TrainingData\\Combined Video'
    output_path = "C:\\Users\\Sunny\\Desktop\\VDAS\\StitchedVideos"
    videoList = os.listdir(path) 
    numberOfVideos = len(videoList)
    i = 0
    print('Check1')
    while(i<numberOfVideos):
        input_path = path+'\\'+videoList[i]
        output_path_video=output_path+"\\"+videoList[i]+"_stitched_comparison.avi"
        videoCapture = cv2.VideoCapture(input_path)
        i+=1
        fps = videoCapture.get(5)
        frame_size = ((int(videoCapture.get(3)/3)),
                int(videoCapture.get(4)))
        if(MULTI_STITCH==0):
            size = ((int(videoCapture.get(3)/3)),
                    int(videoCapture.get(4)))
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        else:
            size = ((int(videoCapture.get(3)/3)*2),
                    int(videoCapture.get(4))*2)
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            
        videoWriter = cv2.VideoWriter(output_path_video, 
                                      fourcc,
                                      10, 
                                      size)
        
        success, frame = videoCapture.read()
        success, frame = videoCapture.read()
#==============================================================================
#         while(i<1200):
#             success, frame = videoCapture.read()
#             i+=1
#==============================================================================
        print(success)
        count=0
        while success: 
            frame_exception = frame
            frame_1 = frame[0:frame_size[1], 0:frame_size[0]]
            frame_2 = frame[0:frame_size[1], frame_size[0]:frame_size[0]*2]
            frame_3 = frame[0:frame_size[1], frame_size[0]*2:frame_size[0]*3]
            frame_1 = cv2.cvtColor(frame_1,cv2.COLOR_BGRA2GRAY)
            #frame_1 = cv2.equalizeHist(frame_1)
            frame_2 = cv2.cvtColor(frame_2,cv2.COLOR_BGRA2GRAY)
            #frame_2 = cv2.equalizeHist(frame_2)
            frame_3 = cv2.cvtColor(frame_3,cv2.COLOR_BGRA2GRAY)
            #frame_3 = cv2.equalizeHist(frame_3)
            
            
            frame_1 = cv2.flip(frame_1,1)
            frame_2 = cv2.flip(frame_2,1)
            
            if(MULTI_STITCH!=0):
                M =  get_sift(frame_2,frame_1)
                result_image_1 = stitch_left_based_gray(frame_2,frame_1, M)
                result_image_1 = cv2.resize(result_image_1,frame_size,interpolation=cv2.INTER_CUBIC)
                result_image_1 = cv2.flip(result_image_1,1)
        
                frame_2 = cv2.flip(frame_2,1)
    
                M = get_sift(frame_2,frame_3)
                result_image_2 = stitch_left_based_gray(frame_2,frame_3, M)
                result_image_2 = cv2.resize(result_image_2,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                M = get_sift(result_image_1,result_image_2)
                result_image_1 = stitch_left_based_gray(result_image_1,result_image_2, M)
                result_image_1 = cv2.resize(result_image_1,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                cv2.putText(result_image_1,"SIFT BF", 
                             (10,10), 
                             cv2.FONT_HERSHEY_SIMPLEX, 
                             0.5,
                             (0,0,255),
                             2)
    
                frame_2 = cv2.flip(frame_2,1)
                
                M =  get_sift_flann(frame_2,frame_1)
                result_image_2 = stitch_left_based_gray(frame_2,frame_1, M)
                result_image_2 = cv2.resize(result_image_2,frame_size,interpolation=cv2.INTER_CUBIC)
                result_image_2 = cv2.flip(result_image_2,1)
        
                frame_2 = cv2.flip(frame_2,1)
    
                M = get_sift_flann(frame_2,frame_3)
                result_image_3 = stitch_left_based_gray(frame_2,frame_3, M)
                result_image_3 = cv2.resize(result_image_3,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                M = get_sift_flann(result_image_2,result_image_3)
                result_image_2 = stitch_left_based_gray(result_image_2,result_image_3, M)
                result_image_2 = cv2.resize(result_image_2,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                cv2.putText(result_image_2,"SIFT FLANN", 
                             (10,10), 
                             cv2.FONT_HERSHEY_SIMPLEX, 
                             0.5,
                             (0,0,255),
                             2)
    
                frame_2 = cv2.flip(frame_2,1)
                
                M =  get_surf(frame_2,frame_1)
                result_image_3 = stitch_left_based_gray(frame_2,frame_1, M)
                result_image_3 = cv2.resize(result_image_3,frame_size,interpolation=cv2.INTER_CUBIC)
                result_image_3 = cv2.flip(result_image_3,1)
        
                frame_2 = cv2.flip(frame_2,1)
    
                M = get_surf(frame_2,frame_3)
                result_image_4 = stitch_left_based_gray(frame_2,frame_3, M)
                result_image_4 = cv2.resize(result_image_4,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                M = get_surf(result_image_3,result_image_4)
                result_image_3 = stitch_left_based_gray(result_image_3,result_image_4, M)
                result_image_3 = cv2.resize(result_image_3,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                cv2.putText(result_image_3,"SURF BF", 
                             (10,10), 
                             cv2.FONT_HERSHEY_SIMPLEX, 
                             0.5,
                             (0,0,255),
                             2)
            
                frame_2 = cv2.flip(frame_2,1)
                
                M =  get_surf_flann(frame_2,frame_1)
                result_image_4 = stitch_left_based_gray(frame_2,frame_1, M)
                result_image_4 = cv2.resize(result_image_4,frame_size,interpolation=cv2.INTER_CUBIC)
                result_image_4 = cv2.flip(result_image_4,1)
               
                frame_2 = cv2.flip(frame_2,1)
     
                M = get_surf_flann(frame_2,frame_3)
                result_image_5 = stitch_left_based_gray(frame_2,frame_3, M)
                result_image_5 = cv2.resize(result_image_5,frame_size,interpolation=cv2.INTER_CUBIC)   
    
                M = get_surf_flann(result_image_4,result_image_5)
                result_image_4 = stitch_left_based_gray(result_image_4,result_image_5, M)
                result_image_4 = cv2.resize(result_image_4,frame_size,interpolation=cv2.INTER_CUBIC)   
                
                cv2.putText(result_image_4,"SURF FLANN", 
                             (10,10), 
                             cv2.FONT_HERSHEY_SIMPLEX, 
                             0.5,
                             (0,0,255),
                             2)
                
                result_image = np.vstack((np.hstack((result_image_1,result_image_2)),np.hstack((result_image_3,result_image_4))))
                
            else:
                
                M =  get_sift(frame_2,frame_1)
                result_image = stitch_left_based_gray(frame_2,frame_1, M)
                result_image = cv2.resize(result_image,frame_size,interpolation=cv2.INTER_CUBIC)
                result_image = cv2.flip(result_image,1)
                frame_2 = cv2.flip(frame_2,1)
    
                M = get_sift(frame_2,frame_3)
                result_image_2 = stitch_left_based_gray(frame_2,frame_3, M)
                result_image_2 = cv2.resize(result_image_2,frame_size,interpolation=cv2.INTER_CUBIC)    
                
                M = get_sift(result_image,frame_3)
                result_image = stitch_left_based_gray(result_image,result_image_2, M)
                result_image = cv2.resize(result_image,frame_size,interpolation=cv2.INTER_CUBIC)    
                
#==============================================================================
#                 
#                 cv2.putText(result_image,"SIFT BF", 
#                              (10,10), 
#                              cv2.FONT_HERSHEY_SIMPLEX, 
#                              0.5,
#                              (0,0,255),
#                              2)
#==============================================================================
               
#==============================================================================
#             if(count%30==0 and count!=0):
#                 break
#                 print("Footage Duration:",count)
#==============================================================================
            result_image = cv2.cvtColor(result_image,cv2.COLOR_GRAY2BGR)
            videoWriter.write(result_image)
            print("Frame Written")
            success, frame = videoCapture.read()
            count+=1
        if(count%30==0):
            break
            print("Footage Duration:",count)
            
        i+=1

except Exception as e:
    print(e)
    cv2.imshow("Frame",frame_exception)
    cv2.imshow("Frame1",frame_1)
    cv2.imshow("Frame2",frame_2)
    cv2.imshow("Frame3",frame_3)
    
    M =  get_sift(frame_2,frame_1)
    print("M ==",M)
    result_image = stitch_left_based_gray(frame_2,frame_1, M)
    result_image = cv2.resize(result_image,frame_size,interpolation=cv2.INTER_CUBIC)
    result_image = cv2.flip(result_image,1)
    cv2.imshow("Result_image_1",result_image)
    
    frame_2 = cv2.flip(frame_2,1)

    M = get_sift(frame_2,frame_3)
    result_image_2 = stitch_left_based_gray(frame_2,frame_3, M)
    result_image_2 = cv2.resize(result_image_2,frame_size,interpolation=cv2.INTER_CUBIC)    
    cv2.imshow("Result_image_2",result_image_2)

    M = get_sift(result_image,frame_3)
    result_image = stitch_left_based_gray(result_image,result_image_2, M)
    result_image = cv2.resize(result_image,frame_size,interpolation=cv2.INTER_CUBIC)    

videoWriter.release()
videoCapture.release()
print("FINISHED")