from flask import Flask, Response
import cv2
import threading

app = Flask(__name__)

frames = {}

class camThread(threading.Thread):
    def __init__(self, camID):
        threading.Thread.__init__(self)
        self.camID = camID
        self.cam = cv2.VideoCapture(camID)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    def run(self):
        while True:
            success, frame = self.cam.read()
            if not success:
                continue
            frames[self.camID] = frame.copy()

def gen_frames(camID):
    while True:
        ret, buffer = cv2.imencode('.jpg', frames[camID], [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video1')
def video1_feed():
    return Response(gen_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video2')
def video2_feed():
    return Response(gen_frames(2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/html')
def html():
    return '<html><body style="padding:0;margin:0;background-color:black;"><img onclick="document.documentElement.requestFullscreen()" src="/video1" style="width:50vw;" /><img src="/video2" style="width:50vw;" /></body></html>'

thread1 = camThread(0)
thread2 = camThread(2)
thread1.start()
thread2.start()
