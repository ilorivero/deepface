type Mode = "webcam" | "upload";

interface EmotionDetail {
  emotion: string;
  score: number;
}

interface AttributesResponse {
  age: string;
  gender: string;
  emotion: string;
  ethnicity: string;
  emotion_details: EmotionDetail[];
}

interface UploadSuccessResponse {
  message?: string;
  preview?: string;
  attributes: AttributesResponse;
}

interface UploadErrorResponse {
  error?: string;
  preview?: string;
}

type UploadResponse = UploadSuccessResponse | UploadErrorResponse;

interface ServerInfoResponse {
  lan_ips: string[];
  port: number;
}

interface UIElements {
  webcamView: HTMLElement;
  cameraFeed: HTMLImageElement;
  uploadPlaceholder: HTMLElement;
  uploadPanel: HTMLElement;
  webcamButton: HTMLButtonElement;
  uploadButton: HTMLButtonElement;
  age: HTMLElement;
  gender: HTMLElement;
  emotion: HTMLElement;
  ethnicity: HTMLElement;
  serverIp: HTMLElement;
  remoteUrl: HTMLElement;
  remoteUrlStatus: HTMLElement;
  copyRemoteUrlButton: HTMLButtonElement;
  emotionDetailsList: HTMLUListElement;
  status: HTMLElement;
  uploadForm: HTMLFormElement;
  imageFile: HTMLInputElement;
}

function getElementById<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) {
    throw new Error(`Elemento com id '${id}' não encontrado.`);
  }

  return element as T;
}

function buildUI(): UIElements {
  return {
    webcamView: getElementById<HTMLElement>("webcam-view"),
    cameraFeed: getElementById<HTMLImageElement>("camera-feed"),
    uploadPlaceholder: getElementById<HTMLElement>("upload-placeholder"),
    uploadPanel: getElementById<HTMLElement>("upload-panel"),
    webcamButton: getElementById<HTMLButtonElement>("mode-webcam"),
    uploadButton: getElementById<HTMLButtonElement>("mode-upload"),
    age: getElementById<HTMLElement>("age"),
    gender: getElementById<HTMLElement>("gender"),
    emotion: getElementById<HTMLElement>("emotion"),
    ethnicity: getElementById<HTMLElement>("ethnicity"),
    serverIp: getElementById<HTMLElement>("server-ip"),
    remoteUrl: getElementById<HTMLElement>("remote-url"),
    remoteUrlStatus: getElementById<HTMLElement>("remote-url-status"),
    copyRemoteUrlButton: getElementById<HTMLButtonElement>("copy-remote-url"),
    emotionDetailsList: getElementById<HTMLUListElement>("emotion_details_list"),
    status: getElementById<HTMLElement>("status"),
    uploadForm: getElementById<HTMLFormElement>("upload-form"),
    imageFile: getElementById<HTMLInputElement>("image-file"),
  };
}

async function copyTextToClipboard(text: string): Promise<boolean> {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      return false;
    }
  }

  try {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    const copied = document.execCommand("copy");
    document.body.removeChild(textArea);
    return copied;
  } catch {
    return false;
  }
}

function setMode(mode: Mode, ui: UIElements): void {
  if (mode === "webcam") {
    ui.webcamView.classList.remove("hidden");
    ui.uploadPanel.classList.add("hidden");
    ui.webcamButton.classList.add("active");
    ui.uploadButton.classList.remove("active");
    ui.uploadPlaceholder.classList.add("hidden");
    ui.cameraFeed.classList.remove("hidden");
    ui.cameraFeed.src = "/video_feed";
    ui.cameraFeed.alt = "Stream da webcam";
    return;
  }

  ui.webcamView.classList.remove("hidden");
  ui.uploadPanel.classList.remove("hidden");
  ui.webcamButton.classList.remove("active");
  ui.uploadButton.classList.add("active");
  ui.cameraFeed.src = "";
  ui.cameraFeed.classList.add("hidden");
  ui.uploadPlaceholder.classList.remove("hidden");
  ui.uploadPlaceholder.innerText = "Esperando upload de arquivo";
}

function renderEmotionDetails(details: EmotionDetail[], ui: UIElements): void {
  ui.emotionDetailsList.innerHTML = "";

  if (!Array.isArray(details) || details.length === 0) {
    const noDataItem = document.createElement("li");
    noDataItem.innerText = "Sem dados";
    ui.emotionDetailsList.appendChild(noDataItem);
    return;
  }

  details.forEach((detail) => {
    const listItem = document.createElement("li");
    listItem.innerText = `${detail.emotion}: ${detail.score.toFixed(1)}%`;
    ui.emotionDetailsList.appendChild(listItem);
  });
}

function renderAttributes(data: AttributesResponse, ui: UIElements): void {
  ui.age.innerText = data.age;
  ui.gender.innerText = data.gender;
  ui.emotion.innerText = data.emotion;
  ui.ethnicity.innerText = data.ethnicity;
  renderEmotionDetails(data.emotion_details, ui);
}

