import json
import queue
import sounddevice as sd


from vosk import Model, KaldiRecognizer
from voice_output import speak


# -----------------------------
# Configuration
# -----------------------------

MODEL_PATH = r".\model\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000


# -----------------------------
# AIRA Voice
# -----------------------------



# -----------------------------
# Load Vosk model ONCE
# -----------------------------

print("Loading AIRA's voice system...")

model = Model(MODEL_PATH)

print("Voice system ready.")


# -----------------------------
# Speech Recognition
# -----------------------------

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):

    if status:
        print(status)

    audio_queue.put(bytes(indata))


def listen():

    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )

    print("\n🎤 AIRA is listening...")
    print("Speak clearly...")

    try:

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=4000,
            dtype="int16",
            channels=1,
            device=1,
            callback=audio_callback
        ):

            while True:

                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get(
                        "text",
                        ""
                    ).strip()

                    if text:
                        return text

    except KeyboardInterrupt:

        return "exit"


# -----------------------------
# Basic AIRA Brain
# -----------------------------

def process_command(text):

    text = text.lower().strip()


    if "hello" in text or "hi" in text:

        return "Hello. I'm here."


    elif "who are you" in text:

        return "I am AIRA, your personal AI assistant."


    elif "how are you" in text:

        return "I'm doing great. Thank you for asking."


    elif "good morning" in text:

        return "Good morning. I hope you have a wonderful day."


    elif "good night" in text:

        return "Good night. Sleep well."


    elif "bye" in text:

        return "Goodbye. I'll be here when you need me."


    else:

        return "I heard you, but I don't understand that command yet."


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    speak("Hello. I am AIRA.")

    try:

        while True:

            user_text = listen()

            if user_text == "exit":
                break

            print("You:", user_text)

            response = process_command(user_text)

            print("Response:", response)

            speak(response)

    except KeyboardInterrupt:

        print("\nAIRA stopped.")

    finally:

        print("AIRA closed.")