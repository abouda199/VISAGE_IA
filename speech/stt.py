from faster_whisper import WhisperModel
import os


class SpeechToText:

    def __init__(
        self,
        model_path="assets/models/faster-whisper-base"
    ):

        print()
        print("================================")
        print("CHARGEMENT DE FASTER-WHISPER")
        print("================================")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Modèle Whisper introuvable : {model_path}"
            )

        print("Modèle local :", model_path)

        self.model = WhisperModel(
            model_path,
            device="cpu",
            compute_type="int8"
        )

        print("✓ faster-Whisper prêt")

    def transcribe(self, audio_file):

        print()
        print("================================")
        print("🤔 TRANSCRIPTION...")
        print("================================")

        segments, info = self.model.transcribe(
            audio_file,
            language="fr",
            beam_size=5,
            vad_filter=False,
            condition_on_previous_text=False
        )
        

        texts = []

        for segment in segments:
            text = segment.text.strip()

            if text:
                texts.append(text)

        final_text = " ".join(texts).strip()

        return final_text