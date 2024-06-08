from flask import Flask, Response, render_template_string
import cv2

import face

app = Flask(__name__)

cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        _,img = cap.read()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert RGB to BGR
        res, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        face.detect_face(cap)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>LIVE CAM</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-size: cover;
                background-position: center;
                color: white;
            }
            .container {
                text-align: center;
                background: blue;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
            }
            .clock {
                font-size: 2em;
                margin-bottom: 20px;
            }
            .title {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .video-container {
                position: relative;
                display: inline-block;
                border: 5px solid #fff;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            }
            video {
                display: block;
                width: 150%;
                height: auto;
            }
            .time {
                color: red;
                }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="video-container">
                <img src="{{ url_for('video_feed') }}" alt="Live video feed" />
            </div>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
