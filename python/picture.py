import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv



def take_pic(camera, rawCapture, Time = 1):
    time.sleep(Time)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    rawCapture.truncate(0)
    return image[:,:,::-1] 


def filter_red(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(img_hsv,(0,150,50),(15,255,255))
    mask2 = cv.inRange(img_hsv,(165,150,50), (180,255,255))
    mask = cv.bitwise_or(mask1, mask2)
    cropped = cv.bitwise_and(image,image, mask = mask)
    return cropped
    
def filter_blue(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv,(90,100,50),(140,255,255))
    cropped = cv.bitwise_and(image,image, mask = mask)
    return cropped
    
def filter_green(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv,(40,100,40),(80,255,255))
    cropped = cv.bitwise_and(image,image, mask = mask)
    return cropped

