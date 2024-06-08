from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
camera.start()

def generate_frames():
    while True:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
        res, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ANEMA - LIVE CAM</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url("https://img.lovepik.com/photo/48013/0603.jpg_wh860.jpg");
                background-size: cover;
                background-position: center;
                color: white;
            }
            .container {
                text-align: center;
                background: #769126;
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
                border-radius: 15px;
                display: block;
                width: 100%;
                height: auto;
            }
            .time {
                color: red;
                }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-container" style="position: absolute;">
                <img src="{{ url_for('static', filename='/logo.png') }}" alt="Logo" style="position: relative; top:-33px; width: 230px;"/>
            </div>
            <div class="clock" id="clock"></div>
            <div class="title">LIVE CAM</div>
            <div class="video-container">
                <img src="{{ url_for('video_feed') }}" alt="Live video feed" />
            </div>
        </div>
        <script>
            function updateClock() {
                var now = new Date();
                var year = now.getFullYear();
                var month = (now.getMonth() + 1).toString().padStart(2, '0');
                var day = now.getDate().toString().padStart(2, '0');
                var hours = now.getHours().toString().padStart(2, '0');
                var minutes = now.getMinutes().toString().padStart(2, '0');
                var seconds = now.getSeconds().toString().padStart(2, '0');
                var dateString = year + '-' + month + '-' + day;
                var timeString = '<span class="time">' + hours + ':' + minutes + ':' + seconds + '</span>';
                document.getElementById('clock').innerHTML = dateString + ' ' + timeString;
            }
            setInterval(updateClock, 1000);
            updateClock();  // initial call
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
