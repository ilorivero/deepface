import platform
import time

import cv2
import numpy as np


class CameraService:
    def __init__(self):
        self.cap = self.open_camera()
        self.camera_available = self.cap is not None

    def open_camera(self):
        preferred_backends = []
        current_system = platform.system().lower()

        if current_system == "darwin":
            preferred_backends = [cv2.CAP_AVFOUNDATION]
        elif current_system == "windows":
            preferred_backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF]
        else:
            preferred_backends = [cv2.CAP_V4L2]

        for camera_index in (0, 1, 2):
            for backend in preferred_backends + [None]:
                camera = (
                    cv2.VideoCapture(camera_index)
                    if backend is None
                    else cv2.VideoCapture(camera_index, backend)
                )
                if camera.isOpened():
                    return camera
                camera.release()

        return None

    def release_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def build_placeholder_frame(self, message):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(
            frame,
            message,
            (20, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )
        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            return b""
        return buffer.tobytes()

    def generate_frames(self, process_frame_callback):
        while True:
            if self.cap is None:
                self.cap = self.open_camera()
                self.camera_available = self.cap is not None

            if self.cap is None:
                frame_bytes = self.build_placeholder_frame(
                    "Webcam indisponivel. Use o modo Upload de Arquivo."
                )
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
                time.sleep(1)
                continue

            success, frame = self.cap.read()

            if not success:
                self.release_camera()
                self.camera_available = False
                frame_bytes = self.build_placeholder_frame(
                    "Falha na webcam. Tentando reconectar..."
                )
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
                time.sleep(0.5)
                continue

            self.camera_available = True
            processed_frame = process_frame_callback(frame)
            success, buffer = cv2.imencode(".jpg", processed_frame)
            if not success:
                continue

            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
