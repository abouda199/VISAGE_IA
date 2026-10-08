
import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


class VisageLLM:

    def __init__(self):
        # Charger la clé API
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY introuvable dans le fichier .env"
            )

        # Initialisation de Gemini
        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-3.5-flash-lite"

        # Historique de conversation
        self.history = []

        # Configuration des tentatives
        self.max_retries = 3

        # Instructions du cerveau IA
        self.instructions = """
Tu es VISAGE-AI, un assistant conversationnel
incarné par un visage robotique animé.

Ton objectif est de comprendre le contexte
global des messages de l'utilisateur.

Tu dois :

1. Comprendre le sens du paragraphe complet.
2. Identifier les émotions implicites.
3. Comprendre les négations, les sous-entendus
   et les intentions.
4. Tenir compte de l'historique de conversation.
5. Générer une réponse naturelle et intelligente.
6. Choisir une expression adaptée au visage robotique.

Émotions disponibles :
- neutral
- happy
- sad
- angry
- surprised
- thinking

L'émotion représente la réaction appropriée
du visage à la situation décrite.

L'intensité est comprise entre 0.0 et 1.0.

Ne te limite jamais à des mots-clés.

Réponds en français.

Retourne uniquement un objet JSON contenant :
emotion, intensity, intent, response.
"""

        self.response_schema = {
            "type": "OBJECT",
            "properties": {
                "emotion": {
                    "type": "STRING",
                    "enum": [
                        "neutral",
                        "happy",
                        "sad",
                        "angry",
                        "surprised",
                        "thinking"
                    ]
                },
                "intensity": {
                    "type": "NUMBER"
                },
                "intent": {
                    "type": "STRING"
                },
                "response": {
                    "type": "STRING"
                }
            },
            "required": [
                "emotion",
                "intensity",
                "intent",
                "response"
            ]
        }

    # ========================================================
    # ANALYSE DU MESSAGE
    # ========================================================

    def analyze(self, message):

        if not message or not message.strip():
            raise ValueError("Le message est vide.")

        message = message.strip()

        contents = self.history + [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=message)
                ]
            )
        ]

        result = None

        # ====================================================
        # APPEL GEMINI AVEC TENTATIVES AUTOMATIQUES
        # ====================================================

        for attempt in range(self.max_retries):

            try:
                print(
                    f"Gemini : tentative "
                    f"{attempt + 1}/{self.max_retries}"
                )

                result = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self.instructions,
                        response_mime_type="application/json",
                        response_schema=self.response_schema,
                        temperature=0.5
                    )
                )

                break

            except errors.ServerError as e:

                # Ne réessayer que pour les erreurs 503
                if e.code != 503:
                    raise

                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        "Gemini reste indisponible après "
                        "plusieurs tentatives."
                    ) from e

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Serveur Gemini surchargé (503). "
                    f"Nouvelle tentative dans "
                    f"{wait_time} secondes..."
                )

                time.sleep(wait_time)

        # ====================================================
        # VALIDATION DE LA REPONSE
        # ====================================================

        if result is None or not result.text:
            raise RuntimeError(
                "Gemini n'a retourné aucune réponse."
            )

        data = json.loads(result.text)

        required_fields = [
            "emotion",
            "intensity",
            "intent",
            "response"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(
                    f"Champ manquant dans la réponse : {field}"
                )

        allowed_emotions = {
            "neutral",
            "happy",
            "sad",
            "angry",
            "surprised",
            "thinking"
        }

        if data["emotion"] not in allowed_emotions:
            data["emotion"] = "neutral"

        data["intensity"] = max(
            0.0,
            min(1.0, float(data["intensity"]))
        )

        # ====================================================
        # MEMOIRE DE CONVERSATION
        # ====================================================

        self.history.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=message)
                ]
            )
        )

        self.history.append(
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text=json.dumps(
                            data,
                            ensure_ascii=False
                        )
                    )
                ]
            )
        )

        return data
