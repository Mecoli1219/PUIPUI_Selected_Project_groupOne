from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv
import serial
import numpy as np
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
    color_dict = {"red":1, "blue":1, "green":1}

    if (sys.argv[1] == '0'):
        target = 3
        get_target = False
        lock_target = False
        while True:
            image = pic.take_pic(camera,rawCapture,0.1)
            if not lock_target:
                next_color, direction, lock_target = pic.detect_object(image, color_dict, 20, 2500)
                ser.write(b"%s\n" % direction)
            elif lock_target:
                pass

    elif (sys.argv[1] == '1'):
        test = cv.imread("./src/test.jpg")
        print(test.shape)
        next_color, direction, target = pic.detect_object(test, color_dict, 20, 2500)
        print(next_color, direction, target)
        cv.imshow("circle", test)
        cv.waitKey()



if __name__ == '__main__':
    main()
