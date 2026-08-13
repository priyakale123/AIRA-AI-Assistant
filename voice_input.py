import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer


MODEL_PATH = r".\model\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    audio_queue.put(bytes(indata))


def listen():
    print("Loading AIRA's voice system...")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    print("AIRA is listening... 🎤")
    print("Speak something...")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):
        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                if text:
                    return text


if __name__ == "__main__":
    text = listen()
    print("You said:", text)