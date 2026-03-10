import logging

import cv2
from deepface import DeepFace


class FaceAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.emotion_map = {
            "angry": "Zangado",
            "disgust": "Nojo",
            "fear": "Medo",
            "happy": "Feliz",
            "neutral": "Neutro",
            "sad": "Triste",
            "surprise": "Surpresa",
        }
        self.ethnicity_map = {
            "white": "Branco",
            "black": "Negro",
            "asian": "Asiático",
            "indian": "Indiano",
            "middle eastern": "Oriente Médio",
            "latino hispanic": "Latino/Hispânico",
        }

    def format_emotion_details(self, emotion_scores):
        if not emotion_scores:
            return []

        sorted_scores = sorted(
            emotion_scores.items(), key=lambda item: item[1], reverse=True
        )
        return [
            {
                "emotion": self.emotion_map.get(name, name),
                "score": round(float(score), 1),
            }
            for name, score in sorted_scores
        ]

    def map_attributes(self, attributes):
        dominant_emotion_en = attributes["dominant_emotion"]
        dominant_emotion_pt = self.emotion_map.get(
            dominant_emotion_en, dominant_emotion_en
        )
        emotion_details = self.format_emotion_details(attributes.get("emotion", {}))
        dominant_gender = attributes.get("dominant_gender", "")

        return {
            "age": f"{attributes['age']} anos",
            "gender": "Masculino" if dominant_gender == "Man" else "Feminino",
            "emotion": dominant_emotion_pt,
            "ethnicity": self.ethnicity_map.get(
                attributes["dominant_race"], attributes["dominant_race"]
            ),
            "emotion_details": emotion_details,
        }

    def analyze_face(self, frame):
        latest_attributes = None

        try:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)

            for (x, y, w, h) in faces:
                face_region = frame[y : y + h, x : x + w]
                result = DeepFace.analyze(
                    face_region,
                    actions=["age", "gender", "emotion", "race"],
                    enforce_detection=False,
                )
                attributes = result[0] if isinstance(result, list) else result
                latest_attributes = self.map_attributes(attributes)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Emocao: {latest_attributes['emotion']}",
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )

            return frame, latest_attributes

        except Exception as exc:
            logging.error("Erro na análise facial: %s", exc)
            return frame, None
