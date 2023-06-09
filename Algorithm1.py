
# import libraries

import time
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.ndimage import distance_transform_edt as edt

#read video stream from camera
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    
   if gpio.input(4) == 0: #if gpio pin is low, stop recording
        break
        
    #start frame timer
    start_time = time.time()
    #convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #add gaussian blur
    gray = cv2.GaussianBlur(gray,(13,13),0)
    
    #threshold to split blur
    ret,gray = cv2.threshold(gray,210,255,cv2.THRESH_BINARY)
    
    #convert to binary image
    binary=gray.copy()
    binary[binary <= 210.] = 0
    binary[binary > 210.] = 1

    #---contour detection---
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt1 = contours[0]
    cnt2 = contours[1]

    #define contours without using drawContours
    temp_img= np.zeros  ((frame.shape[0], frame.shape[1], 1), dtype=np.uint8)
    cv2.fillPoly(temp_img, pts =contours, color=(255))
   
    #polynomial fitting
    poly1 = np.polyfit(cnt1[:,0,0], cnt1[:,0,1], 2)
    poly2 = np.polyfit(cnt2[:,0,0], cnt2[:,0,1], 2)
    
    #overlay polynomial on frame
    x = np.linspace(0, frame.shape[1], 100)
    y1 = poly1[0]*x**2 + poly1[1]*x + poly1[2]
    y2 = poly2[0]*x**2 + poly2[1]*x + poly2[2]
    cv2.polylines(frame, [np.int32(np.vstack((x,y1)).T)], False, (0,0,255), 1)
    cv2.polylines(frame, [np.int32(np.vstack((x,y2)).T)], False, (0,255,0), 3)


    #---midline detection---

    #euclidean distance transform 
    dist_transform = scipy.ndimage.distance_transform_edt(binary)

    #dynamic thresholding
    temp_img2 = dist_transform.copy()
    temp_img2 = [[0 if val < 0.9*max(row) else val for val in row] for row in temp_img2]
    temp_img2 = np.array(temp_img2, dtype=np.uint8)
    temp_img2 = cv2.bitwise_not(frame)
    temp_img2 = cv2.bitwise_and(temp_img2, temp_img2, mask = temp_img)
    temp_img2 = cv2.bitwise_not(temp_img2)


    #draw current trajectory as a line from the bottom of the frame straight up 20px
    
    cv2.line(temp_img2, (int(x[0]), frame.shape[0]), (int(x[0]), frame.shape[0]-20), (255,255,255), 1)
    cv2.line(temp_img2, (int(x[-1]), frame.shape[0]), (int(x[-1]), frame.shape[0]-20), (255,255,255), 1)

    #add distance transform to frame
    temp_img2 = cv2.cvtColor(temp_img2, cv2.COLOR_BGR2GRAY)
    temp_img2 = cv2.bitwise_not(temp_img2)
    temp_img2 = cv2.bitwise_and(temp_img2, temp_img2, mask = temp_img)
    temp_img2 = cv2.bitwise_not(temp_img2)
    temp_img2 = cv2.cvtColor(temp_img2, cv2.COLOR_GRAY2BGR)
    temp_img2 = cv2.addWeighted(frame, 0.5, temp_img2, 0.5, 0)
    cv2.imshow('frame', temp_img2)
    # cv2.imshow('frame', frame) for debugging purposes
    
    #send direction instructions to arduino
    turning_value1 = np.arctan(poly1[1]) * 180 / np.pi
    turning_value2 = np.arctan(poly2[1]) * 180 / np.pi
    turning_value = int((turning_value1 + turning_value2) / 2)
    turning_value = int((turning_value + 90) * 255 / 180)
    turning_value = turning_value.to_bytes(1, byteorder='big')

    #convert turning value to wheel speed values
    #wheel speed values are sent to arduino as a byte array

    left_speed_value_1 = 255 - turning_value
    right_speed_value_2 = 255 + turning_value
    speed_value = speed_value.to_bytes(1, byteorder='big')

    #send speed values to arduino using pwm through the gpio pins
    left_speed_value_1 = left_speed_value_1.to_bytes(1, byteorder='big')
    right_speed_value_2 = right_speed_value_2.to_bytes(1, byteorder='big')
    
    #end time
    end_time = time.time()
    time_elapsed=start_time-end_time
    #record time into csv file
    with open('time.csv', 'a') as f:
        f.write(str(end_time - start_time) + '\n')
       

cap.release() #end video capture