function disabledAttributes(): AttributesResponse {
  return {
    age: "--",
    gender: "--",
    emotion: "--",
    ethnicity: "--",
    emotion_details: [],
  };
}

function hasAttributes(
  payload: UploadResponse,
): payload is UploadSuccessResponse {
  return "attributes" in payload;
}

function hasCameraError(
  payload: CameraStateResponse | CameraErrorResponse,
): payload is CameraErrorResponse {
  return "error" in payload;
}

async function updateAttributes(ui: UIElements): Promise<void> {
  try {
    const response = await fetch("/attributes");
    if (!response.ok) {
      throw new Error("Falha na resposta de atributos.");
    }

    const data = (await response.json()) as AttributesResponse;
    renderAttributes(data, ui);
  } catch {
    ui.status.innerText = "Falha ao atualizar atributos em tempo real.";
  }
}

async function updateServerInfo(ui: UIElements): Promise<void> {
  let detectedRemoteUrl = "";

  try {
    const response = await fetch("/server_info");
    if (!response.ok) {
      throw new Error("Falha na resposta de informações do servidor.");
    }

    const data = (await response.json()) as ServerInfoResponse;

    if (Array.isArray(data.lan_ips) && data.lan_ips.length > 0) {
      const primaryIp = data.lan_ips[0];
      ui.serverIp.innerText = `IP da máquina: ${primaryIp} (porta ${data.port})`;
      detectedRemoteUrl = `http://${primaryIp}:${data.port}`;
      ui.remoteUrl.innerText = `URL remota: ${detectedRemoteUrl}`;
      ui.copyRemoteUrlButton.disabled = false;
      ui.copyRemoteUrlButton.dataset.remoteUrl = detectedRemoteUrl;
      return;
    }

    ui.serverIp.innerText = "IP da máquina: não detectado";
    ui.remoteUrl.innerText = "URL remota: não detectada";
    ui.copyRemoteUrlButton.disabled = true;
    ui.copyRemoteUrlButton.dataset.remoteUrl = "";
  } catch {
    ui.serverIp.innerText = "IP da máquina: indisponível";
    ui.remoteUrl.innerText = "URL remota: indisponível";
    ui.copyRemoteUrlButton.disabled = true;
    ui.copyRemoteUrlButton.dataset.remoteUrl = "";
  } finally {
    if (!detectedRemoteUrl) {
      ui.remoteUrlStatus.innerText = "";
    }
  }
}

async function copyRemoteUrl(ui: UIElements): Promise<void> {
  const remoteUrl = ui.copyRemoteUrlButton.dataset.remoteUrl || "";
  if (!remoteUrl) {
    ui.remoteUrlStatus.innerText = "URL remota indisponível para cópia.";
    return;
  }

  const copied = await copyTextToClipboard(remoteUrl);
  ui.remoteUrlStatus.innerText = copied
    ? "URL copiada para a área de transferência."
    : "Não foi possível copiar automaticamente.";
}

async function uploadFile(event: SubmitEvent, ui: UIElements): Promise<void> {
  event.preventDefault();

  const file = ui.imageFile.files?.[0];
  if (!file) {
    ui.status.innerText = "Selecione um arquivo de imagem.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  ui.status.innerText = "Analisando arquivo...";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    const data = (await response.json()) as UploadResponse;

    if (data.preview) {
      setMode("upload", ui);
      ui.uploadPlaceholder.classList.add("hidden");
      ui.cameraFeed.classList.remove("hidden");
      ui.cameraFeed.src = `data:image/jpeg;base64,${data.preview}`;
      ui.cameraFeed.alt = "Preview da foto enviada";
    }

    if (!response.ok) {
      const errorMessage = "error" in data ? data.error : undefined;
      ui.status.innerText = errorMessage || "Falha no upload.";
      return;
    }

    if (hasAttributes(data)) {
      ui.status.innerText = data.message || "Análise concluída.";
      renderAttributes(data.attributes, ui);
      return;
    }

    ui.status.innerText = "Análise concluída.";
  } catch {
    ui.status.innerText = "Erro ao enviar arquivo.";
  }
}

function initializeApp(): void {
  const ui = buildUI();

  setMode("webcam", ui);
  void updateAttributes(ui);
  void updateServerInfo(ui);

  setInterval(() => {
    void updateAttributes(ui);
  }, 1000);

  ui.webcamButton.addEventListener("click", () => setMode("webcam", ui));
  ui.uploadButton.addEventListener("click", () => setMode("upload", ui));
  ui.copyRemoteUrlButton.addEventListener("click", () => {
    void copyRemoteUrl(ui);
  });

  ui.uploadForm.addEventListener("submit", (event) => {
    void uploadFile(event as SubmitEvent, ui);
  });
}

window.addEventListener("DOMContentLoaded", initializeApp);
