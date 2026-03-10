"use strict";
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
        cameraFeed: getElementById("camera-feed"),
        uploadPlaceholder: getElementById("upload-placeholder"),
        uploadPanel: getElementById("upload-panel"),
        webcamButton: getElementById("mode-webcam"),
        uploadButton: getElementById("mode-upload"),
        age: getElementById("age"),
        gender: getElementById("gender"),
        emotion: getElementById("emotion"),
        ethnicity: getElementById("ethnicity"),
        serverIp: getElementById("server-ip"),
        remoteUrl: getElementById("remote-url"),
        remoteUrlStatus: getElementById("remote-url-status"),
        copyRemoteUrlButton: getElementById("copy-remote-url"),
        emotionDetailsList: getElementById("emotion_details_list"),
        status: getElementById("status"),
        uploadForm: getElementById("upload-form"),
        imageFile: getElementById("image-file"),
    };
}
async function copyTextToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        }
        catch {
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
    }
    catch {
        return false;
    }
}
function setMode(mode, ui) {
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
function renderEmotionDetails(details, ui) {
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
function renderAttributes(data, ui) {
    ui.age.innerText = data.age;
    ui.gender.innerText = data.gender;
    ui.emotion.innerText = data.emotion;
    ui.ethnicity.innerText = data.ethnicity;
    renderEmotionDetails(data.emotion_details, ui);
}
function disabledAttributes() {
    return {
        age: "--",
        gender: "--",
        emotion: "--",
        ethnicity: "--",
        emotion_details: [],
    };
}
function hasAttributes(payload) {
    return "attributes" in payload;
}
function hasCameraError(payload) {
    return "error" in payload;
}
async function updateAttributes(ui) {
    try {
        const response = await fetch("/attributes");
        if (!response.ok) {
            throw new Error("Falha na resposta de atributos.");
        }
        const data = (await response.json());
        renderAttributes(data, ui);
    }
    catch {
        ui.status.innerText = "Falha ao atualizar atributos em tempo real.";
    }
}
async function updateServerInfo(ui) {
    let detectedRemoteUrl = "";
    try {
        const response = await fetch("/server_info");
        if (!response.ok) {
            throw new Error("Falha na resposta de informações do servidor.");
        }
        const data = (await response.json());
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
    }
    catch {
        ui.serverIp.innerText = "IP da máquina: indisponível";
        ui.remoteUrl.innerText = "URL remota: indisponível";
        ui.copyRemoteUrlButton.disabled = true;
        ui.copyRemoteUrlButton.dataset.remoteUrl = "";
    }
    finally {
        if (!detectedRemoteUrl) {
            ui.remoteUrlStatus.innerText = "";
        }
    }
}
async function copyRemoteUrl(ui) {
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
async function uploadFile(event, ui) {
    var _a;
    event.preventDefault();
    const file = (_a = ui.imageFile.files) === null || _a === void 0 ? void 0 : _a[0];
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
        const data = (await response.json());
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
    }
    catch {
        ui.status.innerText = "Erro ao enviar arquivo.";
    }
}
function initializeApp() {
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
        void uploadFile(event, ui);
    });
}
window.addEventListener("DOMContentLoaded", initializeApp);
