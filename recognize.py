import face_recognition
import cv2
import os
import pandas as pd
from datetime import datetime

known_encodings = []
known_names = []

# Load faces
for file in os.listdir("faces"):
    img = face_recognition.load_image_file(f"faces/{file}")
    encoding = face_recognition.face_encodings(img)[0]
    known_encodings.append(encoding)
    known_names.append(file.split(".")[0])

video = cv2.VideoCapture(0)

def mark_attendance(name):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    date = now.strftime("%Y-%m-%d")

    df = pd.DataFrame([[name, date, time]],
                      columns=["Name", "Date", "Time"])

    if not os.path.exists("attendance.csv"):
        df.to_csv("attendance.csv", index=False)
    else:
        df.to_csv("attendance.csv", mode='a', header=False, index=False)

while True:
    ret, frame = video.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for encoding, face in zip(encodings, faces):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
            mark_attendance(name)

        top, right, bottom, left = face
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()