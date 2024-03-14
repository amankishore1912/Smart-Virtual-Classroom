import cv2
import sys
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from flask import Flask, render_template, Response
# import tensorflow as tf

sys.stdout = open(os.devnull, 'w')
sys.stdout = sys.__stdout__

from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)


facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('data/trainer.yml')
# cascadePath = "data/haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)

names = np.unique(LABELS)
label_map = {index: label for index, label in enumerate(names)}

COL_NAMES = ['NAME', 'TIME']

def generate_frames():
    video=cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, ((x),(y)), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                if (100-confidence)>55:
                    confidence = "  {0}%".format(round(100 - confidence))
                    output = label_map[id]
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
                    cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
                    cv2.putText(frame, ((output) + confidence), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    video.release()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_attendance', methods=['POST'])
def take_attendance():
    video=cv2.VideoCapture(0)
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    flag = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, ((x),(y)), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        if (100-confidence)>55:
            output = label_map[id]
            ts=time.time()
            date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            exist=os.path.isfile("Attendance/Attendance_" + date + ".csv")
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(300,300,255),2)
            cv2.rectangle(frame,(x,y-40),(x+w,y),(300,300,255),-1)
            cv2.putText(frame, str(output), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (300,300,255), 1)
            attendance=[str(output), str(timestamp)]

            speak(f"Attendance of {output} Taken..")
            flag = 1
            if exist:
                with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(attendance)
                csvfile.close()
            else:
                with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
                csvfile.close()
        else:
            print("Face not Recognised.. ")
    if(not flag):
       print("Face not Recognised.. ") 
       video.release()
       return render_template('index.html')
    
    video.release()
    return "<html> <body> <h3>Attendence Taken Successfully... <br> Close this window </h3> </body> </html>"

if __name__ == '__main__':
    app.run(debug=True)