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
    return path

############################################################

def what_is_this_word(word_or_sentence, filter_word=None):
    """finds out whether word(s) in a string are verbs, nouns, adjectives, etc."""
    import nltk  # nltk.download('averaged_perceptron_tagger')  # dependency
    text_result = nltk.pos_tag(nltk.word_tokenize(word_or_sentence))  # gets individual words then check what they are.
    if filter_word is not None:
        text_result = [i for i in text_result if i[0].lower() == filter_word]
    return text_result


def match_translation(og_txt, eng_translation):
    """finds out what each word in two translated texts mean in the other language."""
    from googletrans import Translator as gT
    o_lang = gT().detect(og_txt).lang  # finds out which language the og_txt is in. ja, pt, etc.
    grammar_info = what_is_this_word(eng_translation)
    matches = []
    for w in grammar_info:  # for individual words in the english translation.
        try:
            translated_w = gT().translate(w[0], dest=o_lang).text  # if translated words match original text.
            if translated_w in og_txt:
                # found ('Tokyo', 'NNP') translation (東京) in 東京へ行くのに２時間かかった. Tokyo(東京) is a NNP
                print(f'{translated_w}({w[0]}) found in {og_txt}. \n{w[0]}({translated_w}) is a {w[1]}')
                if w[1] not in ['.', ',', '?', '!', '@', '|']:
                    matches.append([translated_w, w[0], w[1]])
            else:
                pass
                print(f"{translated_w} not in {og_txt}")
        except TypeError:
            pass
    return matches



# match_translation('東京へ行くのに２時間かかった', 'It took two hours to go to Tokyo')  # test
# abc = get_sentence_examples('clean', jp_en)
# grammar = match_translation(abc[1][0], abc[1][1])
