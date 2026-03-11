FROM python:3.11-slim

ARG PRELOAD_DEEPFACE_MODELS=false

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOST=0.0.0.0 \
    APP_PORT=8080 \
    APP_DEBUG=false \
    LOG_LEVEL=INFO \
    DEEPFACE_HOME=/root/.deepface

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN mkdir -p /root/.deepface/weights

RUN if [ "$PRELOAD_DEEPFACE_MODELS" = "true" ]; then \
    python -c "import numpy as np; from deepface import DeepFace; dummy = np.zeros((224, 224, 3), dtype='uint8'); DeepFace.analyze(dummy, actions=['age', 'gender', 'emotion', 'race'], enforce_detection=False); print('DeepFace models preloaded.')"; \
    fi

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)" || exit 1

CMD ["python", "main.py"]
