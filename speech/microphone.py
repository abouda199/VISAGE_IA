import sounddevice as sd
import numpy as np

from scipy.io.wavfile import write
from scipy.signal import resample_poly


class MicrophoneRecorder:

    def __init__(
        self,
        sample_rate=48000,
        target_sample_rate=16000,
        channels=1,
        device_id=9
    ):
        self.sample_rate = sample_rate
        self.target_sample_rate = target_sample_rate
        self.channels = channels
        self.device_id = device_id

    def record(
        self,
        duration=5,
        filename="user_voice.wav"
    ):

        print()
        print("================================")
        print("🎤 ECOUTE")
        print("Parlez maintenant...")
        print("================================")

        # -----------------------------------------------
        # Enregistrement à la fréquence native du micro
        # -----------------------------------------------

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            device=self.device_id
        )

        sd.wait()

        print()
        print("✓ Enregistrement terminé")

        # -----------------------------------------------
        # Mesure du signal original
        # -----------------------------------------------

        peak = float(np.max(np.abs(audio)))

        rms = float(
            np.sqrt(np.mean(audio ** 2))
        )

        print("Niveau PEAK :", round(peak, 4))
        print("Niveau RMS  :", round(rms, 4))

        # -----------------------------------------------
        # Passage mono
        # -----------------------------------------------

        audio = audio.flatten()

        # -----------------------------------------------
        # 48 kHz -> 16 kHz
        # -----------------------------------------------

        if self.sample_rate != self.target_sample_rate:

            print(
                f"Conversion : "
                f"{self.sample_rate} Hz -> "
                f"{self.target_sample_rate} Hz"
            )

            audio = resample_poly(
                audio,
                self.target_sample_rate,
                self.sample_rate
            )

        # -----------------------------------------------
        # Protection contre saturation
        # -----------------------------------------------

        audio = np.clip(
            audio,
            -1.0,
            1.0
        )

        # -----------------------------------------------
        # Conversion WAV 16 bits
        # -----------------------------------------------

        audio_int16 = np.int16(
            audio * 32767
        )

        # -----------------------------------------------
        # Sauvegarde
        # -----------------------------------------------

        write(
            filename,
            self.target_sample_rate,
            audio_int16
        )

        print(
            "✓ Audio sauvegardé :",
            filename
        )

        print(
            "✓ Fréquence WAV :",
            self.target_sample_rate,
            "Hz"
        )

        return filename