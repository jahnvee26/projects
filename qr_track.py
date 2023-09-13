import cv2
import sys
from pyzbar.pyzbar import decode
import numpy as np
import RPi.GPIO as GPIO

def qr_read():
    delay = 1
    window_name = 'frame'

    cap = cv2.VideoCapture('/dev/v4l/by-id/usb-9726-200619_Integrated_Camera-video-index0')

    if not cap.isOpened():
        sys.exit()

    while True:
        ret, frame = cap.read()
        k = False
        #cv2.imshow(window_name, frame)
        if ret:
            for d in decode(frame):
                s = d.data.decode()
                frame = cv2.rectangle(frame, (d.rect.left, d.rect.top),
                                    (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (0, 255, 0), 3)
                frame = cv2.putText(frame, s, (d.rect.left, d.rect.top + d.rect.height),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                cx = int(d.rect.left + d.rect.width/2)
                cy = int(d.rect.top + d.rect.height/2)
                height, width, _ = frame.shape
                ox = int(height/2)
                oy = int(width/2)
                dx = cx - ox
                K = (d.rect.width*d.rect.height)/(width*height)
                print(K*dx*0.3)
                frame = cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
            cv2.imshow(window_name, frame)
        if (cv2.waitKey(delay) & 0xFF == ord('q')):
            break

    cv2.destroyWindow(window_name)

def SetAngle(angle):

	duty = angle / 18 + 2

	GPIO.output(03, True)

	pwm.ChangeDutyCycle(duty)

	sleep(1)

	GPIO.output(03, False)

	pwm.ChangeDutyCycle(0)
qr_read()
