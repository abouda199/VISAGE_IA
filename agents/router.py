
import re
import unicodedata

from agents.music_agent import MusicAgent
from agents.web_agent import WebAgent
from agents.app_agent import AppAgent


def normalize(text):
    text = str(text).lower().strip()
    text = unicodedata.normalize("NFKD", text)

    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    text = text.replace("’", "'")
    text = text.replace("«", " ")
    text = text.replace("»", " ")

    return re.sub(r"\s+", " ", text).strip(" .,!?;:")


class AgentRouter:

    def __init__(self):
        self.music_agent = MusicAgent()
        self.web_agent = WebAgent()
        self.app_agent = AppAgent()

    def execute(self, message):

        text = normalize(message)

        print("\n[ROUTER] Texte reçu :", text)

        if not text:
            return {"handled": False}

        # Supprimer les introductions fréquentes
        prefixes = [
            r"^(?:hey|salut|bonjour)\s+visage(?:\s*ai)?[\s,:-]*",
            r"^visage(?:\s*ai)?[\s,:-]*",
            r"^toi[\s,:-]+",
            r"^s'il te plait[\s,:-]+",
            r"^est-ce que tu peux[\s,:-]+",
            r"^peux-tu[\s,:-]+",
            r"^tu peux[\s,:-]+",
            r"^s'il te plait[\s,:-]+",
        ]

        # Plusieurs préfixes peuvent se suivre
        for _ in range(5):
            old_text = text

            for prefix in prefixes:
                text = re.sub(
                    prefix,
                    "",
                    text
                ).strip()

            if text == old_text:
                break

        print("[ROUTER] Commande nettoyée :", text)

        # ====================================================
        # MUSIQUE
        # ====================================================

        music_patterns = [
            r"^(?:ouvre|lance|mets?|joue|ecoute)"
            r"(?:-moi|\s+moi)?\s+"
            r"(?:(?:la|le|une|un|de la)\s+)?"
            r"(?:musique|chanson|titre|morceau)\s+"
            r"(.+)$",

            r"^(?:mets?|joue|lance|ecoute)"
            r"(?:-moi|\s+moi)?\s+"
            r"(.+?)\s+sur youtube$",

            r"^ouvre(?:-moi|\s+moi)?\s+"
            r"(.+?)\s+sur youtube$",
        ]

        for pattern in music_patterns:
            match = re.match(pattern, text)

            if match:
                song = match.group(1).strip()

                song = re.sub(
                    r"^(?:de|du|des|d'|au)\s*",
                    "",
                    song
                ).strip()

                song = re.sub(
                    r"\s+s'il te plait$",
                    "",
                    song
                ).strip()

                if not song:
                    return {
                        "handled": True,
                        "agent": "MusicAgent",
                        "response": "Quelle chanson veux-tu écouter ?",
                        "emotion": "neutral"
                    }

                print("[ROUTER] MUSIC AGENT :", song)

                return self.music_agent.execute(song)

        # ====================================================
        # RECHERCHE WEB
        # ====================================================

        search_patterns = [
            r"^(?:recherche|cherche|trouve)"
            r"(?:-moi|\s+moi)?\s+"
            r"(?:sur google\s+)?(.+)$",

            r"^fais une recherche\s+"
            r"(?:sur|de|pour)?\s*(.+)$",
        ]

        for pattern in search_patterns:
            match = re.match(pattern, text)

            if match:
                query = match.group(1).strip()

                print("[ROUTER] WEB SEARCH :", query)

                return self.web_agent.search_google(query)

        # ====================================================
        # SITES ET APPLICATIONS
        # ====================================================

        match = re.match(
            r"^(?:ouvre|lance|affiche|va sur)"
            r"(?:-moi|\s+moi)?\s+(.+)$",
            text
        )

        if match:
            target = match.group(1).strip()

            target = re.sub(
                r"^(?:le|la|les|l'|un|une)\s*",
                "",
                target
            ).strip()

            for website in self.web_agent.websites:
                if normalize(website) == target:
                    return self.web_agent.open_website(website)

            for application in self.app_agent.applications:
                if normalize(application) == target:
                    return self.app_agent.execute(application)

        # ====================================================
        # GEMINI : CONVERSATION ORDINAIRE
        # ====================================================

        print("[ROUTER] Aucun agent. Passage à Gemini.")

        return {"handled": False}
