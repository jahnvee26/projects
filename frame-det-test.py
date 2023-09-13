import cv2
import sys
import numpy as np

delay = 1
center_x = 0
center_y = 0
resolution = 5

cap = cv2.VideoCapture(0)
if not cap.isOpened():
        sys.exit()

def aspect_ratio(cnt):
        x,y,w,h = cv2.boundingRect(cnt)
        ar = float(w)/float(h)
        return ar
def center(cnt):
        M = cv2.moments(cnt)
        if(M['m00']!=0):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                return cx,cy
        else:
                return 0,0
def mask_red(frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
        # lower boundary RED color range values; Hue (0 - 8)
        red_lower1 = np.array([0, 100, 120])
        red_upper1 = np.array([5, 255, 255])
        
        # upper boundary RED color range values; Hue (160 - 179)
        red_lower2 = np.array([160,100,120])
        red_upper2 = np.array([180,255,255])
        
        red_lower_mask = cv2.inRange(hsv, red_lower1, red_upper1)
        red_upper_mask = cv2.inRange(hsv, red_lower2, red_upper2)
        
        red_mask = red_lower_mask + red_upper_mask
        return red_mask

def mask_green(frame, ox, oy):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        # Masking the GREEN color detection below center of frame to avoid grass
        hsv[oy:, 0:width] = 0

        # lower boundary GREEN color range values; Hue (40 - 80)
        green_lower = np.array([40, 100, 20])
        green_upper = np.array([80, 255, 255])

        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        return green_mask

def approx_frame_center(red_contours):
        global center_x
        global center_y
        global resolution
        red_contours_sorted = sorted(red_contours, key=lambda x: cv2.contourArea(x), reverse=True)
        red_contours_clean = []
        centers_x = []
        centers_y = []
        area = []
        y_coords = np.zeros(5)

        for i in range(len(red_contours_sorted)):
                if(cv2.contourArea(red_contours_sorted[i])<50 or cv2.contourArea(red_contours_sorted[i])>100000):
                        continue
                else:
                        red_contours_clean.append(red_contours_sorted[i])
        if(len(red_contours_clean)<resolution):
               return red_contours, 0
        else:
                for i in range(resolution):
                        area.append(cv2.contourArea(red_contours_clean[i]))
                        rect = cv2.minAreaRect(red_contours_clean[i])
                        box = cv2.boxPoints(rect)
                        box = np.intp(box)
                        y_coords[i] = int(min(box[0][1], box[1][1], box[2][1], box[3][1]))
                        centers_x.append(int((box[0][0]+box[1][0]+box[2][0]+box[3][0])/4))
                        centers_y.append(int((box[0][1]+box[1][1]+box[2][1]+box[3][1])/4))
                y_max = int(np.min(y_coords))
                center_x = int(np.average(centers_x, weights=area))
                center_y = int(np.average(centers_y, weights=area))
                return red_contours_clean[0:resolution], y_max
        
        
while True:
    ret, frame = cap.read()
    if ret:
        height, width, _ = frame.shape
        cx = int(width/2)
        cy = int(height/2)

        red_mask = mask_red(frame)
        red_contours, red_hierarchy = cv2.findContours(image=red_mask, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
        ar=0
        image_copy = frame.copy()
        led_frame = frame.copy()
        if(red_contours):
                red_c = max(red_contours, key=cv2.contourArea)
                ar = aspect_ratio(red_c)
                ox, oy = center(red_c)
                red_contours_copy = frame.copy()
                red_contours_clean, y_max = approx_frame_center(red_contours)
                if(center_x!=0 and center_y!=0 and y_max!=0):
                        image_copy = cv2.circle(image_copy, (center_x, center_y), 5, (25, 25, 25), 3)
                        cv2.drawContours(image=red_contours_copy, contours=red_contours_clean, contourIdx=-1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
                        led_frame[y_max:height, 0:width] = 0
                cv2.imshow('red contours', red_contours_copy)
                cv2.imshow('led mask', led_frame)
                green_mask = mask_green(led_frame, ox, oy)
                green_contours, green_hierarchy = cv2.findContours(image=green_mask, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
                if(green_contours):
                        green_c = max(green_contours, key=cv2.contourArea)
                        gx, gy = center(green_c)
                        if(gx!=0 and gy!=0):
                                image_copy = cv2.circle(image_copy, (gx, gy), 3, (25, 25, 25), 3)
                                image_copy = cv2.putText(image_copy, text='GREEN', org=(gx+10, gy), fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
                                cv2.imshow('green mask', green_mask)

                cv2.imshow('frame copy',image_copy)
                cv2.imshow('red mask', red_mask)
    if (cv2.waitKey(delay) & 0xFF == ord('q')):
        break

cv2.destroyAllWindows()
