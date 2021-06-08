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
    camera.resolution = (1920,1080)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1920,1080))
    color_dict = {"red":1, "blue":1, "green":1}
    
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(2)
    catch_distance = 3 # cm
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
            image = pic.take_pic(camera,rawCapture,0.1)
            if not lock_target:
                print("find target")
                next_color, direction, lock_target = pic.detect_object(image, color_dict, 20, 2500)
                print("Sent command: %s" % direction)
                command = "{}\n".format(direction)
                ser.write(command.encode())
            elif lock_target and not get_target:
                print("track target")
                direction = pic.track_object(image, next_color, 100)
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
                    
                    if distant <= catch_distant:
                        print("Sent command: catch")
                        ser.write(b"catch\n")
                        get_target = True
            elif get_target:
                print("find storage")
                direction, arrive = pic.detect_storage(image, next_color, 20, 100)
                if arrive:
                    print("Sent command: drop")
                    ser.write(b"drop\n")
                    color_dict[next_color] -= 1 
                    get_target = False
                    lock_target = False
                    next_color = None
                else:
                    print("Sent command: %s" % direction)
                    command = "{}\n".format(direction)
                    ser.write(command.encode())


    elif (sys.argv[1] == '1'):
        test = cv.imread("./src/test.jpg")
        print(test.shape)
        next_color, direction, target = pic.detect_object(test, color_dict, 20, 2500)
        print(next_color, direction, target)
        cv.imshow("circle", test)
        cv.waitKey()



if __name__ == '__main__':
    main()
