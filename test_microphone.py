from speech.microphone import MicrophoneRecorder


print()
print("TEST MICROPHONE VISAGE-AI")
print()


microphone = MicrophoneRecorder(
    device_id=5
)


audio_file = microphone.record(
    duration=5,
    filename="test_micro.wav"
)


print()
print("==============================")
print("TEST TERMINE")
print("==============================")
print(
    "Fichier :",
    audio_file
)