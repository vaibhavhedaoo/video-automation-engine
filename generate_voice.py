from gtts import gTTS

def create_voice(text, output_path="voice.mp3", lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)

    with open("voice.txt", "w") as f:
        f.write(text)

    return output_path
