
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class GeminiOrchestrator:

    ALLOWED_ACTIONS = {
        "music",
        "website",
        "search",
        "application",
        "iot",
        "chat"
    }

    def __init__(self):
        api_key = (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        if not api_key:
            raise RuntimeError(
                "Clé API Gemini introuvable dans .env"
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

    def analyze(self, message):
        message = str(message).strip()

        if not message:
            return {
                "action": "chat",
                "target": ""
            }

        system_instruction = """
Tu es Gemini Orchestrator, le système intelligent
de routage de l'assistant vocal VISAGE-AI.

Tu analyses une transcription vocale Whisper et
sélectionnes UNE action parmi :

1. music
   Jouer une chanson sur YouTube.
   target = titre de la chanson et artiste.

2. website
   Ouvrir un site Internet.
   target = nom du site.

3. search
   Effectuer une recherche Google.
   target = requête de recherche.

4. application
   Ouvrir une application Windows.
   target = nom de l'application.

5. iot
   Contrôler une lumière virtuelle.
   target doit être exactement :
   "light:on" ou "light:off"

6. chat
   Conversation normale ou question générale.
   target = ""

COMMANDES IOT :

"Allume la lumière"
-> {"action":"iot","target":"light:on"}

"Ouvre la lumière"
-> {"action":"iot","target":"light:on"}

"Active la lumière"
-> {"action":"iot","target":"light:on"}

"Éteins la lumière"
-> {"action":"iot","target":"light:off"}

"Ferme la lumière"
-> {"action":"iot","target":"light:off"}

"Désactive la lumière"
-> {"action":"iot","target":"light:off"}

"VISAGE, ouvre la lumière"
-> {"action":"iot","target":"light:on"}

RÈGLES :
- Réponds uniquement avec un objet JSON.
- Ne prétends jamais avoir exécuté une action.
- Ne déclenche pas d'action pour une simple question.
- Corrige les erreurs de transcription évidentes.
- N'invente aucune commande système.
- Pour iot, utilise uniquement light:on ou light:off.
- En cas de doute, choisis chat.

FORMAT DE RÉPONSE :

{
    "action": "iot",
    "target": "light:on"
}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0,
                response_mime_type="application/json"
            )
        )

        if not response.text:
            raise RuntimeError(
                "Gemini a retourné une réponse vide."
            )

        data = json.loads(response.text)

        if not isinstance(data, dict):
            raise ValueError(
                "Réponse Gemini invalide."
            )

        action = str(
            data.get("action", "chat")
        ).lower().strip()

        target = str(
            data.get("target") or ""
        ).strip()

        if action not in self.ALLOWED_ACTIONS:
            action = "chat"
            target = ""

        if action == "iot":
            if target not in {"light:on", "light:off"}:
                action = "chat"
                target = ""

        return {
            "action": action,
            "target": target
        }
