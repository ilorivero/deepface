function getElementById(id) {
  const element = document.getElementById(id);
  if (!element) {
    throw new Error(`Elemento com id '${id}' não encontrado.`);
  }
  return element;
}

function buildUI() {
  return {
    webcamView: getElementById("webcam-view"),
    uploadView: getElementById("upload-view"),
    webcamButton: getElementById("mode-webcam"),
    uploadButton: getElementById("mode-upload"),
    age: getElementById("age"),
    gender: getElementById("gender"),
    emotion: getElementById("emotion"),
    ethnicity: getElementById("ethnicity"),
    emotionDetails: getElementById("emotion_details"),
    status: getElementById("status"),
    uploadForm: getElementById("upload-form"),
    imageFile: getElementById("image-file"),
    uploadPreview: getElementById("upload-preview"),
  };
}

function setMode(mode, ui) {
  if (mode === "webcam") {
    ui.webcamView.classList.remove("hidden");
    ui.uploadView.classList.add("hidden");
    ui.webcamButton.classList.add("active");
    ui.uploadButton.classList.remove("active");
    return;
  }
  ui.webcamView.classList.add("hidden");
  ui.uploadView.classList.remove("hidden");
  ui.webcamButton.classList.remove("active");
  ui.uploadButton.classList.add("active");
}

function renderAttributes(data, ui) {
  ui.age.innerText = `Idade: ${data.age}`;
  ui.gender.innerText = `Gênero: ${data.gender}`;
  ui.emotion.innerText = `Emoção: ${data.emotion}`;
  ui.ethnicity.innerText = `Etnia: ${data.ethnicity}`;
  ui.emotionDetails.innerText = `Top emoções: ${data.emotion_details}`;
}

function hasAttributes(payload) {
  return "attributes" in payload;
}

async function updateAttributes(ui) {
  try {
    const response = await fetch("/attributes");
    if (!response.ok) {
      throw new Error("Falha na resposta de atributos.");
    }
    const data = await response.json();
    renderAttributes(data, ui);
  } catch {
    ui.status.innerText = "Falha ao atualizar atributos em tempo real.";
  }
}

async function uploadFile(event, ui) {
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
    const data = await response.json();
    if (data.preview) {
      ui.uploadPreview.src = `data:image/jpeg;base64,${data.preview}`;
    }
    if (!response.ok) {
      ui.status.innerText = data.error || "Falha no upload.";
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

function initializeApp() {
  const ui = buildUI();
  setMode("webcam", ui);
  void updateAttributes(ui);
  setInterval(() => {
    void updateAttributes(ui);
  }, 1000);
  ui.webcamButton.addEventListener("click", () => setMode("webcam", ui));
  ui.uploadButton.addEventListener("click", () => setMode("upload", ui));
  ui.uploadForm.addEventListener("submit", (event) => {
    void uploadFile(event, ui);
  });
}

window.addEventListener("DOMContentLoaded", initializeApp);
