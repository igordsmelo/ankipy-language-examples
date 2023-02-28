def find_language(text):
    from googletrans import Translator as gT
    lang = gT().detect(text).lang
    # print(lang)
    return lang


def text_to_speech(text, save_path):
    from gtts import gTTS
    tts = gTTS(text, lang=find_language(text))
    path = rf"{save_path}\{text.replace(' ', '_')[:20]}.mp3"
    tts.save(path)
    # s(5)
    return path
