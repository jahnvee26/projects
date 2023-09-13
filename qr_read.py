import cv2
import sys
from pyzbar.pyzbar import decode
import numpy as np
import imutils
import requests
  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.0.102:8080/shot.jpg"
  

def qr_read():
    delay = 1
    window_name = 'frame'

    #cap = cv2.VideoCapture('/dev/v4l/by-id/usb-SunplusIT_Inc_HP_TrueVision_HD_Camera-video-index0')

    #if not cap.isOpened():
        #sys.exit()

    while True:
        #ret, frame = cap.read()
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        frame = imutils.resize(frame, width=1000, height=1800)
        k = False
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteFrame) = cv2.threshold(grayFrame, 80, 255, cv2.THRESH_BINARY)
        if True:
            for d in decode(blackAndWhiteFrame):
                s = d.data.decode()
                k = get_coords(s)
                blackAndWhiteFrame = cv2.rectangle(blackAndWhiteFrame, (d.rect.left, d.rect.top),
                                    (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (0, 255, 0), 3)
                blackAndWhiteFrame = cv2.putText(blackAndWhiteFrame, s, (d.rect.left, d.rect.top + d.rect.height),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                cx = int(d.rect.left + d.rect.width/2)
                cy = int(d.rect.top + d.rect.height/2)
                blackAndWhiteFrame = cv2.circle(blackAndWhiteFrame, (cx, cy), 5, (25, 25, 25), 3)
                print(cx, cy)
            cv2.imshow('bw frame', blackAndWhiteFrame)
            for d in decode(frame):
                s = d.data.decode()
                k = get_coords(s)
                frame = cv2.rectangle(frame, (d.rect.left, d.rect.top),
                                    (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (0, 255, 0), 3)
                frame = cv2.putText(frame, s, (d.rect.left, d.rect.top + d.rect.height),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                cx = int(d.rect.left + d.rect.width/2)
                cy = int(d.rect.top + d.rect.height/2)
                frame = cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
                print(cx, cy)
            cv2.imshow('frame', frame)
        if (cv2.waitKey(delay) & 0xFF == ord('q')):
            break

    cv2.destroyWindow(window_name)

def get_coords(s):
    coords1 = []
    coords2 = []
    coords = []
    if(s!=''):
        x = s.split(",")
        if(np.size(x)==4):
            coords1.append(float(s.split(",")[0][2:]))
            coords1.append(float(s.split(",")[1][:-1]))
            coords2.append(float(s.split(",")[2][1:]))
            coords2.append(float(s.split(",")[3][:-2]))
            coords = np.array([coords1, coords2])
        elif(np.size(x)==2):
            coords1.append(float(s.split(",")[0][1:]))
            coords1.append(float(s.split(",")[1][:-1]))
            coords = np.array(coords1)
        print(coords)
        return True
    else:
        return False

qr_read()
