
import re
import unicodedata


class EmotionDetector:

    def __init__(self):
        self.emotion_keywords = {
            "happy": [
                "heureux", "heureuse", "content",
                "contente", "joie", "super",
                "genial", "excellent", "merci",
                "j adore", "ravi", "ravie"
            ],
            "sad": [
                "triste", "malheureux", "malheureuse",
                "pleure", "deprime", "deprimee",
                "chagrin", "decu", "decue"
            ],
            "angry": [
                "colere", "enerve", "enervee",
                "furieux", "furieuse", "fache",
                "fachee", "injuste"
            ],
            "surprised": [
                "surpris", "surprise", "incroyable",
                "impossible", "wow", "etonnant"
            ],
            "thinking": [
                "pourquoi", "comment", "explique",
                "question", "reflechir", "penses tu"
            ]
        }

    def normalize(self, text):
        text = text.lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(
            char for char in text
            if unicodedata.category(char) != "Mn"
        )
        text = re.sub(r"[^\w\s]", " ", text)
        return " ".join(text.split())

    def detect(self, text):
        normalized = self.normalize(text)
        padded = f" {normalized} "

        scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            scores[emotion] = sum(
                1 for keyword in keywords
                if f" {keyword} " in padded
            )

        best_emotion = max(scores, key=scores.get)

        if scores[best_emotion] == 0:
            return "neutral"

        return best_emotion
