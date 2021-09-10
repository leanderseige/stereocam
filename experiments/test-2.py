import cv2


w1 = cv2.namedWindow("W1")
w2 = cv2.namedWindow("W2")
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

  key = cv2.waitKey(20)
  if key == 27:  # exit on ESC
    break

cv2.destroyWindow("W1")
#cv2.destroyWindow("W2")
