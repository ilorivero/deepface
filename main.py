from deepface_app import create_app
from deepface_app.server import read_server_settings, run_server

app = create_app()


if __name__ == "__main__":
    settings = read_server_settings()
    run_server(app, settings)