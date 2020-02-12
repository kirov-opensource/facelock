import os
import time
import sys
import cv2 as cv
import numpy as np
import face_recognition
import multiprocessing
import gpiozero

def updateframe(rtsp_url,lock):
    print('connecting to video ...')
    # set rtsp protocol path
    cap = cv.VideoCapture(rtsp_url)
    print('connected')
    while cap.isOpened():
        # print('Reading frame ...')
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print('can\'t receive frame (stream end?). exiting ...')
            continue
        lock.acquire()
        cv.imwrite('./temp.jpg', frame)
        lock.release()
    print('connection error. exiting ...')
    cap.release()

def main(lock,source_face_encodings):
    gpio21 = gpiozero.LED(21)
    while True:
        lock.acquire()
        frame = face_recognition.load_image_file('./temp.jpg')
        lock.release()
        face_encodings = face_recognition.face_encodings(frame)
        # print('Face encoded')
        for face_encoding in face_encodings:
            print('face comparing ...')
            compare_results = face_recognition.compare_faces(source_face_encodings, face_encoding)
            if np.any(compare_results) == True:
                print('face recognition success')
                gpio21.on()
                print('lock opened')
                time.sleep(2)
                print('lock closed')
                break

if __name__ == "__main__":
    source_path = sys.argv[1]
    source_face_encodings = []
    # cache source face encoding to memory
    for file_name in os.listdir(source_path):
        file_path = source_path + file_name
        source_face_encodings += face_recognition.face_encodings(face_recognition.load_image_file(file_path))
    print('source face encoded')
    lock = multiprocessing.Lock()
    p = multiprocessing.Process(target=updateframe, args=(sys.argv[2],lock,))
    p.start()
    main(lock, source_face_encodings)