import cv2


def takePhoto(id):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    sampleNum = 0
    take = False
    time = 0
    while (True):
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # incrementing sample number
            time=time+1
            # saving the captured face in the dataset folder
            if(time>10):
                sampleNum = (sampleNum + 1)
                cv2.imwrite("images/" + str(id) + '.' + str(sampleNum) + ".jpg", cv2.resize(gray[y:y + h, x:x + w],(280,280)))
            cv2.imshow('frame', img)

        # wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is more than 20
        elif sampleNum > 4:
            break
    cam.release()
    cv2.destroyAllWindows()
    return True