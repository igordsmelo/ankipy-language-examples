# from gtts import gTTS
# from googletrans import Translator as gT
# import nltk  # nltk.download('averaged_perceptron_tagger')  # dependency


def detect_language(text: str):
    """
    Uses Google Translate to identify in what language is the given text.
    :param text: the text you'd like to be checked.
    :return: language
    """
    from googletrans import Translator as gT
    detected_language = gT().detect(text).lang
    return detected_language


def text_to_speech(text, save_path):
    from gtts import gTTS
    tts = gTTS(text, lang=detect_language(text))
    tts_audio_path = rf"{save_path}\{text.replace(' ', '_')[:20]}.mp3"
    tts.save(tts_audio_path)
    return tts_audio_path

############################################################

def what_is_this_word(word_or_sentence, filter_word=None):
    """finds out whether word(s) in a string are verbs, nouns, adjectives, etc."""
    import nltk  # nltk.download('averaged_perceptron_tagger')  # dependency
    text_result = nltk.pos_tag(nltk.word_tokenize(word_or_sentence))  # gets individual words then check what they are.
    if filter_word is not None:
        text_result = [i for i in text_result if i[0].lower() == filter_word]
    return text_result
