import cv2
import numpy as np



####font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
def detect():
    targetName = list()
    path = 'data.txt'
    result=""
    with open('data.txt', 'r',encoding="utf8") as f:
        targetName = [line.strip() for line in f]
    def find(str):
        for i in range(len(targetName)):
            if targetName[i].find(str) != -1:
                return targetName[i]
        return None
    recog = cv2.face.EigenFaceRecognizer_create()
    recog.read('trainningData.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceDetect = cv2.CascadeClassifier(cascadePath);

    cam = cv2.VideoCapture(0)
    id = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            id, conf = recog.predict(cv2.resize(gray[y:y + h, x:x + w],(280,280)))
            result = find(str(id))
            print(conf)
            if result != None and conf < 6900:
                id="accepted"
            else:
                id = "denied"
            ##        cv2.putText(img, str(id),(x,y+h),font,255,1)
            cv2.putText(img, str(id), (x, y + h), font, 0.55, (0, 255, 0), 1)
        cv2.imshow('Face', img)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()