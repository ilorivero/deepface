# 🚀 Guia de Execução Rápida

Este arquivo contém comandos essenciais para executar o projeto rapidamente.

## ⚡ Execução Rápida (Windows)

```powershell
# 1. Clone o repositório
git clone https://github.com/seu-usuario/reconhecimento-facial.git
cd reconhecimento-facial

# 2. Crie ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute o programa
python reconhecimento.py

# 5. Acesse no navegador
# http://127.0.0.1:5000
```

## ⚡ Execução Rápida (macOS/Linux)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/reconhecimento-facial.git
cd reconhecimento-facial

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute o programa
python reconhecimento.py

# 5. Acesse no navegador
# http://127.0.0.1:5000
```

## 🔄 Comandos Úteis

### Ativação do Ambiente Virtual
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Desativação do Ambiente Virtual
```bash
deactivate
```

### Atualizar Dependências
```bash
pip install --upgrade -r requirements.txt
```

### Limpar Cache Python
```bash
# Windows
rmdir /s __pycache__

# macOS/Linux
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Verificar Versões
```bash
python --version
pip list
```

## 🐛 Resolução Rápida de Problemas

### Webcam não funciona
```bash
# Teste a webcam
python -c "import cv2; cap=cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'ERRO'); cap.release()"
```

### Erro de importação
```bash
pip install --force-reinstall opencv-python deepface flask tensorflow
```

### Porta ocupada
```bash
# Use porta diferente (altere no código)
# app.run(debug=True, port=5001)
```

### Limpeza completa
```bash
# Remover ambiente virtual e recomeçar
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Recriar tudo
python -m venv venv
# ... seguir passos de instalação
```

## 📱 URLs Importantes

- **Aplicação local**: http://127.0.0.1:5000
- **Stream de vídeo**: http://127.0.0.1:5000/video_feed
- **API de atributos**: http://127.0.0.1:5000/attributes

## 🎯 Primeiro Uso

1. **Permita acesso à webcam** quando solicitado pelo navegador
2. **Posicione seu rosto** na frente da câmera
3. **Aguarde alguns segundos** para a análise começar
4. **Observe os resultados** no painel lateral

## ⚠️ Notas Importantes

- O primeiro uso pode demorar mais (download de modelos)
- Certifique-se de ter boa iluminação
- Mantenha o rosto centralizado na câmera
- Use `Ctrl+C` para parar o programa

---

**🎉 Pronto! Seu sistema de reconhecimento facial está funcionando!**