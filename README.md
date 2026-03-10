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

## 🧩 Frontend com TypeScript

O frontend foi migrado para TypeScript para facilitar manutenção e autocomplete.

- Código-fonte: `frontend/ts/app.ts`
- Arquivo gerado para o Flask servir: `frontend/public/js/app.js`

Para compilar o frontend:

```bash
cd frontend
npm install
npm run build:frontend
```

Para compilar em modo watch durante desenvolvimento:

```bash
cd frontend
npm run watch:frontend
```

## ▶️ Execução

```bash
python main.py
```

Por padrão, a aplicação sobe em modo LAN (`APP_HOST=0.0.0.0`) e imprime no log:

- URL local (`http://127.0.0.1:8080`)
- URLs da sua rede local (ex.: `http://192.168.0.15:8080`)

Abra no navegador (mesmo computador):

`http://127.0.0.1:8080`

Para acessar de outro dispositivo na mesma rede (celular/notebook):

`http://SEU_IP_DA_REDE:8080`

### Variáveis de ambiente úteis

- `APP_HOST` (default: `0.0.0.0`)
- `APP_PORT` (default: `8080`)
- `APP_DEBUG` (default: `false`)

Exemplo (macOS/Linux):

```bash
APP_HOST=0.0.0.0 APP_PORT=8080 APP_DEBUG=false python main.py
```

Exemplo (Windows PowerShell):

```powershell
$env:APP_HOST="0.0.0.0"
$env:APP_PORT="8080"
$env:APP_DEBUG="false"
python main.py
```

> Dica: se quiser isolar para acesso apenas local, use `APP_HOST=127.0.0.1`.

## 🐞 Debug no VS Code

O projeto já inclui configuração em `.vscode/launch.json`:

- **Debug: main.py**
- **Debug: Flask (main)**

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
  "emotion_details": [
    { "emotion": "Feliz", "score": 82.3 },
    { "emotion": "Neutro", "score": 10.4 },
    { "emotion": "Surpresa", "score": 4.1 }
  ]
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
├── deepface_app/
│   ├── __init__.py
│   ├── routes.py
│   └── services/
│       ├── camera_service.py
│       └── face_analyzer.py
├── main.py
├── requirements.txt
├── README.md
├── INSTALL.md
├── QUICKSTART.md
└── frontend/
  ├── package.json
  ├── tsconfig.json
  ├── node_modules/
  ├── templates/
  │   └── index.html
  ├── public/
  │   ├── css/
  │   │   └── style.css
  │   ├── js/
  │   │   └── app.js
  │   └── icei.png
  ├── ts/
  │   └── app.ts
```

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE`.
