import pyttsx3
import time

def speak(text):
    engine = pyttsx3.init("sapi5")

    voices = engine.getProperty("voices")

    for voice in voices:
        print(voice.id, voice.name)

    for voice in voices:
        if "Zira" in voice.name:
            engine.setProperty("voice", voice.id)
            break

    engine.setProperty("rate", 140)
    engine.setProperty("volume", 0.85)

    engine.say(text)
    engine.runAndWait()

    del engine


print("TEST 1")
speak("Hello. I am AIRA.")

time.sleep(2)

print("TEST 2")
speak("This is my second response.")

time.sleep(2)

print("TEST 3")
speak("This is my third response.")