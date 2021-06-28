import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv


def take_pic(camera, rawCapture, Time=1):
    time.sleep(Time)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    rawCapture.truncate(0)
    return image


def show_red(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(img_hsv, (0, 150, 100), (15, 255, 255))
    mask2 = cv.inRange(img_hsv, (165, 150, 100), (180, 255, 255))
    mask = cv.bitwise_or(mask1, mask2)
    cropped = cv.bitwise_and(image, image, mask=mask)
    return cropped


def show_blue(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv, (90, 100, 50), (140, 255, 255))
    cropped = cv.bitwise_and(image, image, mask=mask)
    return cropped


def show_green(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv, (25, 100, 100), (40, 255, 255))
    cropped = cv.bitwise_and(image, image, mask=mask)
    return cropped


def find_circle(image, color):
    if color == "red":
        parameter2 = 10
    if color == "blue":
        parameter2 = 10
    if color == "green":
        parameter2 = 10
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 3, 100, param1=600,
                              param2=parameter2, minRadius=10, maxRadius=400)  # change param2
    return circles


def mask_red(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(img_hsv, (0, 150, 100), (15, 255, 255))
    mask2 = cv.inRange(img_hsv, (165, 150, 100), (180, 255, 255))
    mask = cv.bitwise_or(mask1, mask2)
    return mask


def mask_blue(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv, (90, 100, 50), (140, 255, 255))
    return mask


def mask_green(image):
    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv, (25, 100, 100), (40, 255, 255))
    return mask


def mask_color(image, color):
    if color == "red":
        return mask_red(image)
    if color == "blue":
        return mask_blue(image)
    if color == "green":
        return mask_green(image)


def circle_mask(image, circle):
    x = image.shape[0]
    y = image.shape[1]
    yy, xx = np.mgrid[:y, :x]
    distant = (xx - circle[0]) ** 2 + (yy - circle[1]) ** 2
    bool_mask = distant <= (circle[2] ** 2)
    mask = bool_mask.astype(np.uint8)
    mask *= 255
    return mask


def block_circle(image, circle):
    x = image.shape[0]
    y = image.shape[1]
    yy, xx = np.mgrid[:y, :x]
    distant = (xx - circle[0]) ** 2 + (yy - circle[1]) ** 2
    bool_mask = distant >= (circle[2] ** 2)
    mask = bool_mask.astype(np.uint8)
    mask *= 255
    return mask


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
    return x1, x2, y1, y2


def find_color_circle(image, color):
    circles = find_circle(image, color)
    try:
        for circle in circles[0]:
            mask = circle_mask(image, circle)
            '''
            mask = np.zeros(image.shape[:2], np.uint8)
            x1,x2,y1,y2 = rec_out_circle(circle,image)
            mask[x1:x2,y1:y2] = 255
            '''
            masked = cv.bitwise_and(image, image, mask=mask)
            if color == "red":
                color_mask = mask_red(masked)
            if color == "blue":
                color_mask = mask_blue(masked)
            if color == "green":
                color_mask = mask_green(masked)

            if color_mask.sum() >= 255 * 0.7 * circle[2] ** 2 * np.pi:
                return circle
        return None
    except:
        return None


def find_red_circle(image):
    image = show_red(image)
    circles = find_circle(image, "red")
    try:
        for circle in circles[0]:
            mask = circle_mask(image, circle)
            masked = cv.bitwise_and(image, image, mask=mask)
            red_mask = mask_red(masked)
            if red_mask.sum() >= 255 * 0.7 * circle[2] ** 2 * np.pi:
                return circle
        return None
    except:
        return None


def find_blue_circle(image):
    image = show_blue(image)
    circles = find_circle(image, "blue")
    try:
        for circle in circles[0]:
            mask = circle_mask(image, circle)
            masked = cv.bitwise_and(image, image, mask=mask)
            blue_mask = mask_blue(masked)
            if blue_mask.sum() >= 255 * 0.7 * circle[2] ** 2 * np.pi:
                return circle
        return None
    except:
        return None


def find_green_circle(image):
    image = show_green(image)
    circles = find_circle(image, "green")
    try:
        for circle in circles[0]:
            mask = circle_mask(image, circle)
            masked = cv.bitwise_and(image, image, mask=mask)
            green_mask = mask_green(masked)
            if green_mask.sum() >= 255 * 0.7 * circle[2] ** 2 * np.pi:
                return circle
        return None
    except:
        return None


def direct(mask, threshold, size):
    total = mask.sum() / 255
    half_len = mask.shape[1] // 2
    weighted = np.arange(-half_len,
                         mask.shape[1] - half_len).astype("float64") / 255
    sumup = 0
    for y in range(mask.shape[0]):
        sumup += np.dot(mask[y].astype("float64"), weighted)
    if total != 0:
        final = sumup / total
    else:
        final = 300
    print(final)
    target = False
    direction = "straight"
    if final < -threshold:
        direction = "left"
    if final > threshold:
        direction = "right"
    if final == 300:
        direction = "right_more"
    if total > size:
        target = True
    return direction, target


def detect_object(image, color_dict, threshold, size):
    circle = list()
    circle.append(find_red_circle(image))
    circle.append(find_blue_circle(image))
    circle.append(find_green_circle(image))
    mask = 255 * np.ones(image.shape[:2], np.uint8)
    masked = image
    for index in range(3):
        if circle[index] is not None:
            mask = block_circle(image, circle[index])
            masked = cv.bitwise_and(masked, masked, mask=mask)
    print(mask.sum() /255)
    red_mask = mask_red(masked)
    print(red_mask.sum() / 255)
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
    return None, "right_more", False


def track_object(image, color, threshold):
    circle = find_color_circle(image, color)
    mask = 255 * np.ones(image.shape[:2], np.uint8)
    masked = image
    if circle is not None:
        x1, x2, y1, y2 = rec_out_circle(circle, image)
        mask[x1:x2, y1:y2] = 0
        masked = cv.bitwise_and(masked, masked, mask=mask)
    color_mask = mask_color(masked, color)
    direction, target = direct(color_mask, threshold, 1000)
    return direction


def detect_storage(image, color, threshold, radius=100):
    if color == "red":
        circle = find_red_circle(image)
    if color == "blue":
        circle = find_blue_circle(image)
    if color == "green":
        circle = find_green_circle(image)
    half_len = image.shape[1] // 2
    print(circle)
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
    return "right_more", False
