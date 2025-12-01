import cv2
import cvzone
from ultralytics import YOLO
import numpy as np
from keras.models import load_model
import tensorflow
import winsound
import threading
import time
from pyfirmata2 import Arduino, util     

PORT = 'COM4'
board = Arduino(PORT)

ledVerde = board.get_pin('d:3:o')
ledVermelho = board.get_pin('d:6:o')
ledVerde2 = board.get_pin('d:10:o')
ledVermelho2 = board.get_pin('d:11:o')
# Configuração da câmera 1
video = cv2.VideoCapture(0)
video.set(3,1280)
video.set(4,720)

# Configuração da câmera 2
video2 = cv2.VideoCapture(1)
video2.set(3,1280)
video2.set(4,720)

# Carrega o modelo YOLO
modelo = YOLO('yolov8n.pt') #n,s,m,l,x
modelo_emergencial = YOLO('./runs/detect/train/weights/best.pt')

controleAlarme = False

cronometroComCarro = 0
cronometroSemCarro = 0

cronometroComCarro2 = 0
cronometroSemCarro2 = 0

contador_carros = 0
contador_carros2 = 0

sinaleiraDireira = False
sinaleiraEsquerda = False
def alarme():
    global controleAlarme
    for _ in range(5):
        winsound.Beep(2500, 500)
        controleAlarme = False

while True:
    #CAMERA 1
    check, img = video.read()
    img = cv2.resize(img, (640, 360))

    resultado = modelo.predict(img, conf=0.5)
    contador_carros = 0   # contador por frame

    for objetos in resultado:
        obj = objetos.boxes

        for dados in obj:
            x, y, w, h = dados.xyxy[0]
            x, y, w, h = int(x), int(y), int(w), int(h)
            cls = int(dados.cls[0])

            # Caixa e alerta se for veículo (classe 2 = carro)
            if cls == 1 or cls == 2 or cls == 3 or cls == 5 or cls == 7 or cls == 17:
                cronometroComCarro += 1
                cronometroSemCarro = 0
                contador_carros += 1
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 5)

                if not controleAlarme:
                    controleAlarme = True
                    threading.Thread(target=alarme).start()
                
                resultado_emergencial = modelo_emergencial.predict(img, conf=0.5)

                for objetos_emergencial in resultado_emergencial:
                

        if contador_carros == 0:
            cronometroSemCarro += 1

        if cronometroSemCarro >= 20:
            cronometroComCarro = 0
        
        if cronometroComCarro >= 100 + 100*contador_carros and sinaleiraDireira == True:
            cronometroComCarro2 = 15
            cronometroComCarro = 0

    #cvzone.putTextRect(img, f"Veiculos detectados: { contador_carros }, {cronometroComCarro}", (50, 100), scale=2, thickness=2, colorR=(0, 0, 255))
    if ( cronometroComCarro >= 15 and sinaleiraEsquerda == False) or (cronometroSemCarro2 >=20 and contador_carros >=1):
        cvzone.putTextRect(img, f"Sinaleira aberta", (50, 50), scale=2, thickness=2, colorR=(0, 255, 0))
        ledVermelho.write(0)
        ledVerde.write(1)
        sinaleiraDireira = True
    else:
        cvzone.putTextRect(img, f"Sinaleira fechada", (50, 50), scale=2, thickness=2, colorR=(0, 0, 255))
        ledVerde.write(0)
        ledVermelho.write(1)
        sinaleiraDireira = False
    cv2.imshow('IMG', img)
    cv2.waitKey(1)


    #CAMERA 2
    check2, img2 = video2.read()
    img2 = cv2.resize(img2, (640, 360))

    resultado2 = modelo.predict(img2, conf=0.5)
    contador_carros2 = 0   # contador por frame

    for objetos in resultado2:
        obj = objetos.boxes

        for dados in obj:
            x, y, w, h = dados.xyxy[0]
            x, y, w, h = int(x), int(y), int(w), int(h)
            cls = int(dados.cls[0])

            # Caixa e alerta se for veículo (classe 2 = carro)
            if  cls == 1 or cls == 2 or cls == 3 or cls == 5 or cls == 7 or cls == 17:
                cronometroComCarro2 += 1
                cronometroSemCarro2 = 0
                contador_carros2 += 1
                cv2.rectangle(img2, (x, y), (w, h), (0, 0, 255), 5)
                if not controleAlarme:
                    controleAlarme = True
                    threading.Thread(target=alarme).start()

        if contador_carros2 == 0:
            cronometroSemCarro2 += 1

        if cronometroSemCarro2 >= 20:
            cronometroComCarro2 = 0
        
        if cronometroComCarro2 >= 100 + 100*contador_carros2 and sinaleiraEsquerda == True:
            cronometroComCarro = 15
            cronometroComCarro2 = 0

    # Mostra contador de objetos na tela
    #cvzone.putTextRect(img2, f"Veiculos detectados: { contador_carros2 }, {cronometroComCarro2}", (50, 100), scale=2, thickness=2, colorR=(0, 0, 255))
    if (cronometroComCarro2 >= 15 and sinaleiraDireira == False) or (cronometroSemCarro >=20 and contador_carros2 >= 1):
        cvzone.putTextRect(img2, f"Sinaleira aberta", (50, 50), scale=2, thickness=2, colorR=(0, 255, 0))
        ledVermelho2.write(0)
        ledVerde2.write(1)
        sinaleiraEsquerda = True
    else:
        cvzone.putTextRect(img2, f"Sinaleira fechada", (50, 50), scale=2, thickness=2, colorR=(0, 0, 255))
        ledVerde2.write(0)
        ledVermelho2.write(1)
        sinaleiraEsquerda = False

    cv2.imshow('IMG2', img2)
    cv2.waitKey(1)
