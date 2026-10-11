
import webbrowser

from yt_dlp import YoutubeDL


class MusicAgent:
    """
    Recherche une chanson sur YouTube et ouvre
    directement la vidéo correspondante.
    """

    def __init__(self):
        self.platform = "YouTube"

    def execute(self, song):

        song = str(song).strip()

        if not song:
            return {
                "handled": True,
                "agent": "MusicAgent",
                "response": "Quelle chanson veux-tu écouter ?",
                "emotion": "neutral"
            }

        print("\n" + "=" * 55)
        print("MUSIC AGENT ACTIVÉ")
        print("Recherche :", song)

        try:
            options = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
                "skip_download": True,
                "noplaylist": True,
                "socket_timeout": 12,
            }

            # Recherche la première vidéo YouTube
            with YoutubeDL(options) as ydl:

                results = ydl.extract_info(
                    f"ytsearch1:{song}",
                    download=False
                )

            entries = results.get("entries") or []

            if not entries:
                return {
                    "handled": True,
                    "agent": "MusicAgent",
                    "response": (
                        f"Je n'ai trouvé aucune vidéo "
                        f"pour {song}."
                    ),
                    "emotion": "sad"
                }

            video = entries[0]

            video_id = video.get("id")
            video_title = video.get("title", song)

            if not video_id:
                raise RuntimeError(
                    "Identifiant vidéo introuvable."
                )

            # URL directe de la vidéo
            video_url = (
                "https://www.youtube.com/watch?v="
                + video_id
            )

            print("Vidéo trouvée :", video_title)
            print("URL directe :", video_url)

            # Ouvre directement la vidéo
            opened = webbrowser.open(
                video_url,
                new=2,
                autoraise=True
            )

            if not opened:
                raise RuntimeError(
                    "Impossible d'ouvrir le navigateur."
                )

            print("Vidéo ouverte avec succès.")
            print("=" * 55)

            return {
                "handled": True,
                "agent": "MusicAgent",
                "response": (
                    f"J'ouvre directement {video_title} "
                    "sur YouTube."
                ),
                "emotion": "happy"
            }

        except Exception as error:

            print("Erreur MusicAgent :", error)

            return {
                "handled": True,
                "agent": "MusicAgent",
                "response": (
                    "Je n'ai pas réussi à ouvrir "
                    "la chanson sur YouTube."
                ),
                "emotion": "sad"
            }
