import os
import time
import sys
import queue
import cv2 as cv
import numpy as np
import face_recognition
from multiprocessing import Process
import multiprocessing

def update_frame(rtsp_url,q):
    print('Connecting to video ...')
    # set rtsp protocol path
    cap = cv.VideoCapture(rtsp_url)
    print('Connected')
    while cap.isOpened():
        # print('Reading frame ...')
        ret, current_frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print('Can\'t receive frame (stream end?). Exiting ...')
            continue
        if not q.empty():
            try:
                q.get_nowait()   # discard previous (unprocessed) frame
            except queue.Empty:
                pass
        q.put(current_frame)
    cap.release()

def main(q):
    source_path = sys.argv[2]
    source_face_encodings = []
    # cache source face encoding to memory
    for file_name in os.listdir(source_path):
        file_path = source_path + file_name
        source_face_encodings += face_recognition.face_encodings(face_recognition.load_image_file(file_path))
    print('source face encoded')
    while True:
        frame = q.get()
        print('Get frame')
        face_encodings = face_recognition.face_encodings(frame)
        print('Face encoded')
        print(face_encodings)
        for face_encoding in face_encodings:
            print('Face comparing ...')
            compare_results = face_recognition.compare_faces(source_face_encodings, face_encoding)
            if np.any(compare_results) == True:
                print('Face recognition success')
                break

if __name__ == "__main__":
    _queue = multiprocessing.Queue()
    p = Process(target=update_frame, args=(sys.argv[1],_queue,))
    p.start()
    main(_queue)