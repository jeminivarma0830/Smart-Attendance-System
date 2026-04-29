import face_recognition
import cv2
import os

name = input("Enter your name: ")

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    cv2.imshow("Register Face - Press 's' to save", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        file_path = f"faces/{name}.jpg"
        cv2.imwrite(file_path, frame)
        print("Face saved!")
        break

video.release()
cv2.destroyAllWindows()