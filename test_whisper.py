from speech.microphone import MicrophoneRecorder
from speech.stt import SpeechToText


print()
print("================================")
print("TEST WHISPER BASE - VISAGE AI")
print("================================")


# Microphone
microphone = MicrophoneRecorder(
    device_id=9
)


# Whisper BASE local
print()
print("Initialisation de Whisper...")

whisper = SpeechToText(
    model_path="assets/models/faster-whisper-base"
)

print("✓ Whisper initialisé")


# Enregistrement
audio_file = microphone.record(
    duration=5,
    filename="voice_whisper.wav"
)


# Transcription
text = whisper.transcribe(
    audio_file
)


# Résultat
print()
print("================================")
print("TEXTE RECONNU")
print("================================")

if text:
    print(text)
else:
    print("Aucun texte détecté.")

print("================================")
print("TEST TERMINE")
print("================================")