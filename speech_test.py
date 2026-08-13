import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = r".\model\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"

print("Loading Vosk model...")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)

    audio_queue.put(bytes(indata))


print("\n🎤 Speak something in English...")
print("Press Ctrl+C to stop.\n")

with sd.RawInputStream(
    samplerate=16000,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):
    while True:
        data = audio_queue.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())

            text = result.get("text", "")

            if text:
                print("You said:", text)