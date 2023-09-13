import stage2_functions as sf
import cv2
import sys
import numpy as np

delay = 1
center_x = 0
center_y = 0
resolution = 5

def stage2():
    #start when fn is called
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit()
    while True:
        ret, frame = cap.read()
        if ret:
            height, width, _ = frame.shape
            red_mask = sf.mask_red(frame) #detecting red mask in the frame 
            red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #drawing contour for red mask
            min_x, min_y = width, height
            max_x = max_y = 0
            if(red_contours):
                red_contours_clean = sf.clean_contours(red_contours)
                if(red_contours_clean):
                        # Finding global maximum and minimum coordinates of the bounding boxes of the contours
                        for contour in red_contours_clean:
                            (x,y,w,h) = cv2.boundingRect(contour)
                            min_x, max_x = min(x, min_x), max(x+w, max_x)
                            min_y, max_y = min(y, min_y), max(y+h, max_y)
                            # if w > 80 and h > 80:
                            #     cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

                        if max_x - min_x > 0 and max_y - min_y > 0:
                            # Drawing the bounding box for the frame
                            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
                            cv2.circle(frame, (int((min_x+max_x)/2), int((min_y+max_y)/2)), 5, (25, 25, 25), 3)

                cv2.imshow('Frame detection', frame)

                 ## LED detection
                led_frame = frame.copy()
                led_frame[min_y+20:height, 0:width] = 0
                led_frame[0:height, 0:min_x] = 0
                led_frame[0:height, max_x:width] = 0
                
                if (max_y!=0):
                    green_mask = sf.mask_green(led_frame)
                    green_mask[min_y:height, 0:width] = 0
                    green_contours, _ = cv2.findContours(image=green_mask, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
                    green_contours_clean = sf.clean_contours(green_contours)
                    if(green_contours_clean):
                            for contour in green_contours_clean:
                                if(sf.aspect_ratio(contour)<1.05 and sf.aspect_ratio(contour)>0.95):
                                            x,y,w,h = cv2.boundingRect(contour)
                                            cv2.rectangle(led_frame, (x,y), (x+w,y+h), (0, 0, 255), 2)
                                            gx, gy = sf.center(contour)
                                            break
                                else:
                                            gx, gy = 0, 0
                            if(gx!=0 and gy!=0):
                                    led_frame = cv2.circle(led_frame, (gx, gy), 3, (0,0,0), 3)
                                    led_frame = cv2.putText(led_frame, text='GREEN', org=(gx+10, gy), fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
                    else:
                          print('No green LED detected')

                    cv2.imshow('led mask', led_frame)
                #cv2.imshow('red mask', red_mask)
            if (cv2.waitKey(delay) & 0xFF == ord('q')):
                break

stage2()
cv2.destroyAllWindows()
