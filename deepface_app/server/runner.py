import logging

from deepface_app.constants import LOCALHOST_VALUE
from deepface_app.server.startup import log_startup


def _release_camera_safely(app):
    camera_service = app.config.get("CAMERA_SERVICE")
    if camera_service is not None:
        camera_service.release_camera()


def run_server(app, settings):
    if settings.raw_host.lower() == LOCALHOST_VALUE:
        logging.warning(
            "APP_HOST=localhost detectado. Usando 127.0.0.1 para evitar conflito local."
        )

    log_startup(app, settings)

    try:
        app.run(
            host=settings.host,
            port=settings.port,
            debug=settings.debug,
            threaded=settings.threaded,
        )
    except KeyboardInterrupt:
        logging.info("Encerrando aplicação...")
        _release_camera_safely(app)
        logging.info("Webcam liberada. Aplicação finalizada.")
    except Exception:
        logging.exception("Falha crítica ao iniciar/executar a aplicação")
        _release_camera_safely(app)
