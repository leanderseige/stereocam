import cv2
import numpy as np


w1 = cv2.namedWindow("W1")
w2 = cv2.namedWindow("W2")
w2 = cv2.namedWindow("W3")
cam1 = cv2.VideoCapture(2)
cam2 = cv2.VideoCapture(0)

while True:
  rval1, frame1 = cam1.read()
  if (rval1):
    frame1 = cv2.resize(frame1, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow("W1", frame1)

  rval2, frame2 = cam2.read()
  if (rval2):
    frame2 = cv2.resize(frame2, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow("W2", frame2)

  if (rval1 and rval2):
    frame3 = cv2.hconcat([frame1,frame2])
    cv2.imshow("W3", frame3)

  key = cv2.waitKey(20)
  if key == 27:  # exit on ESC
    break

cv2.destroyWindow("W1")
cv2.destroyWindow("W3")
cv2.destroyWindow("W3")
