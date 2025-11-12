import cv2
import cvzone
from ultralytics import YOLO
import winsound
import threading
import time
from pyfirmata2 import Arduino, util

PORT = 'COM4'  # Detecta automaticamente a porta (ex: COM4)
board = Arduino(PORT)

ledVerde = board.get_pin('d:3:o')
ledVermelho = board.get_pin('d:6:o')

# Configuração da câmera
video = cv2.VideoCapture(0)

video.set(3,1280)
video.set(4,720)

# Carrega o modelo YOLO
modelo = YOLO('yolov8n.pt')

controleAlarme = False

cronometroComCarro = 0
cronometroSemCarro = 0

def alarme():
    global controleAlarme
    for _ in range(5):
        winsound.Beep(2500, 500)
        controleAlarme = False

while True:
    check, img = video.read()
    img = cv2.resize(img, (1280, 720))

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

            if cls != 1 or cls != 2 or cls != 3 or cls != 5 or cls != 7 or cls != 17:
                cronometroSemCarro += 1

        if contador_carros == 0:
            cronometroSemCarro += 1

        if cronometroSemCarro >= 20:
            cronometroComCarro = 0
        
        if cronometroComCarro >= 200:
            cronometroComCarro = 0

    # Mostra contador de objetos na tela
    cvzone.putTextRect(img, f"Veiculos detectados: { contador_carros }, {cronometroComCarro}", (50, 650), scale=2, thickness=2, colorR=(0, 0, 255))
    if cronometroComCarro >= 100:
        cvzone.putTextRect(img, f"Sinaleira aberta", (50, 100), scale=2, thickness=2, colorR=(0, 255, 0))
        ledVermelho.write(0)
        ledVerde.write(1)
    else:
        cvzone.putTextRect(img, f"Sinaleira fechada", (50, 100), scale=2, thickness=2, colorR=(0, 0, 255))
        ledVerde.write(0)
        ledVermelho.write(1)
    cv2.imshow('IMG', img)
    cv2.waitKey(1)
