
import webbrowser
from urllib.parse import quote_plus


class WebAgent:

    def __init__(self):

        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "linkedin": "https://www.linkedin.com",
            "gmail": "https://mail.google.com",
            "wikipedia": "https://fr.wikipedia.org",
            "chatgpt": "https://chatgpt.com",
            "stackoverflow": "https://stackoverflow.com",
            "colab": "https://colab.research.google.com",
            "google colab": "https://colab.research.google.com",
            "hugging face": "https://huggingface.co",
            "kaggle": "https://www.kaggle.com"
        }

    def open_website(self, website):

        website = website.strip().lower()

        url = self.websites.get(website)

        if not url:
            return {
                "handled": False
            }

        if not webbrowser.open(url):
            raise RuntimeError(
                "Impossible d'ouvrir le navigateur."
            )

        return {
            "handled": True,
            "agent": "WebAgent",
            "response": f"J'ouvre {website}.",
            "emotion": "happy"
        }

    def search_google(self, query):

        query = query.strip()

        if not query:
            return {
                "handled": True,
                "agent": "WebAgent",
                "response": (
                    "Que souhaites-tu rechercher ?"
                ),
                "emotion": "neutral"
            }

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        if not webbrowser.open(url):
            raise RuntimeError(
                "Impossible d'ouvrir le navigateur."
            )

        return {
            "handled": True,
            "agent": "WebAgent",
            "response": (
                f"Je recherche {query} sur Google."
            ),
            "emotion": "happy"
        }
