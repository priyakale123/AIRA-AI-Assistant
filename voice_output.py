import pyttsx3


def speak(text):

    print("AIRA:", text)

    engine = pyttsx3.init("sapi5")

    voices = engine.getProperty("voices")

    # Microsoft Zira
    for voice in voices:
        if "Zira" in voice.name:
            engine.setProperty("voice", voice.id)
            break

    # AIRA personality
    engine.setProperty("rate", 140)
    engine.setProperty("volume", 0.85)

    engine.say(text)
    engine.runAndWait()

    del engine