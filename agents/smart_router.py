
import unicodedata

from agents.gemini_orchestrator import GeminiOrchestrator
from agents.music_agent import MusicAgent
from agents.web_agent import WebAgent
from agents.app_agent import AppAgent


def normalize_name(text):
    text = str(text).lower().strip()

    text = unicodedata.normalize(
        "NFKD", text
    )

    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    return " ".join(text.split())


class SmartAgentRouter:
    """
    Orchestrateur intelligent :
    Whisper -> Gemini -> Agent -> Action.
    """

    def __init__(self):
        self.orchestrator = GeminiOrchestrator()

        self.music_agent = MusicAgent()
        self.web_agent = WebAgent()
        self.app_agent = AppAgent()

    def _match_allowed_name(self, target, allowed):
        normalized_target = normalize_name(target)

        for name in allowed:
            if normalize_name(name) == normalized_target:
                return name

        return None

    def execute(self, message):
        print("\n" + "=" * 55)
        print("[SMART ROUTER] Commande :", message)

        decision = self.orchestrator.analyze(message)

        action = decision["action"]
        target = decision["target"]

        print("[GEMINI] Action :", action)
        print("[GEMINI] Cible :", target)

        if action == "chat":
            return {
                "handled": False
            }

        if not target:
            return {
                "handled": True,
                "agent": "GeminiOrchestrator",
                "response": (
                    "Peux-tu préciser ce que "
                    "tu souhaites faire ?"
                ),
                "emotion": "neutral"
            }

        # ================================================
        # MUSIC AGENT
        # ================================================

        if action == "music":
            print("[SMART ROUTER] -> MusicAgent")

            return self.music_agent.execute(
                target
            )

        # ================================================
        # WEB SEARCH AGENT
        # ================================================

        if action == "search":
            print("[SMART ROUTER] -> WebAgent")

            return self.web_agent.search_google(
                target
            )

        # ================================================
        # WEBSITE AGENT
        # ================================================

        if action == "website":
            website = self._match_allowed_name(
                target,
                self.web_agent.websites
            )

            if website:
                print(
                    "[SMART ROUTER] -> WebAgent :",
                    website
                )

                return self.web_agent.open_website(
                    website
                )

            return {
                "handled": True,
                "agent": "WebAgent",
                "response": (
                    f"Le site {target} n'est pas "
                    "dans ma liste de sites autorisés."
                ),
                "emotion": "neutral"
            }

        # ================================================
        # WINDOWS APPLICATION AGENT
        # ================================================

        if action == "application":
            application = self._match_allowed_name(
                target,
                self.app_agent.applications
            )

            if application:
                print(
                    "[SMART ROUTER] -> AppAgent :",
                    application
                )

                return self.app_agent.execute(
                    application
                )

            return {
                "handled": True,
                "agent": "AppAgent",
                "response": (
                    f"L'application {target} n'est pas "
                    "dans ma liste autorisée."
                ),
                "emotion": "neutral"
            }

        return {
            "handled": False
        }
