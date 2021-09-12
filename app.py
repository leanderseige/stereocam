from flask import Flask, Response
import cv2
from datetime import datetime


app = Flask(__name__)

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

font = cv2.FONT_HERSHEY_SIMPLEX
org = (60, 240)
fontScale = 1
color = (32, 255, 32)
thickness = 2

face_cascade = cv2.CascadeClassifier('cv-haarcascades/haarcascade_frontalface_default.xml')

def gen_frames():
    while True:
        success1, frame1 = cam1.read()  # read the camera frame
        success2, frame2 = cam2.read()  # read the camera frame
        if not (success1 & success2) :
            break
        else:
            frame1 = cv2.putText(frame1, datetime.utcnow().strftime('%H:%M:%S.%f')[:-3], org, font, fontScale, color, thickness, cv2.LINE_AA)
            faces = face_cascade.detectMultiScale(frame2, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame2, (x, y), (x+w, y+h), (32, 32, 255), 2)
            frame3 = cv2.hconcat([frame1,frame2])
            ret, buffer = cv2.imencode('.jpg', frame3, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/video')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/html')
def html():
    return '<html><body style="padding:0;margin:0;background-color:black;"><img onclick="document.documentElement.requestFullscreen()" src="/video" style="width:100vw;margin:auto;" /></body></html>'

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
