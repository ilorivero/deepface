# ==============================================================================
# ALGORITMO DE RECONHECIMENTO FACIAL COM DEEPFACE
# ==============================================================================
# Este programa implementa um sistema de reconhecimento facial em tempo real
# que analisa características como idade, gênero, emoção e etnia usando a
# biblioteca DeepFace em conjunto com OpenCV e Flask.
#
# SOBRE O DEEPFACE:
# O DeepFace é uma biblioteca de deep learning que utiliza redes neurais
# convolucionais (CNNs) pré-treinadas para análise facial. Originalmente
# desenvolvido pelo Facebook, implementa vários modelos estado-da-arte:
#
# • VGG-Face: Para reconhecimento e verificação facial
# • OpenFace: Para embeddings faciais 
# • FaceNet: Para representação facial em espaço vetorial
# • DeepID: Para identificação facial
# • Emotion models: Para classificação de emoções (7 categorias básicas)
# • Age/Gender models: Para estimativa de idade e classificação de gênero
# • Race models: Para classificação étnica
#
# FUNCIONAMENTO DO ALGORITMO:
# 1. Captura de vídeo em tempo real da webcam
# 2. Detecção de rostos usando Haar Cascade (OpenCV)
# 3. Extração da região facial para cada rosto detectado
# 4. Pré-processamento da imagem (normalização, redimensionamento)
# 5. Análise através das redes neurais do DeepFace
# 6. Pós-processamento e mapeamento dos resultados
# 7. Exibição em interface web em tempo real
#
# DEPENDÊNCIAS NECESSÁRIAS:
# pip install deepface opencv-python flask tensorflow
#
# AUTOR: [Seu nome]
# DATA: Setembro 2025
# ==============================================================================

# 1. IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
# ==============================================================================
import atexit
import base64
import logging
import os
import platform
import sys
import time

import cv2
import numpy as np
from deepface import DeepFace
from flask import Flask, Response, jsonify, render_template_string, request

# 2. INICIALIZAÇÃO DA APLICAÇÃO FLASK
# ==============================================================================
app = Flask(__name__)  # Cria a instância da aplicação web

# Configuração simples de logs
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# 3. TEMPLATE HTML DA INTERFACE WEB
# ==============================================================================
# Este template define a interface web que exibirá o vídeo em tempo real
# e as informações analisadas sobre o rosto detectado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Análise Facial em Tempo Real</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; padding: 20px; }
        h1 { color: #333; }

        .container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .video-container, .upload-container {
            border: 3px solid #333;
            padding: 5px;
            background-color: white;
            min-height: 370px;
        }

        .video-container img, .upload-container img {
            width: 640px;
            max-width: 90vw;
            height: auto;
            background: #111;
        }

        .mode-buttons {
            margin-bottom: 10px;
        }

        .mode-buttons button {
            border: none;
            border-radius: 6px;
            padding: 10px 14px;
            cursor: pointer;
            margin: 0 5px;
            background: #d5d5d5;
            font-weight: bold;
        }

        .mode-buttons button.active {
            background: #333;
            color: white;
        }

        .hidden {
            display: none;
        }

        .info-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        #info {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            text-align: left;
            width: 250px;
            font-size: 18px;
        }

        #info p {
            margin: 10px 0;
            font-weight: bold;
        }

        .logo {
            width: 150px;
            margin-bottom: 10px;
        }

        #upload-form {
            margin-top: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 250px;
        }

        #upload-form button {
            border: none;
            border-radius: 8px;
            padding: 10px;
            background: #333;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        #status {
            min-height: 20px;
            font-size: 14px;
            color: #222;
        }

    </style>
    <script>
        let currentMode = 'webcam';

        function setMode(mode) {
            currentMode = mode;
            const webcamView = document.getElementById('webcam-view');
            const uploadView = document.getElementById('upload-view');
            const webcamButton = document.getElementById('mode-webcam');
            const uploadButton = document.getElementById('mode-upload');

            if (mode === 'webcam') {
                webcamView.classList.remove('hidden');
                uploadView.classList.add('hidden');
                webcamButton.classList.add('active');
                uploadButton.classList.remove('active');
            } else {
                webcamView.classList.add('hidden');
                uploadView.classList.remove('hidden');
                webcamButton.classList.remove('active');
                uploadButton.classList.add('active');
            }
        }

        function updateAttributes() {
            fetch('/attributes')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("age").innerText = "Idade: " + data.age;
                    document.getElementById("gender").innerText = "Gênero: " + data.gender;
                    document.getElementById("emotion").innerText = "Emoção: " + data.emotion;
                    document.getElementById("ethnicity").innerText = "Etnia: " + data.ethnicity;
                });
        }

        function uploadFile(event) {
            event.preventDefault();
            const fileInput = document.getElementById('image-file');
            const status = document.getElementById('status');
            const preview = document.getElementById('upload-preview');

            if (!fileInput.files || fileInput.files.length === 0) {
                status.innerText = 'Selecione um arquivo de imagem.';
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            status.innerText = 'Analisando arquivo...';

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json().then(data => ({ ok: response.ok, data })))
            .then(({ ok, data }) => {
                if (!ok) {
                    status.innerText = data.error || 'Falha no upload.';
                    return;
                }

                status.innerText = data.message;
                document.getElementById("age").innerText = "Idade: " + data.attributes.age;
                document.getElementById("gender").innerText = "Gênero: " + data.attributes.gender;
                document.getElementById("emotion").innerText = "Emoção: " + data.attributes.emotion;
                document.getElementById("ethnicity").innerText = "Etnia: " + data.attributes.ethnicity;

                if (data.preview) {
                    preview.src = 'data:image/jpeg;base64,' + data.preview;
                }
            })
            .catch(() => {
                status.innerText = 'Erro ao enviar arquivo.';
            });
        }

        window.onload = function() {
            setMode('webcam');
            updateAttributes();
            setInterval(updateAttributes, 1000);
            document.getElementById('upload-form').addEventListener('submit', uploadFile);
        };
    </script>
