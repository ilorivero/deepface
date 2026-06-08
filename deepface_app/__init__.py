import atexit
import logging
import os

from flask import Flask

from deepface_app.routes import create_main_blueprint
from deepface_app.services.camera_service import CameraService
from deepface_app.services.face_analyzer import FaceAnalyzer


def _configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def _initial_attributes():
    return {
        "age": "--",
        "gender": "--",
        "emotion": "--",
        "ethnicity": "--",
        "emotion_details": [],
    }


def create_app():
    _configure_logging()

    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/public",
        static_url_path="/static",
    )

    camera_service = CameraService()
    face_analyzer = FaceAnalyzer()
    state = {"latest_attributes": _initial_attributes()}

    app.config["CAMERA_SERVICE"] = camera_service
    app.config["STATE"] = state

    app.register_blueprint(
        create_main_blueprint(
            face_analyzer=face_analyzer,
            camera_service=camera_service,
            state=state,
        )
    )

    atexit.register(camera_service.release_camera)
    return app
