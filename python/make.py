
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = np.zeros((512, 600, 3),  np.uint8)

cv.line(img, (0, 0), (511, 511), (255, 0, 0), 5)
cv.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)
cv.rectangle(img, (384, 200), (510, 400), (0, 0, 255), 120)
cv.circle(img, (447, 64), 64, (0, 0, 255), -1)
cv.circle(img, (111, 20), 21, (255, 0, 0), -1)
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img, 'SwordArtOnline', (10, 500),
           font, 2, (255, 255, 255), 2, cv.LINE_AA)
cv.imwrite("./src/test.jpg", img)
