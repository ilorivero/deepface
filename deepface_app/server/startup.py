import logging
import os
import platform
import sys

from deepface_app.constants import (
    LOOPBACK_HOST,
    LOOPBACK_PREFIX,
    STARTUP_SEPARATOR_SIZE,
    WILDCARD_HOSTS,
)
from deepface_app.server.network import discover_lan_ips


def log_startup(app, settings):
    camera_service = app.config["CAMERA_SERVICE"]
    separator = "=" * STARTUP_SEPARATOR_SIZE
    logging.info(separator)
    logging.info("Sistema de Reconhecimento Facial iniciado")
    logging.info("SO: %s", platform.platform())
    logging.info("Python: %s", sys.version.split()[0])
    logging.info("Diretório: %s", os.getcwd())
    logging.info(
        "Webcam disponível: %s",
        "sim" if camera_service.camera_available else "não",
    )

    if settings.host in WILDCARD_HOSTS:
        logging.info("Rodando localmente em: http://%s:%s", LOOPBACK_HOST, settings.port)
        lan_ips = discover_lan_ips()
        if lan_ips:
            for ip in lan_ips:
                logging.info("Acesso pela rede local: http://%s:%s", ip, settings.port)
        else:
            logging.warning(
                "Não foi possível detectar IP de LAN automaticamente. Use `ipconfig`/`ifconfig`."
            )
    else:
        logging.info("Rodando em: http://%s:%s", settings.host, settings.port)
        if settings.host.startswith(LOOPBACK_PREFIX):
            logging.warning(
                "Host de loopback detectado. Dispositivos externos não conseguirão acessar."
            )

    logging.info("Pressione Ctrl+C para encerrar")
    logging.info(separator)
