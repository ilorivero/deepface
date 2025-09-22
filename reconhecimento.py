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
import cv2                                          # OpenCV - para captura e processamento de vídeo
import numpy as np                                  # NumPy - para manipulação de arrays
from deepface import DeepFace                       # DeepFace - para análise facial avançada
from flask import Flask, Response, render_template_string, jsonify  # Flask - para criar a interface web

# 2. INICIALIZAÇÃO DA APLICAÇÃO FLASK
# ==============================================================================
app = Flask(__name__)  # Cria a instância da aplicação web

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
        /* Estilos CSS para formatação da página */
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; padding: 20px; }
        h1 { color: #333; }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-top: 20px;
        }

        .video-container {
            border: 3px solid #333;
            padding: 5px;
            background-color: white;
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

    </style>
    <script>
        // JavaScript para atualizar os atributos faciais a cada segundo
        function updateAttributes() {
            fetch('/attributes')  // Faz requisição para obter os dados analisados
                .then(response => response.json())
                .then(data => {
                    // Atualiza os elementos HTML com os dados recebidos
                    document.getElementById("age").innerText = "Idade: " + data.age;
                    document.getElementById("gender").innerText = "Gênero: " + data.gender;
                    document.getElementById("emotion").innerText = "Emoção: " + data.emotion;
                    document.getElementById("ethnicity").innerText = "Etnia: " + data.ethnicity;
                });
        }
        setInterval(updateAttributes, 1000);  // Executa a função a cada 1000ms (1 segundo)
    </script>
</head>
<body>
    <h1>Análise Facial em Tempo Real</h1>
    
    <div class="container">
        <div class="video-container">
            <!-- Exibe o stream de vídeo da webcam -->
            <img src="/video_feed">
        </div>
        <div class="info-container">
            <!-- Logo da instituição -->
            <img src="{{ url_for('static', filename='icei.png') }}" alt="Logomarca ICEI" class="logo">
            <!-- Painel com informações analisadas -->
            <div id="info">
                <p id="age">Idade: ?</p>
                <p id="gender">Gênero: ?</p>
                <p id="emotion">Emoção: ?</p>
                <p id="ethnicity">Etnia: ?</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# 4. INICIALIZAÇÃO DOS COMPONENTES DE VISÃO COMPUTACIONAL
# ==============================================================================
cap = cv2.VideoCapture(0)  # Inicializa a captura de vídeo da webcam (índice 0 = câmera padrão)

# Carrega o classificador Haar Cascade para detecção de rostos
# Este é um classificador pré-treinado que detecta rostos frontais em imagens
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 5. VARIÁVEL GLOBAL PARA ARMAZENAR OS ÚLTIMOS ATRIBUTOS ANALISADOS
# ==============================================================================
# Esta variável mantém os dados mais recentes da análise facial
# para serem exibidos na interface web
latest_attributes = {"age": "?", "gender": "?", "emotion": "?", "ethnicity": "?"}

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
        # ETAPA 1: DETECÇÃO DE ROSTOS
        # Converte o frame para escala de cinza (necessário para o Haar Cascade)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detecta rostos no frame
        # Parâmetros: (imagem, fator_escala, min_vizinhos)
        # - fator_escala=1.3: reduz a imagem em 30% a cada iteração
        # - min_vizinhos=5: número mínimo de detecções vizinhas para confirmar um rosto
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        
        # ETAPA 2: ANÁLISE DE CADA ROSTO DETECTADO
        for (x, y, w, h) in faces:
            # Extrai a região do rosto do frame original
            face_region = frame[y:y+h, x:x+w]
            
            # ETAPA 3: ANÁLISE COM DEEPFACE
            # Aplica o algoritmo DeepFace para analisar múltiplos atributos
            # - age: estimativa da idade
            # - gender: classificação de gênero
            # - emotion: detecção de emoção facial
            # - race: estimativa de etnia
            # - enforce_detection=False: permite análise mesmo com baixa confiança na detecção
            result = DeepFace.analyze(face_region, actions=['age', 'gender', 'emotion', 'race'], enforce_detection=False)
            attributes = result[0]  # Pega o primeiro resultado (caso múltiplos rostos)

            # ETAPA 4: MAPEAMENTO PARA PORTUGUÊS
            # Converte os resultados em inglês para português brasileiro
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

            # ETAPA 5: ATUALIZAÇÃO DOS RESULTADOS
            # Organiza os dados analisados e atualiza a variável global
            latest_attributes = {
                "age": f"{attributes['age']} anos",
                "gender": "Masculino" if attributes['dominant_gender'] == "Man" else "Feminino",
                "emotion": emotion_map.get(attributes['dominant_emotion'], attributes['dominant_emotion']),
                "ethnicity": ethnicity_map.get(attributes['dominant_race'], attributes['dominant_race'])
            }

            # ETAPA 6: DESENHO DO RETÂNGULO DE DETECÇÃO
            # Desenha um retângulo verde ao redor do rosto detectado
            # Parâmetros: (imagem, ponto_inicial, ponto_final, cor_BGR, espessura)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame
        
    except Exception as e:
        # Em caso de erro (ex: nenhum rosto detectado), retorna o frame original
        print(f"Erro na análise facial: {e}")
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
    while True:
        # Captura um frame da webcam
        success, frame = cap.read()
        
        if not success:
            print("Erro ao capturar frame da webcam")
            break
        else:
            # Aplica a análise facial no frame capturado
            processed_frame = analyze_face(frame)
            
            # Codifica o frame processado em formato JPEG
            # Retorna: (sucesso, buffer_com_imagem_codificada)
            _, buffer = cv2.imencode('.jpg', processed_frame)
            
            # Converte o buffer NumPy para bytes
            frame_bytes = buffer.tobytes()
            
            # Formata os dados para streaming HTTP multipart
            # Este formato permite que o browser atualize a imagem continuamente
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
    return render_template_string(HTML_TEMPLATE)

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
    print("=== SISTEMA DE RECONHECIMENTO FACIAL ===")
    print("Iniciando servidor...")
    print("Acesse: http://127.0.0.1:5000")
    print("Pressione Ctrl+C para encerrar")
    print("=" * 40)
    
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("\nEncerrando aplicação...")
        cap.release()  # Libera a webcam
        print("Webcam liberada. Aplicação finalizada.")