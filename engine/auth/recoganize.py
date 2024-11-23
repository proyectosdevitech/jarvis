import os
import cv2

def AuthenticateFace():

    flag = ""
    # Local Binary Patterns Histograms
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    trainer_path = os.path.join('engine', 'auth', 'trainer', 'trainer.yml')
    if not os.path.exists(trainer_path):
        print(f"Error: El modelo de entrenamiento no se encuentra en {trainer_path}")
        return 0
    recognizer.read(trainer_path)  # Load trained model

    cascade_path = os.path.join('engine', 'auth', 'haarcascade_frontalface_default.xml')
    if not os.path.exists(cascade_path):
        print(f"Error: El archivo de la cascada no se encuentra en {cascade_path}")
        return 0
    faceCascade = cv2.CascadeClassifier(str(cascade_path))

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type
    id = 2  # number of persons you want to Recognize
    names = ['', 'Digambar']  # names, leave first empty because counter starts from 0

    cam = cv2.VideoCapture(0)  # cv2.CAP_DSHOW to remove warning
    if not cam.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return 0
    cam.set(3, 640)  # set video FrameWidth
    cam.set(4, 480)  # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:

        ret, img = cam.read()  # read the frames using the above created object
        if not ret or img is None:
            print("Error: No se pudo leer la imagen desde la cámara.")
            break  # Salir si no se puede leer la imagen

        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])

            if accuracy < 100:
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 1
            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 0

            cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:  # Puedes reemplazar 27 con otro código de tecla si lo prefieres
            break
        if flag == 1:
            break

    # Clean up
    cam.release()
    cv2.destroyAllWindows()
    return flag
