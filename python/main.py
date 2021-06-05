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
        test = cv.imread("./src/test.jpg")
        #img = cv.cvtColor(test, cv.COLOR_BGR2GRAY)
        #canny = cv.Canny(img, 50,100)
        #circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 2, 100, param1 = 100, param2 = 100, minRadius = 0, maxRadius = 500)
        #print(circles)
        #for i in circles[0,:]:
        #    cv.circle(test, (i[0],i[1]),int(i[2]),(0,255,0),2)
        #    cv.circle(test, (i[0],i[1]),2,(0,0,255),3)
        circle = pic.find_blue_circle(test)
        try:
            cv.circle(test,(circle[0],circle[1]),5,(0,0,255),3)
        except:
            print("not found")
        cv.imshow("circle", test)
        cv.waitKey()



if __name__ == '__main__':
    main()
