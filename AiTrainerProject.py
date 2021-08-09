from flask import Flask
import cv2
import numpy as np
import time
from dist import PoseModule as pm

app = Flask(__name__)
cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, frame = cap.read()

    """
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    """

    frame = cv2.resize(frame, (1200, 700))
    # frame = cv2.imread("AiTrainer/test.jpg")
    frame = detector.findPose(frame, False)
    lmList = detector.findPosition(frame, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(frame, 12, 14, 16)
        # # Left Arm
        #angle = detector.findAngle(frame, 11, 13, 15,False)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        # Draw Bar
        cv2.rectangle(frame, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(frame, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(frame, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(frame, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", frame)
    cv2.waitKey(1)

"""
@app.route('/')
def index():
    return render_template('python1.html')

@app.route("/video")
def video():
    return Response(main(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
"""