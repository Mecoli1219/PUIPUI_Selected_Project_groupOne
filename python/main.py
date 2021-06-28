from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv
import serial
import numpy as np
import time
import sys
import os
import picture as pic
import RPi.GPIO as GPIO


def main():
    camera = PiCamera()
    camera.resolution = (512, 512)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(512, 512))
    color_dict = {"red": 1, "blue": 0, "green": 1}
    
    object_mask = np.zeros((512,512), np.uint8)
    object_mask[350:,:] = 255
    storage_mask = np.zeros((512,512), np.uint8)
    storage_mask[100:320,:] = 255
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(2)
    catch_distance = 10.5  # cm
    sound_speed = 17150

    if (sys.argv[1] == '0'):
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flush()
        print("Successfully connect to Arduino!")

        target = sum(color_dict.values())
        get_target = False
        lock_target = False
        next_color = None
        while True:
            image = pic.take_pic(camera, rawCapture, 0.1)
            if not lock_target:
                print("find target")
                image = cv.bitwise_and(image,image,mask = object_mask)
                next_color, direction, lock_target = pic.detect_object(
                    image, color_dict, 100, 5000)
                print("Sent command: %s" % direction)
                command = "{}\n".format(direction)
                ser.write(command.encode())
            elif lock_target and not get_target:
                print("track target: %s" % next_color)
                image = cv.bitwise_and(image,image,mask = object_mask)
                direction = pic.track_object(image, next_color, 50)
                print("Sent command: %s" % direction)
                command = "{}\n".format(direction)
                ser.write(command.encode())
                if direction == "straight":
                    GPIO.output(TRIG, True)
                    time.sleep(0.00001)
                    GPIO.output(TRIG, False)

                    while GPIO.input(ECHO) == 0:
                        pulse_start = time.time()

                    while GPIO.input(ECHO) == 1:
                        pulse_end = time.time()

                    pulse_duration = pulse_end - pulse_start
                    distant = pulse_duration * sound_speed

                    if distant <= catch_distance:
                        print("Sent command: catch")
                        while True:
                            ser.write(b"catch\n")
                            time.sleep(3)
                            waiting = ser.inWaiting()
                            rv = ser.read(waiting)
                            if(rv):
                                print(rv)
                                ser.flushInput()
                                break
                        ser.flush()
                        get_target = True
            elif get_target:
                print("find storage")
                image = cv.bitwise_and(image,image, mask = storage_mask)
                direction, arrive = pic.detect_storage(
                    image, next_color, 50, 120)
                if arrive:
                    print("Sent command: drop")
                    while True:
                        ser.write(b"drop\n")
                        time.sleep(3)
                        waiting = ser.inWaiting()
                        rv = ser.read(waiting)
                        if(rv):
                            print(rv)
                            ser.flushInput()
                            break
                    ser.flush()
                    color_dict[next_color] -= 1
                    get_target = False
                    lock_target = False
                    next_color = None
                else:
                    print("Sent command: %s" % direction)
                    command = "{}\n".format(direction)
                    ser.write(command.encode())

    elif (sys.argv[1] == '1'):
        while True:
            image = pic.take_pic(camera, rawCapture, 0.1)
            image = cv.bitwise_and(image,image, mask = storage_mask)
            circles = (pic.find_circle(pic.show_red(image), "red"))
            img = pic.show_red(image)
            red_mask = pic.mask_red(image)
            test = (image)
            print(circles)
            canny = cv.Canny(img, 400, 800)
            if circles is not None:
                for circle in circles[0, :]:
                    cv.circle(img, (circle[0], circle[1]),
                              int(circle[2]), (0, 255, 0), 2)
            circle = pic.find_green_circle(image)
            print(circle)
            if circle is not None:
                mask = pic.circle_mask(test, circle)
                test = cv.bitwise_and(test, test, mask=mask)
                cv.circle(img, (circle[0], circle[1]),
                          int(circle[2]), (255, 255, 0), 2)
            red = cv.bitwise_and(image,image, mask = red_mask)
            cv.imshow("initial", image)
            #cv.imshow("image", img)
            #cv.imshow("test", test)
            cv.imshow("red", red)
           # cv.imshow("canny", canny)
            cv.waitKey(1)

    elif (sys.argv[1] == '2'):
        while True:
            image = pic.take_pic(camera, rawCapture, 0.1)
            image = cv.bitwise_and(image,image, mask = object_mask)
            circles = (pic.find_circle(pic.show_red(image), "red"))
            img = pic.show_red(image)
            green_mask = pic.mask_green(image)
            test = (image)
            print(circles)
            canny = cv.Canny(img, 400, 800)
            if circles is not None:
                for circle in circles[0, :]:
                    cv.circle(img, (circle[0], circle[1]),
                              int(circle[2]), (0, 255, 0), 2)
            circle = pic.find_green_circle(image)
            print(circle)
            if circle is not None:
                mask = pic.circle_mask(test, circle)
                test = cv.bitwise_and(test, test, mask=mask)
                cv.circle(img, (circle[0], circle[1]),
                          int(circle[2]), (255, 255, 0), 2)
            green = cv.bitwise_and(image,image, mask = green_mask)
            cv.imshow("initial", image)
            #cv.imshow("image", img)
            #cv.imshow("test", test)
            cv.imshow("red", green)
            cv.waitKey(1)


if __name__ == '__main__':
    main()
