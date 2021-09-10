from flask import Flask, Response
import cv2

app = Flask(__name__)

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

def oneFrame():
    success1, frame1 = cam1.read()  # read the camera frame
    if not (success1) :
        return  
    ret, buffer = cv2.imencode('.jpg', frame1, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
    frame = buffer.tobytes()
    yield(frame) # concat frame one by one and show result

def gen_frames():  
    while True:
        success1, frame1 = cam1.read()  # read the camera frame
        success2, frame2 = cam2.read()  # read the camera frame
        if not (success1 & success2) :
            break
        else:
            frame3 = cv2.hconcat([frame1,frame2])
            ret, buffer = cv2.imencode('.jpg', frame3, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_1frames():  
    while True:
        success1, frame1 = cam1.read()  # read the camera frame
        if not (success1) :
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame1, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_2frames():  
    while True:
        success2, frame2 = cam2.read()  # read the camera frame
        if not (success2) :
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame2, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/video')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video1')
def video_1feed():
    return Response(gen_1frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video2')
def video_2feed():
    return Response(gen_2frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/one')
def one():
    return Response(oneFrame(), mimetype='image/jpeg')

@app.route('/html')
def html():
    return '<html><body style="padding:0;margin:0;background-color:black;"><img onclick="document.documentElement.requestFullscreen()" src="/video" style="width:100vw;margin:auto;" /></body></html>'

@app.route('/html2')
def html2():
    return '<html><body style="padding:0;margin:0;background-color:black;"><img onclick="document.documentElement.requestFullscreen()" src="/video1" style="width:50vw;" /><img src="/video2" style="width:50vw;" /></body></html>'

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
