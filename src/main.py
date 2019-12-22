import os
import sys
import _thread as thread
import cv2 as cv
import numpy as np
import face_recognition

frame = None
lock = False

def update_frame(rtsp_url):
    print('Connecting to video ...')
    # set rtsp protocol path
    cap = cv.VideoCapture(rtsp_url)
    print('Connected')
    while cap.isOpened():
        print('Reading frame ...')
        ret, current_frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if lock == True:
            continue
        frame = current_frame
    cap.release()

def main():
    thread.start_new_thread(update_frame, (sys.argv[1],) )
    source_path = sys.argv[2]
    source_face_encodings = []
    # cache source face encoding to memory
    for file_name in os.listdir(source_path):
        file_path = source_path + file_name
        source_face_encodings += face_recognition.face_encodings(face_recognition.load_image_file(file_path))
    while True:
        lock = True
        face_encodings = face_recognition.face_encodings(frame)
        lock = False
        print('Face encoded')
        print(face_encodings)
        for face_encoding in face_encodings:
            print('Face comparing ...')
            compare_results = face_recognition.compare_faces(source_face_encodings, face_encoding)
            if np.any(compare_results) == True:
                print('Face recognition success')
                break

if __name__ == "__main__":
    main()