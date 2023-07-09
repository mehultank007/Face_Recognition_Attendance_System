import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from connection import *

path = 'student_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList =[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('dance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            print(name)
            datastore(name,f) 
    f.close()

    
def ser(s):

    tString = datetime.now()
    if (tString.hour >= 8 and tString.minute >= 45) and (tString.hour <= 9 and tString.minute <= 30):
        var = "INSERT INTO cs (stid,stdate) VALUES (?,?);"
        cur.execute(var,(s, current_dt))

    elif (tString.hour >= 9 and tString.minute >= 30) and (tString.hour <= 10 and tString.minute <= 15):
        var = "INSERT INTO java (stid,stdate) VALUES (?,?);"
        cur.execute(var,(s, current_dt))

    elif (tString.hour >= 10 and tString.minute >= 15) and (tString.hour <= 11 and tString.minute <= 5):
        var = "INSERT INTO sad (stid,stdate) VALUES (?,?);"
        cur.execute(var,(s, current_dt))

    elif (tString.hour >= 11 and tString.minute >= 25) and (tString.hour <= 12 and tString.minute <= 15):
        var = "INSERT INTO os (stid,stdate) VALUES (?,?);"
        cur.execute(var,(s, current_dt))

    elif (tString.hour >= 5 and tString.minute >= 5):
        var = "INSERT INTO os (stid,stdate) VALUES (?,?);"
        cur.execute(var,(s, current_dt))

    else:
        print("Plese try again Tomorrow")

def datastore(name,f):
    time_now = datetime.now()
    tiString = time_now.strftime('%H:%M:%S')
    dString = time_now.strftime('%d/%m/%Y')
    f.writelines(f'\n{name},{tiString},{dString}')

    # var = "INSERT INTO students (stname,stclass)  VALUES (?,?);"
    # cur.execute(var,(name,arg3))
    
    for s in conn.execute("select stid from students where stname='"+name+"'"):
        s = str(s).replace('()','').replace(',','')
        print(s)
        ser(s)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    cv2.imshow('webcam', img)
    # if cv2.waitKey(10) == 13:
        # break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        file = open('dance.csv','w')
        file.truncate()
        file.close()
        break

#  To fetch the data from the table os
# i = input("Enter student id : ")
# for s in conn.execute("select * from os where stid='("+i+")'"):
    # print(s)

cap.release()
cv2.destroyAllWindows()
conn.commit()
conn.close()