</head>
<body>
    <h1>Análise Facial em Tempo Real</h1>

    <div class="mode-buttons">
        <button id="mode-webcam" type="button" class="active" onclick="setMode('webcam')">Webcam</button>
        <button id="mode-upload" type="button" onclick="setMode('upload')">Upload de Arquivo</button>
    </div>
    
    <div class="container">
        <div id="webcam-view" class="video-container">
            <img src="/video_feed" alt="Stream da webcam">
        </div>

        <div id="upload-view" class="upload-container hidden">
            <img id="upload-preview" alt="Preview do arquivo analisado">
        </div>

        <div class="info-container">
            <img src="{{ url_for('static', filename='icei.png') }}" alt="Logomarca ICEI" class="logo">
            <div id="info">
                <p id="age">Idade: ?</p>
                <p id="gender">Gênero: ?</p>
                <p id="emotion">Emoção: ?</p>
                <p id="ethnicity">Etnia: ?</p>
            </div>

            <form id="upload-form" enctype="multipart/form-data">
                <input id="image-file" type="file" name="file" accept="image/*">
                <button type="submit">Enviar e analisar</button>
                <p id="status"></p>
            </form>
        </div>
    </div>
</body>
</html>
"""

# 4. INICIALIZAÇÃO DOS COMPONENTES DE VISÃO COMPUTACIONAL
# ==============================================================================
def open_camera():
    preferred_backends = []
    current_system = platform.system().lower()

    if current_system == "darwin":
        preferred_backends = [cv2.CAP_AVFOUNDATION]
    elif current_system == "windows":
        preferred_backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF]
    else:
        preferred_backends = [cv2.CAP_V4L2]

    for camera_index in (0, 1, 2):
        for backend in preferred_backends + [None]:
            cam = cv2.VideoCapture(camera_index) if backend is None else cv2.VideoCapture(camera_index, backend)
            if cam.isOpened():
                return cam
            cam.release()

    return None


cap = open_camera()
camera_available = cap is not None

# Carrega o classificador Haar Cascade para detecção de rostos
# Este é um classificador pré-treinado que detecta rostos frontais em imagens
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 5. VARIÁVEL GLOBAL PARA ARMAZENAR OS ÚLTIMOS ATRIBUTOS ANALISADOS
# ==============================================================================
# Esta variável mantém os dados mais recentes da análise facial
# para serem exibidos na interface web
latest_attributes = {"age": "?", "gender": "?", "emotion": "?", "ethnicity": "?"}

emotion_map = {
    "angry": "Zangado",
    "disgust": "Nojo",
    "fear": "Medo",
    "happy": "Feliz",
    "neutral": "Neutro",
    "sad": "Triste",
    "surprise": "Surpresa"
}

ethnicity_map = {
    "white": "Branco",
    "black": "Negro",
    "asian": "Asiático",
    "indian": "Indiano",
    "middle eastern": "Oriente Médio",
    "latino hispanic": "Latino/Hispânico"
}


def release_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None


atexit.register(release_camera)


def log_startup(host, port):
    separator = "=" * 60
    logging.info(separator)
    logging.info("Sistema de Reconhecimento Facial iniciado")
    logging.info("SO: %s", platform.platform())
    logging.info("Python: %s", sys.version.split()[0])
    logging.info("Diretório: %s", os.getcwd())
    logging.info("Webcam disponível: %s", "sim" if camera_available else "não")
    logging.info("Rodando em: http://%s:%s", host, port)
    logging.info("Pressione Ctrl+C para encerrar")
    logging.info(separator)


def build_placeholder_frame(message):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(frame, message, (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()

# 6. FUNÇÃO PRINCIPAL DE ANÁLISE FACIAL
# ==============================================================================
def analyze_face(frame):
    """
    Esta função realiza a análise facial completa de um frame de vídeo.
    
    Processo:
    1. Detecta rostos no frame usando Haar Cascade
    2. Para cada rosto encontrado, extrai a região facial
    3. Aplica o DeepFace para analisar atributos (idade, gênero, emoção, etnia)
    4. Desenha um retângulo verde ao redor do rosto detectado
    5. Atualiza a variável global com os resultados
    
    Args:
        frame: Frame de vídeo capturado da webcam
        
    Returns:
        frame: Frame processado com retângulos desenhados nos rostos
    """
    global latest_attributes
    
    try:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for (x, y, w, h) in faces:
            face_region = frame[y:y+h, x:x+w]
            result = DeepFace.analyze(face_region, actions=['age', 'gender', 'emotion', 'race'], enforce_detection=False)
            attributes = result[0]

            latest_attributes = {
                "age": f"{attributes['age']} anos",
                "gender": "Masculino" if attributes['dominant_gender'] == "Man" else "Feminino",
                "emotion": emotion_map.get(attributes['dominant_emotion'], attributes['dominant_emotion']),
                "ethnicity": ethnicity_map.get(attributes['dominant_race'], attributes['dominant_race'])
            }

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame
        
    except Exception as e:
        logging.error("Erro na análise facial: %s", e)
        return frame

# 7. FUNÇÃO GERADORA DE FRAMES PARA STREAMING
# ==============================================================================
def generate_frames():
    """
    Função geradora que captura frames continuamente da webcam,
    aplica a análise facial e prepara os dados para streaming web.
    
    Esta função implementa o padrão de streaming de vídeo para web browsers
    usando o formato multipart/x-mixed-replace, que permite atualizações
    contínuas da imagem sem recarregar a página.
    
    Yields:
        bytes: Frame codificado em JPEG formatado para streaming HTTP
    """
    global cap
    global camera_available

    while True:
        if cap is None:
            cap = open_camera()
            camera_available = cap is not None

        if cap is None:
            frame_bytes = build_placeholder_frame("Webcam indisponivel. Use o modo Upload de Arquivo.")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(1)
            continue

        success, frame = cap.read()

        if not success:
            release_camera()
            camera_available = False
            frame_bytes = build_placeholder_frame("Falha na webcam. Tentando reconectar...")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.5)
            continue

        camera_available = True
        processed_frame = analyze_face(frame)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 8. ROTAS DA APLICAÇÃO WEB (FLASK ENDPOINTS)
# ==============================================================================

@app.route('/')
def index():
    """
    Rota principal da aplicação.
    Serve a página HTML com a interface do usuário.
    
    Returns:
        str: Template HTML renderizado
    """
    return render_template_string(HTML_TEMPLATE, camera_available=camera_available)

@app.route('/video_feed')
def video_feed():
    """
    Rota que fornece o stream de vídeo em tempo real.
    
    Esta rota utiliza a função generate_frames() para criar um stream
    contínuo de imagens que são exibidas no browser como um vídeo.
    O formato 'multipart/x-mixed-replace' permite atualizações automáticas.
    
    Returns:
        Response: Stream de vídeo formatado para exibição web
    """
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attributes')
def attributes():
    """
    Rota que retorna os atributos faciais analisados em formato JSON.
    
    Esta rota é chamada periodicamente pelo JavaScript na página web
    para atualizar as informações exibidas sobre o rosto detectado.
    
    Returns:
        JSON: Dados dos últimos atributos analisados (idade, gênero, emoção, etnia)
    """
    return jsonify(latest_attributes)


@app.route('/upload', methods=['POST'])
def upload():
    global latest_attributes

    file_obj = request.files.get('file')
    if file_obj is None or file_obj.filename == '':
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file_bytes = np.frombuffer(file_obj.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Arquivo inválido. Envie uma imagem."}), 400

    processed_image = analyze_face(image)
    success, buffer = cv2.imencode('.jpg', processed_image)

    if not success:
        return jsonify({"error": "Falha ao processar imagem."}), 500

    preview_base64 = base64.b64encode(buffer.tobytes()).decode('utf-8')

    return jsonify({
        "message": "Arquivo analisado com sucesso!",
        "attributes": latest_attributes,
        "preview": preview_base64
    })

# 9. EXECUÇÃO PRINCIPAL DO PROGRAMA
# ==============================================================================
if __name__ == '__main__':
    """
    Ponto de entrada principal do programa.
    
    Quando o script é executado diretamente (não importado como módulo),
    inicia o servidor Flask em modo de desenvolvimento.
    
    O servidor ficará disponível em: http://127.0.0.1:5000
    
    Parâmetros:
    - debug=True: Habilita o modo de depuração (reinicialização automática
      quando o código é modificado e exibição detalhada de erros)
    """
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "5000"))
    log_startup(host, port)
    
    try:
        app.run(host=host, port=port, debug=True)
    except KeyboardInterrupt:
        logging.info("Encerrando aplicação...")
        release_camera()
        logging.info("Webcam liberada. Aplicação finalizada.")
    except Exception:
        logging.exception("Falha crítica ao iniciar/executar a aplicação")
        release_camera()