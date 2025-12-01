🚦 Sinaleira Inteligente com Visão Computacional

Este projeto implementa um sistema de controle inteligente de sinaleiras (semáforos) utilizando visão computacional e modelos de detecção de objetos.
O objetivo é tornar o fluxo de trânsito mais eficiente ao metrificar o número de veículos em cada via para ajustar o tempo de abertura dos semáforos de forma dinâmica, além de priorizar veículos emergenciais, como:

🚑 Ambulâncias
🚓 Viaturas policiais
🚒 Caminhões de bombeiro

<hr>

🧠 Como funciona

O sistema utiliza um modelo YOLO treinado para detectar:

carros
motos
caminhões
ônibus
cavalos
veículos emergenciais

A cada quadro da câmera, o sistema:
📸 Captura a imagem do cruzamento
🔍 Detecta e conta todos os veículos por faixa/direção
🚨 Identifica veículos emergenciais
⏱️ Calcula o tempo ideal de abertura de cada sinal
🟢 Troca a sinaleira de acordo com a decisão inteligente

<hr>

⚙️ Tecnologias utilizadas

Python
YOLOv8 / Ultralytics
OpenCV
Numpy
Arduino

<hr>

▶️ Como rodar o projeto

1. Clone o repositório

*codigo de clonar

2. Instale as dependências

pip install -r requirements.txt *preencher

3. Execute o sistema

python src/deteccao.py

<hr>

📈 Benefícios do sistema

Redução de filas em horários de pico
Priorização em situações críticas
Otimização de tráfego sem intervenção humana
Operação contínua e autônoma
Pode substituir ou complementar sistemas tradicionais de sensores no solo

👨‍💻 Autor

Projeto desenvolvido por:
Felipe da Silva Rieger *Linkedin
João Pedro de Oliveira Cidade *Linkedin
Matheus Amaro Vettorazi *Linkedin



