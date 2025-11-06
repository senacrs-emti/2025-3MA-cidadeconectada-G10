import cv2
import cvzone
from ultralytics import YOLO
import winsound
import threading

# Configuração da câmera
video = cv2.VideoCapture(1)
video.set(3,1280)
video.set(4,720)

# Carrega o modelo YOLO
modelo = YOLO('yolov8n.pt')

controleAlarme = False

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
            if cls == 2:
                contador_carros += 1
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 5)
                cvzone.putTextRect(img, "VEÍCULO IDENTIFICADO", (105, 65), colorR=(0, 0, 255))
                if not controleAlarme:
                    controleAlarme = True
                    threading.Thread(target=alarme).start()

    # Mostra contador de objetos na tela
    cvzone.putTextRect(img, f"Objetos detectados: { contador_carros }", (50, 650), scale=2, thickness=2, colorR=(0, 255, 0))

    cv2.imshow('IMG', img)
    cv2.waitKey(1)
