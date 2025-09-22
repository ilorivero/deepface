# 📋 Guia Detalhado de Instalação

Este documento fornece instruções passo-a-passo para instalar e configurar o Sistema de Reconhecimento Facial em diferentes sistemas operacionais.

## 🎯 Índice

- [Pré-requisitos por Sistema](#-pré-requisitos-por-sistema)
- [Instalação no Windows](#-instalação-no-windows)
- [Instalação no macOS](#-instalação-no-macos)
- [Instalação no Linux](#-instalação-no-linux)
- [Verificação da Instalação](#-verificação-da-instalação)
- [Solução de Problemas](#-solução-de-problemas)

## 💻 Pré-requisitos por Sistema

### Windows 10/11
- Python 3.7+ ([Download oficial](https://python.org/downloads/))
- Microsoft Visual C++ Redistributable
- Webcam funcional
- Mínimo 4GB RAM

### macOS 10.14+
- Python 3.7+ (via Homebrew recomendado)
- Xcode Command Line Tools
- Webcam funcional
- Mínimo 4GB RAM

### Ubuntu/Debian/Linux
- Python 3.7+ 
- Pacotes de desenvolvimento
- Webcam funcional
- Mínimo 4GB RAM

## 🪟 Instalação no Windows

### Passo 1: Instalar Python
```powershell
# Baixar e instalar Python do site oficial
# https://python.org/downloads/

# Verificar instalação
python --version
pip --version
```

### Passo 2: Instalar Visual C++ Redistributable
```powershell
# Baixar do site oficial da Microsoft
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### Passo 3: Clonar o Repositório
```powershell
git clone https://github.com/seu-usuario/reconhecimento-facial.git
cd reconhecimento-facial
```

### Passo 4: Criar Ambiente Virtual
```powershell
python -m venv venv
venv\Scripts\activate
```

### Passo 5: Instalar Dependências
```powershell
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### Passo 6: Teste de Funcionamento
```powershell
python reconhecimento.py
```

## 🍎 Instalação no macOS

### Passo 1: Instalar Homebrew (se não tiver)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Passo 2: Instalar Python
```bash
brew install python@3.9
```

### Passo 3: Instalar Dependências do Sistema
```bash
# Para OpenCV
brew install cmake pkg-config
brew install jpeg libpng libtiff openexr
brew install eigen tbb
```

### Passo 4: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/reconhecimento-facial.git
cd reconhecimento-facial
```

### Passo 5: Criar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 6: Instalar Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 7: Permissões da Webcam
```bash
# O macOS solicitará permissão para acessar a câmera
# Aceite quando solicitado ou vá em:
# Preferências do Sistema > Segurança e Privacidade > Câmera
```

## 🐧 Instalação no Linux

### Ubuntu/Debian

### Passo 1: Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Passo 2: Instalar Python e Dependências
```bash
sudo apt install python3 python3-pip python3-venv python3-dev
sudo apt install build-essential cmake pkg-config
sudo apt install libjpeg-dev libtiff5-dev libpng-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install libxvidcore-dev libx264-dev
sudo apt install libgtk-3-dev
sudo apt install libatlas-base-dev gfortran
```

### Passo 3: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/reconhecimento-facial.git
cd reconhecimento-facial
```

### Passo 4: Criar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 5: Instalar Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 6: Configurar Webcam
```bash
# Verificar se a webcam está detectada
lsusb | grep -i camera
v4l2-ctl --list-devices

# Instalar utilitários de webcam (opcional)
sudo apt install cheese guvcview
```

### CentOS/RHEL/Fedora

### Passo 1: Instalar Dependências
```bash
# Fedora
sudo dnf install python3 python3-pip python3-devel
sudo dnf install cmake gcc gcc-c++ make
sudo dnf install opencv-devel

# CentOS/RHEL (com EPEL)
sudo yum install epel-release
sudo yum install python3 python3-pip python3-devel
sudo yum install cmake gcc gcc-c++ make
```

### Passo 2: Seguir passos 3-6 do Ubuntu

## ✅ Verificação da Instalação

### Teste 1: Importações Básicas
```python
python -c "
import cv2
import numpy as np
import flask
from deepface import DeepFace
print('✅ Todas as bibliotecas importadas com sucesso!')
print(f'OpenCV versão: {cv2.__version__}')
print(f'NumPy versão: {np.__version__}')
"
```

### Teste 2: Webcam
```python
python -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('✅ Webcam detectada e funcionando!')
    cap.release()
else:
    print('❌ Problema com a webcam')
"
```

### Teste 3: DeepFace
```python
python -c "
from deepface import DeepFace
import numpy as np
# Teste com imagem sintética
test_img = np.ones((224, 224, 3), dtype=np.uint8) * 128
try:
    result = DeepFace.analyze(test_img, actions=['emotion'], enforce_detection=False)
    print('✅ DeepFace funcionando!')
except Exception as e:
    print(f'❌ Erro no DeepFace: {e}')
"
```

## 🔧 Solução de Problemas

### Problema 1: "Microsoft Visual C++ 14.0 is required"
**Windows:**
```powershell
# Instalar Build Tools para Visual Studio
# https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019
```

### Problema 2: "Could not find a backend to open camera"
**Todos os sistemas:**
```bash
# Verificar se a webcam não está sendo usada por outro programa
# Reiniciar o computador se necessário
# Testar com webcam externa se a integrada não funcionar
```

### Problema 3: "No module named 'cv2'"
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python
```

### Problema 4: Erro de memória/TensorFlow
```bash
# Para CPU apenas (mais leve)
pip uninstall tensorflow
pip install tensorflow-cpu

# Reduzir uso de memória
export TF_CPP_MIN_LOG_LEVEL=2
```

### Problema 5: "Permission denied" para webcam (Linux)
```bash
# Adicionar usuário ao grupo video
sudo usermod -a -G video $USER
# Reiniciar sessão
```

### Problema 6: Porta 5000 ocupada
```python
# Alterar porta no arquivo reconhecimento.py
app.run(debug=True, port=5001)  # ou qualquer porta livre
```

## 🚀 Otimizações Opcionais

### Para melhor performance:

1. **Instalar TensorFlow com GPU** (se disponível):
```bash
pip install tensorflow-gpu
```

2. **Usar ambiente conda** (alternativa ao venv):
```bash
conda create -n reconhecimento python=3.9
conda activate reconhecimento
conda install tensorflow opencv flask
pip install deepface
```

3. **Otimizar OpenCV** (compilação personalizada):
```bash
# Somente para usuários avançados
# Compilar OpenCV com otimizações específicas do hardware
```

## 📞 Suporte

Se você encontrar problemas não cobertos neste guia:

1. Verifique as [Issues do GitHub](link-para-issues)
2. Crie uma nova issue com:
   - Sistema operacional e versão
   - Versão do Python
   - Mensagem de erro completa
   - Passos para reproduzir o problema

---

**✨ Dica**: Sempre use ambientes virtuais para evitar conflitos entre projetos!