'''
Created on Jan 31, 2018
@author: Preetham
'''

import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
from numpy.linalg import inv

def get_sift(a,b):
    #intitate shift detector
    sift =  cv2.xfeatures2d.SIFT_create()

    #find keypoints and descriptors
    kps1, des1 = sift.detectAndCompute(a, None)
    kps2, des2 = sift.detectAndCompute(b, None)

    # Brute force to matcher for keypints
    FLANN_INDEX_KDTREE = 0
    bf = cv2.BFMatcher()
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)
    #flann = cv2.FlannBasedMatcher(index_params,search_params)
    raw_matches = bf.knnMatch(des1, des2, k=2)
    #raw_matches_flann = flann.knnMatch(des1,des2, k=2)
    
    good_matches = []
    good=[]
    for m,n in raw_matches:
        if m.distance < 0.8*n.distance: #Lowe's ratio
            good_matches.append(( m.trainIdx, m.queryIdx))
            good.append([m])
    img3 = cv2.drawMatchesKnn(a,kps1,b,kps2,good,None,flags=2)
    plt.imshow(img3)
    plt.show()
    
    if len(good_matches) > 4: #Set Minimum number of matches
        kpsA = np.float32([kps1[i].pt for (_, i) in good_matches])
        kpsB = np.float32([kps2[i].pt for (i, _) in good_matches])
        H, status = cv2.findHomography(kpsB, kpsA, cv2.RANSAC)
        print(H)
        return H
        print('Error: Not enough matches')
        exit()

def stitch_left_based(a, b, H):
    #imag warping
    warp = cv2.warpPerspective(b, H, (300+a.shape[1]+b.shape[1] , 300+b.shape[0]))
    warp[0:b.shape[0], 0:b.shape[1]] = a
    rows, cols = np.where(warp[:,:,0] !=0)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    final = warp[min_row:max_row,min_col:max_col,:]
    return final


def stitch_left_based_gray(a, b, H):
    #imag warping
    warp = cv2.warpPerspective(b, H, (a.shape[1]+b.shape[1] ,b.shape[0]))
    print(warp.shape[0])
    print(warp.shape[1])
    warp[0:a.shape[0], 0:a.shape[1]] = a
    print(2)
    rows, cols = np.where(warp !=0)
    print(3)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    final = warp[min_row:max_row,min_col:max_col]
    #cv2.imshow("Final",final)
    return final

def main():
    #enter image to e stitched
    try:
        a = cv2.imread('1.png')
        b = cv2.imread('2.png')
        #a = cv2.imread('spa.png')
        #b = cv2.imread('spb.png')
        c = cv2.imread('3.png')
        a = cv2.cvtColor(a,cv2.COLOR_BGRA2GRAY)
        a = cv2.equalizeHist(a)
        b = cv2.cvtColor(b,cv2.COLOR_BGRA2GRAY)
        b = cv2.equalizeHist(b)
        c = cv2.cvtColor(c,cv2.COLOR_BGRA2GRAY)
        c = cv2.equalizeHist(c)
        print(a)
        a = cv2.resize(a,(640,480),interpolation=cv2.INTER_CUBIC)
        b = cv2.resize(b,(640,480),interpolation=cv2.INTER_CUBIC)
        c = cv2.resize(c,(640,480),interpolation=cv2.INTER_CUBIC)

        a = cv2.flip(a,1)
        b = cv2.flip(b,1)
        M =  get_sift(b, a)
        print("1")
        result_image = stitch_left_based_gray(b,a, M)
#==============================================================================
#         result_image = cv2.resize(result_image,(640,480),interpolation=cv2.INTER_CUBIC)
#==============================================================================
        print("4")
        result_image = cv2.flip(result_image,1)
        cv2.imshow("Result",result_image)
        
#==============================================================================
#         b = cv2.flip(b,1)
#         M =  get_sift(b[], c)
#         result_image_2 = stitch_left_based_gray(b,c, M)
#         #result_image_2 = cv2.resize(result_image_2,(640,480),interpolation=cv2.INTER_CUBIC)
#         cv2.imshow("Result 2",result_image_2)
#==============================================================================

        print("5")
        M = get_sift(result_image,c)
        print(6)ll
        result_image = stitch_left_based_gray(result_image,c, M)
        
#==============================================================================
#         cv2.imshow('A',a)
#         cv2.imshow('B',b)
#         cv2.imshow('C',c)
#==============================================================================
        print("7")
        
        result_image = cv2.equalizeHist(result_image)
        #result_image[0:480,0:640] = result_image[(result_image[0:480,0:640]>0)]-10
        cv2.imshow('matches',result_image)
        #cv2.imshow('matches2',result_image_2)
        cv2.waitKey()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
    
