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
                return
            frames[self.camID] = frame.copy() 

def gen_frames():  
    while True:
        frameout = cv2.hconcat([frames[0],frames[2]])
        ret, buffer = cv2.imencode('.jpg', frameout, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

thread1 = camThread(0)
thread2 = camThread(2)
thread1.start()
thread2.start()
