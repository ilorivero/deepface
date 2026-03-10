import logging
import socket

from deepface_app.constants import LAN_DISCOVERY_TARGET, LOOPBACK_PREFIX


def discover_lan_ips():
    ips = set()

    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_DGRAM):
            ip = info[4][0]
            if not ip.startswith(LOOPBACK_PREFIX):
                ips.add(ip)
    except Exception:
        logging.debug("Não foi possível resolver IPs de rede via hostname.")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(LAN_DISCOVERY_TARGET)
            ip = sock.getsockname()[0]
            if ip and not ip.startswith(LOOPBACK_PREFIX):
                ips.add(ip)
    except Exception:
        logging.debug("Não foi possível descobrir IP de saída padrão.")

    return sorted(ips)
