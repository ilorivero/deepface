import os
from dataclasses import dataclass

from deepface_app.constants import (
    APP_DEBUG_ENV_VAR,
    APP_HOST_ENV_VAR,
    APP_PORT_ENV_VAR,
    BOOLEAN_TRUE_VALUES,
    DEFAULT_APP_DEBUG,
    DEFAULT_APP_HOST,
    DEFAULT_APP_PORT,
    DEFAULT_THREADED,
    LOCALHOST_VALUE,
    LOOPBACK_HOST,
)


@dataclass(frozen=True)
class ServerSettings:
    host: str
    port: int
    debug: bool
    raw_host: str
    threaded: bool = DEFAULT_THREADED


def _parse_bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in BOOLEAN_TRUE_VALUES


def read_server_settings():
    raw_host = os.getenv(APP_HOST_ENV_VAR, DEFAULT_APP_HOST).strip()
    host = LOOPBACK_HOST if raw_host.lower() == LOCALHOST_VALUE else raw_host
    port = int(os.getenv(APP_PORT_ENV_VAR, str(DEFAULT_APP_PORT)).strip())
    debug = _parse_bool_env(APP_DEBUG_ENV_VAR, default=DEFAULT_APP_DEBUG)

    return ServerSettings(host=host, port=port, debug=debug, raw_host=raw_host)
