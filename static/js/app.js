function setMode(mode) {
  const webcamView = document.getElementById("webcam-view");
  const uploadView = document.getElementById("upload-view");
  const webcamButton = document.getElementById("mode-webcam");
  const uploadButton = document.getElementById("mode-upload");

  if (mode === "webcam") {
    webcamView.classList.remove("hidden");
    uploadView.classList.add("hidden");
    webcamButton.classList.add("active");
    uploadButton.classList.remove("active");
  } else {
    webcamView.classList.add("hidden");
    uploadView.classList.remove("hidden");
    webcamButton.classList.remove("active");
    uploadButton.classList.add("active");
  }
}

function renderAttributes(data) {
  document.getElementById("age").innerText = "Idade: " + data.age;
  document.getElementById("gender").innerText = "Gênero: " + data.gender;
  document.getElementById("emotion").innerText = "Emoção: " + data.emotion;
  document.getElementById("ethnicity").innerText = "Etnia: " + data.ethnicity;
  document.getElementById("emotion_details").innerText =
    "Top emoções: " + data.emotion_details;
}

function updateAttributes() {
  fetch("/attributes")
    .then((response) => response.json())
    .then((data) => {
      renderAttributes(data);
    })
    .catch(() => {
      const status = document.getElementById("status");
      status.innerText = "Falha ao atualizar atributos em tempo real.";
    });
}

function uploadFile(event) {
  event.preventDefault();
  const fileInput = document.getElementById("image-file");
  const status = document.getElementById("status");
  const preview = document.getElementById("upload-preview");

  if (!fileInput.files || fileInput.files.length === 0) {
    status.innerText = "Selecione um arquivo de imagem.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  status.innerText = "Analisando arquivo...";

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) =>
      response.json().then((data) => ({ ok: response.ok, data })),
    )
    .then(({ ok, data }) => {
      if (data.preview) {
        preview.src = "data:image/jpeg;base64," + data.preview;
      }

      if (!ok) {
        status.innerText = data.error || "Falha no upload.";
        return;
      }

      status.innerText = data.message || "Análise concluída.";
      renderAttributes(data.attributes);
    })
    .catch(() => {
      status.innerText = "Erro ao enviar arquivo.";
    });
}

window.onload = function onLoad() {
  setMode("webcam");
  updateAttributes();
  setInterval(updateAttributes, 1000);
  document.getElementById("upload-form").addEventListener("submit", uploadFile);
};
