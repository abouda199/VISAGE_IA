
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiOrchestrator:
    """
    Analyse les commandes de VISAGE-AI
    et sélectionne une action structurée.
    """

    ALLOWED_ACTIONS = {
        "music",
        "website",
        "search",
        "application",
        "chat"
    }

    def __init__(self):
        api_key = (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        if not api_key:
            raise RuntimeError(
                "Clé Gemini introuvable. "
                "Vérifie GEMINI_API_KEY dans .env."
            )

        self.client = genai.Client(
            api_key=api_key
        )

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
Tu es l'orchestrateur d'un assistant vocal Windows
nommé VISAGE-AI.

Ta tâche est d'analyser la transcription Whisper
et de choisir une action.

ACTIONS AUTORISÉES :

music :
L'utilisateur souhaite écouter une chanson ou un artiste.

website :
L'utilisateur souhaite ouvrir un site Internet.

search :
L'utilisateur souhaite effectuer une recherche Google.

application :
L'utilisateur souhaite lancer une application Windows.

chat :
L'utilisateur pose une question ou souhaite discuter.

Réponds uniquement avec un objet JSON :
{
    "action": "music",
    "target": "Shape of You Ed Sheeran"
}

RÈGLES :

1. Ne déclenche pas d'action pour une simple question.
2. Corrige les erreurs évidentes de transcription.
3. Ne devine pas un titre lorsque plusieurs choix sont possibles.
4. Pour music, target contient le titre et l'artiste si connus.
5. Pour website, target contient le nom du site.
6. Pour application, target contient le nom de l'application.
7. Pour search, target contient la requête.
8. Ne prétends jamais avoir exécuté une action.
9. N'invente pas de commandes système.
10. En cas de doute sur l'intention, choisis chat.
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
                "La réponse Gemini n'est pas un objet JSON."
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

        return {
            "action": action,
            "target": target
        }
