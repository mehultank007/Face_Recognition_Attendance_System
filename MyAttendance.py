import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime 
import pyttsx3 as textSpeach
from connection import *

# engine = textSpeach.init()

video_capture = cv2.VideoCapture(0)

jobs_img = face_recognition.load_image_file("student_images/Mehul_Tank.jpg")
jobs_encoding = face_recognition.face_encodings(jobs_img)[0]

dmt_img = face_recognition.load_image_file("student_images/Dharmik_Thanki.jpg")
dmt_encoding = face_recognition.face_encodings(dmt_img)[0]

vipul_img = face_recognition.load_image_file("student_images/Vipul_Khunti.jpeg")
vipul_encoding = face_recognition.face_encodings(vipul_img)[0]

known_face_enc = [
    jobs_encoding,
    dmt_encoding,
    vipul_encoding
]

known_face_names = [
    "Mehul Tank",
    "Dharmik Thanki",
    "Vipul Khunti"
]
student = known_face_names.copy()

face_loc = []
face_enc = []
face_name = []
s = True

now = datetime.now()
current_dt = now.strftime("%d-%m-%Y")

# f = open(current_dt+'.csv','w+',newline= '')
# lnwriter = csv.writer(f)

while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_loc = face_recognition.face_locations(rgb_small_frame)
        face_enc = face_recognition.face_encodings(rgb_small_frame,face_loc)
        face_names = []
        for fc in face_enc:  
            matches = face_recognition.compare_faces(known_face_enc,fc)
            name = ""
            face_distance = face_recognition.face_distance(known_face_enc,fc)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)
            # if name in known_face_names:
            if name in student:
                student.remove(name)
                print(student)
                                        # current_time = now.strftime("%H-%M-%S")
                        # lnwriter.writerow([name,current_time])
                    # Database code
                # var = "INSERT INTO students (stname,stclass,stdate)  VALUES (?,?,?);"
                # cur.execute(var,(name,arg3,current_dt))

                    # engine.say("Welcome to class" + name)
                    # engine.runAndWait()
    cv2.imshow("attendence System",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
# f.close()
conn.commit()
conn.close()