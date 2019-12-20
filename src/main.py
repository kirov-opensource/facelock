import os
import sys
import cv2 as cv
import numpy as np
import face_recognition


def main():
    # set rtsp protocol path
    cap = cv.VideoCapture(sys.argv[1])
    source_path = sys.argv[2]
    source_face_encodings = []
    # cache source face encoding to memory
    for file_name in os.listdir(source_path):
        file_path = source_path + file_name
        np.concatenate((source_face_encodings, face_recognition.load_image_file(file_path)), axis = 0)

    while cap.isOpened():
        print('Reading frame ...')
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        print('Read frame success')
        print('Finding face ...')
        face_locations = face_recognition.face_locations(frame)
        print(face_locations)
        print('Face encoding ...')
        face_encodings = face_recognition.face_encodings(frame)
        print('Face encoded')
        print('Face quantity ' + np.size(face_encodings, 0))
        compare_flag = False
        for face_encoding in face_encodings:
            print('Face comparing ...')
            compare_results = face_recognition.compare_faces(source_face_encodings, face_encoding)
            for compare_result in compare_results:
                if compare_result == True:
                    compare_flag = True
                    print('Face recognition success')
                    break
            if compare_flag == True:
                break
    cap.release()

if __name__ == "__main__":
    main()