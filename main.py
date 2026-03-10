import logging
import os
import platform
import sys

from deepface_app import create_app

app = create_app()


def log_startup(host, port):
    camera_service = app.config["CAMERA_SERVICE"]
    separator = "=" * 60
    logging.info(separator)
    logging.info("Sistema de Reconhecimento Facial iniciado")
    logging.info("SO: %s", platform.platform())
    logging.info("Python: %s", sys.version.split()[0])
    logging.info("Diretório: %s", os.getcwd())
    logging.info(
        "Webcam disponível: %s",
        "sim" if camera_service.camera_available else "não",
    )
    logging.info("Rodando em: http://%s:%s", host, port)
    logging.info("Pressione Ctrl+C para encerrar")
    logging.info(separator)


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "localhost")
    port = int(os.getenv("APP_PORT", "5000"))
    log_startup(host, port)

    try:
        app.run(host=host, port=port, debug=True)
    except KeyboardInterrupt:
        logging.info("Encerrando aplicação...")
        app.config["CAMERA_SERVICE"].release_camera()
        logging.info("Webcam liberada. Aplicação finalizada.")
    except Exception:
        logging.exception("Falha crítica ao iniciar/executar a aplicação")
        app.config["CAMERA_SERVICE"].release_camera()
