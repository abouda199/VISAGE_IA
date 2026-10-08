
import asyncio
import os
import tempfile
import threading

import pygame
import edge_tts


class VisageTTS:

    def __init__(self):

        # Voix féminine française
        self.voice = "fr-FR-DeniseNeural"

        self.rate = "+0%"
        self.volume = "+0%"

        self.speaking = False
        self.lock = threading.Lock()

        if not pygame.mixer.get_init():
            pygame.mixer.init()

    async def generate_audio(self, text, path):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume
        )

        await communicate.save(path)

    def speak(self, text):

        if not text or not text.strip():
            return

        with self.lock:

            path = None

            try:

                with tempfile.NamedTemporaryFile(
                    suffix=".mp3",
                    delete=False
                ) as file:

                    path = file.name

                # Générer le fichier audio
                asyncio.run(
                    self.generate_audio(text, path)
                )

                # Lecture de la voix
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()

                self.speaking = True

                while pygame.mixer.music.get_busy():
                    pygame.time.wait(50)

            except Exception as e:

                print("Erreur TTS :", e)

            finally:

                self.speaking = False

                try:
                    pygame.mixer.music.unload()
                except pygame.error:
                    pass

                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    def speak_async(self, text):

        thread = threading.Thread(
            target=self.speak,
            args=(text,),
            daemon=True
        )

        thread.start()
