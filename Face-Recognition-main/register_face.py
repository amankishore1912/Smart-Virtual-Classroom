import cv2
import pickle
import numpy as np
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces_data=[]
lables = []

i=0
x = 0
print("Register Face (1: YES / 0: NO): ")
x = int(input("Press 1 to Register Face"))
if(x):
    name=input("Enter Your Name: ")
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    
    while True:
        ret,frame=video.read()
        frame = cv2.flip(frame, 1)
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=facedetect.detectMultiScale(gray, 1.3 ,5)
        for (x,y,w,h) in faces:
            crop_img=gray[y:y+h, x:x+w]
            crop_img=cv2.resize(crop_img, (300,300))
            img_numpy = np.array(crop_img,'uint8')
            if len(faces_data)<=100 and i%10==0:
                faces_data.append(img_numpy)
                lables.append(name)
            i=i+1
            cv2.putText(frame, str(len(faces_data)), (300,300), cv2.FONT_HERSHEY_COMPLEX, 1, (300,300,255), 1)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (300,300,255), 1)
        cv2.imshow("Frame",frame)
        k=cv2.waitKey(1)
        if k==ord('q') or len(faces_data)==100:
            break
    video.release()
    cv2.destroyAllWindows()

    print("\n [INFO] Face data collected...")



    if 'names.pkl' not in os.listdir('data/'):
        with open('data/names.pkl', 'wb') as f:
            pickle.dump(lables, f)
    else:
        with open('data/names.pkl', 'rb') as f:
            names=pickle.load(f)
        names=names+lables
        with open('data/names.pkl', 'wb') as f:
            pickle.dump(names, f)

    if 'faces_data.pkl' not in os.listdir('data/'):
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces_data, f)
    else:
        with open('data/faces_data.pkl', 'rb') as f:
            faces=pickle.load(f)
        faces=faces + faces_data
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces, f)


with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)



names = np.unique(LABELS)

label_map = {label: index for index, label in enumerate(names)}

encoded_labels = [label_map[label] for label in LABELS]
encoded_labels = np.array(encoded_labels)


print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")

recognizer.train(FACES, encoded_labels)
# Save the model into trainer/trainer.yml
recognizer.write('Data/trainer.yml') 
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(encoded_labels))))