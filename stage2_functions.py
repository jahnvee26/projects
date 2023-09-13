import cv2
import sys
import numpy as np

delay = 1
center_x = 0
center_y = 0
resolution = 5

def aspect_ratio(cnt):
        x,y,w,h = cv2.boundingRect(cnt)
        ar = float(w)/float(h)
        return ar
def center(cnt):
        x,y,w,h = cv2.boundingRect(cnt)
        cx = int(x+w/2)
        cy = int(y+h/2)
        return cx,cy

def mask_red(frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
        # lower boundary RED color range values; Hue (0 - 8)
        red_lower1 = np.array([0, 100, 150])
        red_upper1 = np.array([5, 255, 255])
        
        # upper boundary RED color range values; Hue (160 - 179)
        red_lower2 = np.array([160,100,150])
        red_upper2 = np.array([180,255,255])
        
        red_lower_mask = cv2.inRange(hsv, red_lower1, red_upper1)
        red_upper_mask = cv2.inRange(hsv, red_lower2, red_upper2)
        
        red_mask = red_lower_mask + red_upper_mask
        return red_mask

def mask_green(frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        # lower boundary GREEN color range values; Hue (40 - 80)
        green_lower = np.array([50, 100, 20])
        green_upper = np.array([85, 255, 255])

        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        
        return green_mask


def clean_contours(contours):
        global center_x
        global center_y
        global resolution
        contours_sorted = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        contours_clean = []

        for i in range(len(contours_sorted)):
                if(cv2.contourArea(contours_sorted[i])<100 or cv2.contourArea(contours_sorted[i])>100000):
                        continue
                else:
                        contours_clean.append(contours_sorted[i])
        if(len(contours_clean)>resolution):
                contours_clean = contours_clean[0:resolution]
        else:
                contours_clean = contours_clean
        return contours_clean
        


