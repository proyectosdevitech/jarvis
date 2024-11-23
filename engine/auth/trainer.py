import cv2
import numpy as np
from PIL import Image #pillow package
import os
from pathlib import Path

path = 'engine\\auth\\samples' # Path for samples already taken

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
cascade_path = Path('engine') / 'auth' / 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(str(cascade_path))
#Haar Cascade classifier is an effective object detection approach


def Images_And_Labels(path): # function to fetch the images and labels

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []

    for imagePath in imagePaths: # to iterate particular image path

        gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_arr = np.array(gray_img,'uint8') #creating an array

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            faceSamples.append(img_arr[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("Training faces. It will take a few seconds. Wait ...")

faces,ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

# Define la ruta del archivo de salida de manera compatible con ambos sistemas operativos
trainer_path = Path('engine') / 'auth' / 'trainer' / 'trainer.yml'

# Guardar el modelo entrenado
recognizer.write(str(trainer_path))  # Convertir el Path a string

print("Model trained, Now we can recognize your face.")