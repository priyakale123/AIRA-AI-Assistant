import sounddevice as sd

print("Available microphones:")
print(sd.query_devices())

print("\nDefault input device:")
print(sd.query_devices(kind="input"))

print("\nMicrophone test starting...")

duration = 5
sample_rate = 44100

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()

print("Microphone recording completed successfully! 🎤") 