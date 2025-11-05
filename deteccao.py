import cv2
import cvzone
from ultralytics import YOLO
import winsound
import threading

video = cv2.VideoCapture(0)
video.set(3,1280)
video.set(4,720)

modelo = YOLO('yolov8n.pt')
#yolov8n (n = nano; mais leve, mas menos acertivo)
#yolov8x (x; mais pesado, mas mais acertivo)

controleAlarme = False

def alarme():
    global controleAlarme
    for _ in range(5):
        winsound.Beep(2500,500)

    controleAlarme = False

while True:
    check,img = video.read()
    img = cv2.resize(img,(1280,720))

    resultado = modelo.predict(img,conf=0.5)

    for objetos in resultado:
        obj = objetos.boxes
        for dados in obj:
            #bbox
            x,y,w,h = dados.xyxy[0]
            x, y, w, h = int(x),int(y),int(w),int(h)
            cls = int(dados.cls[0])
            print(x,y,w,h,cls)
            if cls==0:
                cv2.rectangle(img,(x,y),(w,h),(0,0,255),5)
                cvzone.putTextRect(img,"PESSOA IDENTIFICADA",(105,65),colorR=(0,0,255))
                if not controleAlarme:
                    controleAlarme =True
                    threading.Thread(target=alarme).start()

    cv2.imshow('IMG',img)
    cv2.waitKey(1)