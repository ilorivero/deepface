# Dockerização Completa do Projeto DeepFace

Este guia descreve como rodar o projeto inteiro em containers (backend + frontend), com persistência de cache dos modelos do DeepFace.

## Visão geral

A stack Docker foi organizada em dois serviços:

- `backend`: Flask + DeepFace + OpenCV (porta interna `8080`, publicada como `8081` no host)
- `frontend`: Nginx servindo arquivos estáticos e fazendo proxy para o backend (porta `8080` no host)

Além disso:

- existe um volume nomeado `deepface_models` para persistir pesos/modelos baixados pelo DeepFace
- o backend expõe `GET /health` para healthcheck
- o frontend só sobe depois do backend ficar saudável

## Arquitetura de rede

- Navegador -> `http://localhost:8080` (frontend/Nginx)
- Frontend (Nginx) -> `http://backend:8080` (backend Flask, via rede interna do Compose)
- Backend direto (debug/API): `http://localhost:8081`

## Pré-requisitos

- Docker
- Docker Compose (plugin `docker compose`)

Verificação rápida:

```bash
docker --version
docker compose version
```

## Subir o projeto inteiro

Na raiz do projeto:

```bash
docker compose up --build
```

Em background:

```bash
docker compose up --build -d
```

Acessos:

- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8081`
- Healthcheck backend: `http://localhost:8081/health`

## Parar e remover

```bash
docker compose down
```

Remover também o volume de modelos (limpeza total):

```bash
docker compose down -v
```

## Persistência dos modelos DeepFace

Os pesos/modelos baixados pelo DeepFace são gravados no volume:

- volume: `deepface_models`
- path no container: `/root/.deepface`

Benefício: após o primeiro download, os próximos `up` ficam mais rápidos.

## Pré-carregar modelos no build (opcional)

Por padrão, a imagem não força preload de modelos durante o build.

Se quiser embutir preload no build, altere no `docker-compose.yml`:

- `services.backend.build.args.PRELOAD_DEEPFACE_MODELS: "true"`

Depois rode novamente:

```bash
docker compose build --no-cache backend
docker compose up -d
```

Observação: preload aumenta tempo de build e tamanho da imagem.

## Logs e diagnóstico

Logs de todos os serviços:

```bash
docker compose logs -f
```

Somente backend:

```bash
docker compose logs -f backend
```

Status dos containers:

```bash
docker compose ps
```

Inspecionar healthcheck do backend:

```bash
docker inspect --format='{{json .State.Health}}' deepface-backend
```

## Webcam dentro de container

- macOS/Windows (Docker Desktop): acesso direto à webcam pelo container pode ter limitações.
- Linux: pode funcionar com mapeamento de dispositivo (ex.: `/dev/video0`) e permissões.

Exemplo Linux (adicionar no serviço `backend`):

```yaml
devices:
  - /dev/video0:/dev/video0
```

Mesmo sem webcam no container, o fluxo de upload de imagem continua funcional.

## Variáveis úteis do backend

No `docker-compose.yml`:

- `APP_HOST` (padrão `0.0.0.0`)
- `APP_PORT` (padrão `8080`)
- `APP_DEBUG` (padrão `false`)
- `LOG_LEVEL` (padrão `INFO`)
- `DEEPFACE_HOME` (padrão `/root/.deepface`)

## Problemas comuns

### Backend em `unhealthy`

- Verifique logs:

```bash
docker compose logs backend
```

- Teste endpoint:

```bash
curl -f http://localhost:8081/health
```

### Porta 8080 ocupada

Troque o mapeamento do frontend em `docker-compose.yml`:

- de `"8080:80"`
- para `"8090:80"`

Depois:

```bash
docker compose up -d --build
```

### Build muito demorado no primeiro uso

Normal no primeiro pull/build da stack e no primeiro download de modelos DeepFace.
