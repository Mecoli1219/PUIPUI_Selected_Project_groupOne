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

    
    n = 1

    while n == 1:
        n = 2
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        print(image)



if __name__ == '__main__':
    main()
