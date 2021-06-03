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
import picture as pic

def main():

    # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    # ser.flush()
    print("Successfully connect to Arduino!")

    camera = PiCamera()
    camera.resolution = (1920,1080)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1920,1080))

    if (sys.argv[1] == '0'):
        n = 1

        while True:
            image = pic.take_pic(camera,rawCapture,0.1)
            #image_red = pic.filter_red(image)
            #image_blue = pic.filter_blue(image)
            image_green = pic.filter_green(image)
            #cv.imshow("image_red",image_red)
            #cv.imshow("image_blue",image_blue)
            cv.imshow("image_green",image_green)
            cv.waitKey(1)

    elif (sys.argv[1] == '1'):
        img = cv.imread("./b.jpg")
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask_red1 = cv.inRange(img_hsv,(0,50,20),(5,255,255))
        mask_red2 = cv.inRange(img_hsv,(175,50,20),(180,255,255))
        mask_blue = cv.inRange(img_hsv,(110,50,50),(130,255,255))
        mask_green = cv.inRange(img_hsv,(40,40,40),(70,255,255))
        mask_red = cv.bitwise_or(mask_red1, mask_red2)
        croped_red = cv.bitwise_and(img,img, mask = mask_red)
        croped_blue = cv.bitwise_and(img,img, mask = mask_blue)
        croped_green = cv.bitwise_and(img,img, mask = mask_green)
        print(img.shape)
        cv.imshow("red", croped_red)
        cv.imshow("blue", croped_blue)
        cv.imshow("green", croped_green)
        cv.waitKey()



if __name__ == '__main__':
    main()
