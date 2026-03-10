# 🔍 Sistema de Reconhecimento Facial (DeepFace + Flask)

Aplicação web em Python para análise facial com **DeepFace**, com dois modos de entrada:

- **Webcam em tempo real**
- **Upload de imagem**

O sistema detecta e exibe:

- Idade
- Gênero
- Emoção dominante
- Top 3 emoções com percentual
- Etnia

## ✅ Estado atual do projeto

- Compatível com Windows, macOS e Linux
- Fallback de backend da câmera por sistema operacional
- Reconexão automática quando a webcam falha
- Logs simples de execução (SO, Python, pasta e URL)

## 📦 Requisitos

- Python **3.10, 3.11 ou 3.12** (recomendado: 3.11)
- Webcam (opcional, já que existe modo upload)
- Navegador moderno

> Observação: Python 3.13+ e 3.14 ainda podem ter incompatibilidades com TensorFlow/DeepFace.

## 🚀 Instalação

### 1) Criar e ativar ambiente virtual

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

O `requirements.txt` já escolhe automaticamente:

- `tensorflow-macos` no macOS Apple Silicon
- `tensorflow` nas demais plataformas
- `tf-keras` para compatibilidade com DeepFace + TensorFlow 2.16+

## ▶️ Execução

```bash
python reconhecimento.py
```

Abra no navegador:

`http://127.0.0.1:5000`

## 🐞 Debug no VS Code

O projeto já inclui configuração em `.vscode/launch.json`:

- **Debug: reconhecimento.py**
- **Debug: Flask (reconhecimento)**

Para usar:

1. Selecione o interpretador da `.venv`
2. Abra **Run and Debug**
3. Execute um dos perfis

## 🌐 Endpoints

### `GET /`

Interface principal.

### `GET /video_feed`

Stream de vídeo da webcam no formato `multipart/x-mixed-replace`.

### `GET /attributes`

Retorna os últimos atributos analisados.

Exemplo:

```json
{
  "age": "27 anos",
  "gender": "Masculino",
  "emotion": "Feliz",
  "ethnicity": "Branco",
  "emotion_details": "Feliz (82.3%) | Neutro (10.4%) | Surpresa (4.1%)"
}
```

### `POST /upload`

Recebe arquivo de imagem (`multipart/form-data`, campo `file`), processa e retorna:

- `attributes` (mesma estrutura do `/attributes`)
- `preview` (imagem processada em base64)

## 🔧 Troubleshooting

### Erro de TensorFlow / DeepFace

- Confirme Python 3.10–3.12
- Recrie a `.venv`
- Rode novamente `pip install -r requirements.txt`

### Erro `No module named tf_keras`

```bash
pip install tf-keras
```

### Webcam indisponível

- Verifique permissões de câmera no sistema
- Feche apps que possam estar usando a câmera
- Use o modo **Upload de Arquivo** como alternativa

## 📁 Estrutura do projeto

```text
deepface/
├── reconhecimento.py
├── requirements.txt
├── README.md
├── INSTALL.md
├── QUICKSTART.md
└── static/
```

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE`.
