import cv2 as cv
import face_recognition

cap = cv.VideoCapture('rtsp://player.daniulive.com:554/live20656.sdp')
my_face_encodings = face_recognition.load_image_file("./source/wangshenjie_idcard.jpg")

while cap.isOpened():
    print('Reading frame ...')
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    print('Read frame success')
    print('Face encoding ...')
    face_encodings = face_recognition.face_encodings(image)
    print('Face encoded')
    print('Face quantity ' + face_encodings.length)
    for face_encoding in face_encodings:
        compare_flag = False
        print('Face comparing ...')
        compare_results = face_recognition.compare_faces(my_face_encodings, face_encoding)
        for compare_result in compare_results:
            if compare_result == True:
                compare_flag = True
                print('Face recognition success')
                break
        if compare_flag == True:
            break
cap.release()