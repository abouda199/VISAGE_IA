
import time
from collections import deque

import numpy as np
import sounddevice as sd
import webrtcvad

from scipy.signal import resample_poly
from faster_whisper import WhisperModel


class VisageSTT:

    def __init__(self):
        print("Chargement de Whisper...")

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        self.device = 9
        self.record_rate = 48000
        self.whisper_rate = 16000

        self.vad = webrtcvad.Vad(2)

        print("Whisper prêt !")

    def transcribe(self, audio):
        audio = np.asarray(
            audio,
            dtype=np.float32
        ).flatten()

        if audio.size == 0:
            return ""

        rms = float(np.sqrt(np.mean(audio ** 2)))

        if rms < 0.001:
            return ""

        segments, _ = self.model.transcribe(
            audio,
            language="fr",
            beam_size=5,
            vad_filter=True,
            initial_prompt=(
                "Conversation en français avec VISAGE-AI. "
                "Intelligence artificielle, Python, "
                "machine learning et informatique."
            ),
            condition_on_previous_text=False
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

    def listen(self, duration=5):
        print("Enregistrement manuel...")

        audio = sd.rec(
            int(duration * self.record_rate),
            samplerate=self.record_rate,
            channels=1,
            dtype="float32",
            device=self.device
        )

        sd.wait()

        audio = resample_poly(
            audio.flatten(),
            1,
            3
        ).astype(np.float32)

        return self.transcribe(audio)

    def listen_auto(
        self,
        stop_event=None,
        max_duration=15,
        silence_duration=0.9,
        start_timeout=10
    ):
        frame_ms = 30

        native_frame = int(
            self.record_rate * frame_ms / 1000
        )

        target_frame = int(
            self.whisper_rate * frame_ms / 1000
        )

        pre_buffer = deque(maxlen=10)
        chunks = []

        started = False
        voice_frames = 0
        silence_frames = 0

        silence_limit = max(
            1,
            int(silence_duration * 1000 / frame_ms)
        )

        start_time = time.monotonic()
        speech_start = None

        print("En attente de parole...")

        with sd.InputStream(
            samplerate=self.record_rate,
            device=self.device,
            channels=1,
            dtype="float32",
            blocksize=native_frame
        ) as stream:

            while True:
                if (
                    stop_event is not None
                    and stop_event.is_set()
                ):
                    return ""

                data, overflowed = stream.read(
                    native_frame
                )

                if overflowed:
                    print("Attention : débordement audio.")

                audio16 = resample_poly(
                    data[:, 0],
                    1,
                    3
                ).astype(np.float32)

                if len(audio16) != target_frame:
                    continue

                pcm16 = (
                    np.clip(audio16, -1.0, 1.0)
                    * 32767
                ).astype(np.int16).tobytes()

                is_voice = self.vad.is_speech(
                    pcm16,
                    self.whisper_rate
                )

                if not started:
                    pre_buffer.append(audio16)

                    if is_voice:
                        voice_frames += 1
                    else:
                        voice_frames = 0

                    if voice_frames >= 2:
                        started = True
                        speech_start = time.monotonic()

                        chunks.extend(pre_buffer)

                        print(" Parole détectée !")

                    elif (
                        time.monotonic() - start_time
                        >= start_timeout
                    ):
                        return ""

                else:
                    chunks.append(audio16)

                    if is_voice:
                        silence_frames = 0
                    else:
                        silence_frames += 1

                    if silence_frames >= silence_limit:
                        break

                    if (
                        time.monotonic() - speech_start
                        >= max_duration
                    ):
                        break

        if not chunks:
            return ""

        audio = np.concatenate(chunks)

        print(" Transcription en cours...")

        return self.transcribe(audio)
