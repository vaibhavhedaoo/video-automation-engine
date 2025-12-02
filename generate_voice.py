from gtts import gTTS

def create_voice(text, output_path="voice.mp3", lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path

