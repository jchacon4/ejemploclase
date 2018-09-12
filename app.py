import face_recognition
import cv2
import requests



video_capture = cv2.VideoCapture(0)

#lo que tienen que cambiar empieza aqui

# registrar cara de persona 1
alguien_image = face_recognition.load_image_file("alguien3.jpg")
alguien_face_encoding = face_recognition.face_encodings(alguien_image)[0]

# registrar cara de persona 2
alguien2_image = face_recognition.load_image_file("alguien2.jpg")
alguien2_face_encoding = face_recognition.face_encodings(alguien2_image)[0]

# Crear lista de personas con nombre
known_face_encodings = [
    alguien_face_encoding,
    alguien2_face_encoding
]
known_face_names = [
    "alguien1",
    "alguien2"
]


#lo que tienen que cambiar termina aqui


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "nadie"
            data = '{"who":"%s"}' % name
            response = requests.patch('https://caraudem.firebaseio.com/.json', data=data)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                data = '{"who":"%s"}' % name
                response = requests.patch('https://caraudem.firebaseio.com/.json', data=data)
            face_names.append(name)
    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
