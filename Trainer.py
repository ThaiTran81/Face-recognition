import cv2, os
import numpy as np
from PIL import Image

#Takes in the number of components for the PCA for crating Eigenfaces. OpenCV documentation mentions
recognizer = cv2.face.EigenFaceRecognizer_create()



detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def train():
    path="images"
    def getImageWithID(path):
        width_d, height_d = 280, 280
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        IDs = []

        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L');
            faceNp = np.array(faceImg, 'uint8')
            faces = detector.detectMultiScale(faceNp)

            ID = int(os.path.split(imagePath)[-1].split('.')[0])
            for (x, y, w, h) in faces:
                faceSamples.append(cv2.resize(faceNp[y:y+h,x:x+w], (width_d, height_d)))
                IDs.append(ID)

        return IDs, faceSamples


    Ids, faces = getImageWithID(path)
    recognizer.train(faces, np.array(Ids))
    recognizer.write('trainningData.yml')
    cv2.destroyAllWindows()