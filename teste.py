from pyfirmata2 import Arduino, util

PORT = Arduino.AUTODETECT  # Detecta automaticamente a porta (ex: COM4)
board = Arduino(PORT)

# Define o pino 10 como saída digital
led = board.get_pin('d:5:o')

# Acende o LED
led.write(1)

input("Pressione Enter para desligar e sair...")

# Desliga o LED antes de sair
led.write(0)
board.exit()

