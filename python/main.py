from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv
import matplotlib.pyplot as plt
import serial
import numpy as np
import pandas
import time
import sys
import os


def main():

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    print("Successfully connect to Arduino!")

    camera = PiCamera();
    rawCapture = PiRGBArray(camera)

    if (sys.argv[1] == '0'):
        n = 1

        while n == 1:
            n = 2
            time.sleep(0.1)
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            print(image)


    elif (sys.argv[1] == '1'):
        img = cv.imread("./src/test.jpg")
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask1 = cv.inRange(img_hsv,(0,50,20),(5,255,255))
        mask2 = cv.inRange(img_hsv,(175,50,20), (180,255,255))
        mask = cv.bitwise_or(mask1, mask2)
        croped = cv.bitwise_and(img,img, mask = mask)
        print(img.shape)
        print(mask.shape)
        cv.imshow("croped", croped)
        cv.waitKey()



if __name__ == '__main__':
    main()
