import base64

import cv2
import numpy as np
from flask import Blueprint, Response, jsonify, render_template, request

from deepface_app.constants import DEFAULT_APP_PORT
from deepface_app.server.network import discover_lan_ips


def _disabled_attributes():
    return {
        "age": "--",
        "gender": "--",
        "emotion": "--",
        "ethnicity": "--",
        "emotion_details": [],
    }


def create_main_blueprint(face_analyzer, camera_service, state):
    main_blueprint = Blueprint("main", __name__)

    @main_blueprint.route("/")
    def index():
        return render_template("index.html")

    @main_blueprint.route("/video_feed")
    def video_feed():
        def process_frame(frame):
            processed_frame, attributes = face_analyzer.analyze_face(frame)
            if attributes is not None:
                state["latest_attributes"] = attributes
            return processed_frame

        return Response(
            camera_service.generate_frames(process_frame),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    @main_blueprint.route("/attributes")
    def attributes():
        if not camera_service.is_camera_enabled():
            disabled_state = _disabled_attributes()
            state["latest_attributes"] = disabled_state
            return jsonify(disabled_state)

        return jsonify(state["latest_attributes"])

    @main_blueprint.route("/camera_status")
    def camera_status():
        return jsonify(
            {
                "enabled": camera_service.is_camera_enabled(),
                "available": camera_service.camera_available,
            }
        )

    @main_blueprint.route("/camera/control", methods=["POST"])
    def camera_control():
        payload = request.get_json(silent=True) or {}
        target_enabled = payload.get("enabled")

        if not isinstance(target_enabled, bool):
            return jsonify({"error": "Parâmetro 'enabled' inválido."}), 400

        if target_enabled:
            available = camera_service.start_camera()
            message = (
                "Câmera ligada."
                if available
                else "Câmera ligada, mas nenhum dispositivo foi encontrado."
            )
        else:
            camera_service.stop_camera()
            available = False
            message = "Câmera desligada."
            state["latest_attributes"] = _disabled_attributes()

        return jsonify(
            {
                "enabled": camera_service.is_camera_enabled(),
                "available": available,
                "message": message,
            }
        )

    @main_blueprint.route("/server_info")
    def server_info():
        lan_ips = discover_lan_ips()
        host_with_port = request.host or ""
        _, _, port = host_with_port.rpartition(":")
        resolved_port = port if port.isdigit() else str(DEFAULT_APP_PORT)

        return jsonify(
            {
                "lan_ips": lan_ips,
                "port": int(resolved_port),
            }
        )

    @main_blueprint.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @main_blueprint.route("/upload", methods=["POST"])
    def upload():
        file_obj = request.files.get("file")
        if file_obj is None or file_obj.filename == "":
            return jsonify({"error": "Nenhum arquivo enviado."}), 400

        file_bytes = np.frombuffer(file_obj.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Arquivo inválido. Envie uma imagem."}), 400

        processed_image, attributes = face_analyzer.analyze_face(image)
        success, buffer = cv2.imencode(".jpg", processed_image)

        if not success:
            return jsonify({"error": "Falha ao processar imagem."}), 500

        preview_base64 = base64.b64encode(buffer.tobytes()).decode("utf-8")

        if attributes is None:
            return (
                jsonify(
                    {
                        "error": "Nenhum rosto detectado na imagem.",
                        "attributes": state["latest_attributes"],
                        "preview": preview_base64,
                    }
                ),
                422,
            )

        state["latest_attributes"] = attributes
        return jsonify(
            {
                "message": "Arquivo analisado com sucesso!",
                "attributes": state["latest_attributes"],
                "preview": preview_base64,
            }
        )

    return main_blueprint
