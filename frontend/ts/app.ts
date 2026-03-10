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

interface UIElements {
  webcamView: HTMLElement;
  cameraFeed: HTMLImageElement;
  webcamButton: HTMLButtonElement;
  uploadButton: HTMLButtonElement;
  age: HTMLElement;
  gender: HTMLElement;
  emotion: HTMLElement;
  ethnicity: HTMLElement;
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
    webcamButton: getElementById<HTMLButtonElement>("mode-webcam"),
    uploadButton: getElementById<HTMLButtonElement>("mode-upload"),
    age: getElementById<HTMLElement>("age"),
    gender: getElementById<HTMLElement>("gender"),
    emotion: getElementById<HTMLElement>("emotion"),
    ethnicity: getElementById<HTMLElement>("ethnicity"),
    emotionDetailsList: getElementById<HTMLUListElement>("emotion_details_list"),
    status: getElementById<HTMLElement>("status"),
    uploadForm: getElementById<HTMLFormElement>("upload-form"),
    imageFile: getElementById<HTMLInputElement>("image-file"),
  };
}

function setMode(mode: Mode, ui: UIElements): void {
  if (mode === "webcam") {
    ui.webcamView.classList.remove("hidden");
    ui.webcamButton.classList.add("active");
    ui.uploadButton.classList.remove("active");
    ui.cameraFeed.src = "/video_feed";
    ui.cameraFeed.alt = "Stream da webcam";
    return;
  }

  ui.webcamView.classList.remove("hidden");
  ui.webcamButton.classList.remove("active");
  ui.uploadButton.classList.add("active");
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
  ui.age.innerText = `Idade: ${data.age}`;
  ui.gender.innerText = `Gênero: ${data.gender}`;
  ui.emotion.innerText = `Emoção: ${data.emotion}`;
  ui.ethnicity.innerText = `Etnia: ${data.ethnicity}`;
  renderEmotionDetails(data.emotion_details, ui);
}

function hasAttributes(
  payload: UploadResponse,
): payload is UploadSuccessResponse {
  return "attributes" in payload;
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

  setInterval(() => {
    void updateAttributes(ui);
  }, 1000);

  ui.webcamButton.addEventListener("click", () => setMode("webcam", ui));
  ui.uploadButton.addEventListener("click", () => setMode("upload", ui));

  ui.uploadForm.addEventListener("submit", (event) => {
    void uploadFile(event as SubmitEvent, ui);
  });
}

window.addEventListener("DOMContentLoaded", initializeApp);
