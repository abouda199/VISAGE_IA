
import threading

import pyttsx3
import pythoncom


class VisageTTS:

    def __init__(self):
        self.speaking = False
        self.lock = threading.Lock()

    def _speak(self, text):
        initialized = False

        try:
            pythoncom.CoInitialize()
            initialized = True

            engine = pyttsx3.init("sapi5")

            engine.setProperty("rate", 165)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")

            # Chercher une voix française
            for voice in voices:
                name = voice.name.lower()
                voice_id = voice.id.lower()

                if (
                    "french" in name
                    or "français" in name
                    or "fr-fr" in voice_id
                ):
                    engine.setProperty(
                        "voice",
                        voice.id
                    )
                    break

            print("🔊 VISAGE-AI parle...")

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("Erreur TTS :", e)

        finally:
            if initialized:
                pythoncom.CoUninitialize()

            with self.lock:
                self.speaking = False

    def speak_async(self, text):
        if not text or not text.strip():
            return False

        with self.lock:
            if self.speaking:
                return False

            self.speaking = True

        threading.Thread(
            target=self._speak,
            args=(text,),
            daemon=True
        ).start()

        return True
