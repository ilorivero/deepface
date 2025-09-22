# 🔍 Sistema de Reconhecimento Facial em Tempo Real

Um sistema completo de análise facial que utiliza **DeepFace** e **OpenCV** para detectar e analisar características faciais em tempo real através de uma interface web moderna. Este exemplo de código foi gerado pelo Copilot e documentado pelo Claude para testar as capacidades de desenvolvimento de aplicações simples que utilizem Inteligência Artificial.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-v4.0+-green.svg)
![DeepFace](https://img.shields.io/badge/deepface-v0.0.79+-orange.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Funciona](#-como-funciona)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Sobre o Projeto

Este sistema implementa um algoritmo avançado de reconhecimento facial que analisa múltiplos atributos em tempo real:

- **Idade**: Estimativa baseada em características faciais
- **Gênero**: Classificação masculino/feminino
- **Emoção**: Detecção de 7 emoções básicas (feliz, triste, zangado, etc.)
- **Etnia**: Classificação étnica em 6 categorias principais

O projeto combina técnicas de **Computer Vision** e **Deep Learning** para criar uma aplicação web interativa e educacional.

## ✨ Funcionalidades

### 🎥 Análise em Tempo Real
- Captura de vídeo da webcam
- Detecção automática de rostos
- Análise simultânea de múltiplos atributos
- Interface web responsiva

### 🧠 Inteligência Artificial
- Utiliza modelos pré-treinados do DeepFace
- Redes neurais convolucionais (CNNs)
- Precisão elevada na classificação
- Processamento otimizado

### 🌐 Interface Web Moderna
- Design responsivo e intuitivo
- Atualizações em tempo real via AJAX
- Streaming de vídeo otimizado
- Suporte para logos personalizados

## 🚀 Tecnologias Utilizadas

### Core Libraries
- **[DeepFace](https://github.com/serengil/deepface)**: Framework de deep learning para análise facial
- **[OpenCV](https://opencv.org/)**: Biblioteca de computer vision para processamento de imagem
- **[Flask](https://flask.palletsprojects.com/)**: Framework web para Python
- **[NumPy](https://numpy.org/)**: Computação científica e manipulação de arrays

### Modelos de IA Utilizados
- **VGG-Face**: Reconhecimento facial
- **Emotion Models**: Classificação de emoções
- **Age-Gender Models**: Estimativa de idade e gênero
- **Race Classification**: Análise étnica

### Frontend
- **HTML5**: Estrutura da página
- **CSS3**: Estilização e layout responsivo
- **JavaScript**: Interatividade e comunicação AJAX

## 🔬 Como Funciona

### 1. **Captura de Vídeo**
```python
cap = cv2.VideoCapture(0)  # Inicializa webcam
```

### 2. **Detecção de Rostos**
```python
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
```

### 3. **Análise com DeepFace**
```python
result = DeepFace.analyze(face_region, 
                         actions=['age', 'gender', 'emotion', 'race'],
                         enforce_detection=False)
```

### 4. **Processamento dos Resultados**
- Mapeamento de idiomas (EN → PT)
- Formatação dos dados
- Atualização da interface

### 5. **Streaming Web**
- Formato multipart/x-mixed-replace
- Atualizações contínuas sem reload
- API REST para dados JSON

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Ubuntu 18.04+

### Software Necessário
- **Python 3.7+** ([Download](https://python.org/downloads/))
- **Webcam** (integrada ou USB)
- **Navegador Web** (Chrome, Firefox, Safari, Edge)

### Recursos de Hardware
- **RAM**: Mínimo 4GB (Recomendado 8GB+)
- **CPU**: Processador dual-core 2.0GHz+
- **GPU**: Opcional (acelera o processamento)

## 📦 Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/reconhecimento-facial.git
cd reconhecimento-facial
```

### 2. Crie um Ambiente Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Instale Dependências Manualmente (se necessário)
```bash
pip install deepface opencv-python flask tensorflow numpy
```

### 5. Verificar Instalação
```bash
python -c "import cv2, deepface; print('Instalação bem-sucedida!')"
```

## ▶️ Como Executar

### 1. **Execução Básica**
```bash
python reconhecimento.py
```

### 2. **Acesse a Aplicação**
- Abra seu navegador
- Navegue para: `http://127.0.0.1:5000`
- Permita acesso à webcam quando solicitado

### 3. **Parar a Aplicação**
- Pressione `Ctrl + C` no terminal
- A webcam será liberada automaticamente

### 4. **Execução em Modo Produção** (Opcional)
```bash
# Para ambiente de produção
export FLASK_ENV=production
python reconhecimento.py
```

## 📁 Estrutura do Projeto

```
reconhecimento-facial/
│
├── reconhecimento.py          # Arquivo principal da aplicação
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git
│
├── static/                   # Arquivos estáticos
│   ├── icei.png             # Logo da instituição
│   └── css/                 # Estilos CSS (se expandir)
│
├── templates/               # Templates HTML (se expandir)
│   └── index.html          # Template principal (opcional)
│
└── docs/                   # Documentação adicional
    ├── INSTALL.md          # Guia de instalação detalhado
    ├── API.md              # Documentação da API
    └── TROUBLESHOOTING.md  # Solução de problemas
```

## 🌐 API Endpoints

### **GET /**
- **Descrição**: Página principal da aplicação
- **Retorno**: Interface HTML completa
- **Exemplo**: `http://127.0.0.1:5000/`

### **GET /video_feed**
- **Descrição**: Stream de vídeo em tempo real
- **Formato**: multipart/x-mixed-replace
- **Exemplo**: `http://127.0.0.1:5000/video_feed`

### **GET /attributes**
- **Descrição**: Dados JSON dos atributos analisados
- **Retorno**: 
```json
{
    "age": "25 anos",
    "gender": "Masculino",
    "emotion": "Feliz",
    "ethnicity": "Branco"
}
```

## 🔧 Troubleshooting

### ❌ **Erro: "No module named 'cv2'"**
```bash
pip install opencv-python
```

### ❌ **Erro: "Could not find a backend to open"**
```bash
# Ubuntu/Debian
sudo apt-get install python3-opencv

# Reinstalar
pip uninstall opencv-python
pip install opencv-python
```

### ❌ **Webcam não detectada**
1. Verifique se a webcam está conectada
2. Teste com outras aplicações (Skype, Zoom)
3. Altere o índice da câmera:
```python
cap = cv2.VideoCapture(1)  # Tente 1, 2, 3...
```

### ❌ **Erro de memória/performance lenta**
1. Feche outras aplicações
2. Reduza a resolução da webcam:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

### ❌ **Erro: "TensorFlow not found"**
```bash
# CPU apenas
pip install tensorflow

# Com suporte GPU (opcional)
pip install tensorflow-gpu
```

### ❌ **Porta 5000 já em uso**
```python
# Altere a porta no código
app.run(debug=True, port=5001)
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### 💡 Ideias para Contribuição
- [ ] Adicionar mais emoções/expressões
- [ ] Implementar reconhecimento de múltiplos rostos
- [ ] Adicionar filtros em tempo real
- [ ] Criar modo escuro na interface
- [ ] Implementar gravação de vídeo
- [ ] Adicionar estatísticas/relatórios
- [ ] Melhorar precisão dos modelos
- [ ] Criar versão mobile

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2025 Ilo Rivero

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Contato

- **Autor**: Ilo Rivero
- **Email**: ilo@pucminas.br
- **LinkedIn**: https://linkedin.com/in/ilorivero
- **GitHub**: github.com/ilorivero

---

### 🌟 **Se este projeto foi útil, considere dar uma ⭐ no repositório!**

---

*Desenvolvido com ❤️ para fins educacionais e demonstração de técnicas de Computer Vision e Deep Learning.*
