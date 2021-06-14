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


def show_red(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(img_hsv,(0,150,130),(15,255,255))
    mask2 = cv.inRange(img_hsv,(165,150,130), (180,255,255))
    mask = cv.bitwise_or(mask1, mask2)
    cropped = cv.bitwise_and(image, image, mask = mask)
    return cropped
    
def show_blue(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv,(90,100,50),(140,255,255))
    cropped = cv.bitwise_and(image, image, mask = mask)
    return cropped
    
def show_green(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv,(40,100,180),(80,255,255))
    cropped = cv.bitwise_and(image, image, mask = mask)
    return cropped

def find_circle(image):
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 5, 100, param1 = 800, param2 = 130, minRadius = 10, maxRadius = 400) # change param2
    return circles    

def mask_red(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(img_hsv,(0,150,130),(15,255,255))
    mask2 = cv.inRange(img_hsv,(165,150,130), (180,255,255))
    mask = cv.bitwise_or(mask1, mask2)
    return mask

def mask_blue(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv,(90,100,50),(140,255,255))
    return mask
    
def mask_green(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv,(40,100,180),(80,255,255))
    return mask

def mask_color(image, color):
    if color == "red":
        return mask_red(image)
    if color == "blue":
        return mask_blue(image)
    if color == "green":
        return mask_green(image)


def rec_out_circle(circle, image):
    x1 = int(circle[1] - circle[2])
    x2 = int(circle[1] + circle[2])
    y1 = int(circle[0] - circle[2])
    y2 = int(circle[0] + circle[2])
    if x1 < 0:
        x1 = 0
    if x2 > image.shape[1]:
        x2 = image.shape[1]
    if y1 < 0:
        y1 = 0
    if y2 > image.shape[0]:
        y2 = image.shape[0]
    return x1,x2,y1,y2

def find_color_circle(image, color):
    circles = find_circle(image)
    try:
        for circle in circles[0]:    
            mask = np.zeros(image.shape[:2], np.uint8)
            x1,x2,y1,y2 = rec_out_circle(circle,image)
            mask[x1:x2,y1:y2] = 255
            masked = cv.bitwise_and(image, image, mask = mask)
            if color == "red":
                color_mask = mask_red(masked)
            if color == "blue":
                color_mask = mask_blue(masked)
            if color == "green":
                color_mask = mask_green(masked)

            if color_mask.sum() >= 255 * 0.4 * circle[2] ** 2:
                return circle
        return None
    except:
        return None


def find_red_circle(image):
    circles = find_circle(image)
    try:
        for circle in circles[0]:    
            mask = np.zeros(image.shape[:2], np.uint8)
            x1,x2,y1,y2 = rec_out_circle(circle,image)
            mask[x1:x2,y1:y2] = 255
            masked = cv.bitwise_and(image, image, mask = mask)
            red_mask = mask_red(masked)
            if red_mask.sum() >= 255 * 0.4 * circle[2] ** 2:
                return circle
        return None
    except:
        return None

def find_blue_circle(image):
    circles = find_circle(image)
    try:
        for circle in circles[0]:    
            mask = np.zeros(image.shape[:2], np.uint8)
            x1,x2,y1,y2 = rec_out_circle(circle,image)
            mask[x1:x2,y1:y2] = 255
            masked = cv.bitwise_and(image, image, mask = mask)
            blue_mask = mask_blue(masked)
            if blue_mask.sum() >= 255 * 0.4 * circle[2] ** 2:
                return circle
        return None
    except:
        return None

def find_green_circle(image):
    circles = find_circle(image)
    try:
        for circle in circles[0]:    
            mask = np.zeros(image.shape[:2], np.uint8)
            x1,x2,y1,y2 = rec_out_circle(circle, image)
            mask[x1:x2,y1:y2] = 255
            masked = cv.bitwise_and(image, image, mask = mask)
            green_mask = mask_green(masked)
            if green_mask.sum() >= 255 * 0.4 * circle[2] ** 2:
                return circle
        return None
    except:
        return None

def direct(mask, threshold = 50, size = 2500):
    total = mask.sum() / 255
    half_len = mask.shape[1] // 2
    weighted = np.arange(-half_len, mask.shape[1] - half_len).astype("float64") / 255 
    sumup = 0
    for y in range(mask.shape[0]):
        sumup += np.dot(mask[y].astype("float64"), weighted)
    try:
        final = sumup / total
    except:
        final = 0
    target = False
    direction = "straight"
    if final < -threshold:
        direction =  "left"
    if final > threshold:
        direction =  "right"
    if total > size:
        target = True
    return direction, target

def detect_object(image, color_dict, threshold = 50, size = 2500):
    circle = list()
    circle.append(find_color_circle(image, "red"))
    circle.append(find_color_circle(image, "blue"))
    circle.append(find_color_circle(image, "green"))
    mask = 255 * np.ones(image.shape[:2], np.uint8)
    masked = image
    for index in range(3):
        if circle[index] is not None:
            x1, x2, y1, y2 = rec_out_circle(circle[index], image)
            mask[x1:x2,y1:y2] = 0
            masked = cv.bitwise_and(masked, masked, mask = mask)
    red_mask = mask_red(masked)
    blue_mask = mask_blue(masked)
    green_mask = mask_green(masked)
    if color_dict["blue"] > 0:
        blue_num = blue_mask.sum() // 255
    else:
        blue_num = -1
    if color_dict["green"] > 0:
        green_num = green_mask.sum() // 255
    else:
        green_num = -1
    if color_dict["red"] > 0:
        red_num = red_mask.sum() // 255
    else:
        red_num = -1
    if red_num >= blue_num and red_num >= green_num and red_num != -1:
        next_color = None
        direction, target = direct(red_mask, threshold, size)
        if target:
            next_color = "red"
        return next_color, direction, target
    if blue_num >= red_num and blue_num >= green_num and blue_num != -1:
        next_color = None
        direction, target = direct(blue_mask, threshold, size)
        if target:
            next_color = "blue"
        return next_color, direction, target
    if green_num >= blue_num and green_num >= red_num and green_num != -1:
        next_color = None
        direction, target = direct(green_mask, threshold, size)
        if target:
            next_color = "green"
        return next_color, direction, target
    return None, "right", False

def track_object(image, color, threshold = 50):
    circle = find_color_circle(image, color)
    mask = 255 * np.ones(image.shape[:2], np.uint8)
    masked = image
    if circle is not None:
        x1, x2, y1, y2 = rec_out_circle(circle, image)
        mask[x1:x2,y1:y2] = 0
        masked = cv.bitwise_and(masked, masked, mask = mask)
    color_mask = mask_color(masked, color)
    direction, target = direct(color_mask, threshold, 1000)
    return direction

def detect_storage(image, color, threshold = 20, radius = 100):
    circle = find_color_circle(image, color)
    half_len = image.shape[1] // 2
    if circle is not None:
        arrive = False
        if circle[0] - half_len > threshold:
            direction = "right"
        elif half_len - circle[0] > threshold:
            direction = "left"
        else:
            direction = "straight"
            if circle[2] >= radius:
                arrive = True
        return direction, arrive
    return  "right", False
    


