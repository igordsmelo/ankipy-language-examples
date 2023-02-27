import json
import urllib.request
import time


########################################################################################################################
counter = time.time()
def count(func_took='function took'):
    print(f'{func_took}: {time.time() - counter}')


########################################################################################################################

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):

    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        pass
        # raise Exception(response['error'])
    return response['result']


def get_sentence(sentence):
    s = sentence.split('\t')  # 1 for japanese sentence, 3 for english translation
    return [s[1], s[3]]  # [hi, oi]


def remove_fromtext(text,remove=["&nbsp;", "<rt>.*?</rt>", "<rubytitle=.*?>", "<.*?>"], remove_furigana=True):
    ''''removes parts of the text from string using regex'''
    import re  # IMPORTS REGEX MODULE
    text = text.replace("<rt>", "[").replace("</rt>", "]")
    replace = []
    if len(remove) > 0:
        for r in ["&nbsp;", "<rt>.*?</rt>", "<rubytitle=.*?>", "<.*?>"]:
            replace += [*set(re.findall(r, text))]  # set removes duplicates from list. Went from hundreds to a few strs
        for r in replace:
            text = text.replace(r, '')
    if remove_furigana:
        for r in re.findall("\[.*?\]", text):
            text = text.replace(r, '')
    return text


########################################################################################################################
def find_language(text):
    from googletrans import Translator as gT
    lang = gT().detect(text).lang
    # print(lang)
    return lang

def text_to_speech(text, save_path):
    from gtts import gTTS
    from time import sleep as s
    tts = gTTS(text, lang=find_language(text))
    path = rf"{save_path}\{text.replace(' ', '_')[:20]}.mp3"
    tts.save(path)
    # s(5)
    return path

########################################################################################################################


########################################################################################################################
########################################################################################################################
########################################################################################################################
def create_deck(deck_name):
    invoke('createDeck', deck=deck_name)


def get_decks():
    print('got list of decks: {}'.format(invoke('deckNames')))


def search_notes(query_search):
    query_results = invoke('findNotes', query=query_search)
    return invoke('notesInfo', notes=query_results)


def update_note(note_ID, update_dict):
    invoke('updateNoteFields', note={'id': note_ID, 'fields': update_dict})


def add_tag(note_ID, tag):
    invoke('addTags', notes=[note_ID], tags=tag)

########################################################################################################################
########################################################################################################################
########################################################################################################################

jp_en = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-English - 2022-10-26.txt"
jp_fr = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-French - 2022-10-27.txt"
jp_sp = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Spanish - 2022-10-27.txt"
jp_kr = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Korean - 2022-10-27.txt"
jp_pt = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Portuguese - 2022-10-27.txt"
jp_es = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Esperanto - 2022-10-27.txt"
jp_ge = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-German - 2022-10-27.txt"
jp_cn = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Mandarin Chinese - 2022-10-27.txt"


def get_examples(word, database, word_limit=None, shuffle=False):
    import random
    database = open(database, encoding="utf8").readlines()
    random.shuffle(database) if shuffle else database.sort(key=len)  # shuffles list of lines.
    matching_sentences = [get_sentence(lines) for lines in database if all(w in lines for w in word.split(', '))]
    return matching_sentences[0:word_limit+1] if word_limit is not None else matching_sentences


def edit_anki_note(card, baselanguage='English', language='Word', sentence_field='Sentence', translation_field='English', audio_field='Sentence Audio'):
    print(f'\n\n\n############################################################')
    count('starting editing')

    l = card['fields'][language.title()]['value']
    sf = card['fields'][sentence_field]['value']
    print(f'sf = {sf}')

    try:
        # print(f"{language}:{l} \n {baselanguage}: {bl} \n {sentence_field}:{sf}")
        l = remove_fromtext(l, remove_furigana=True)  # l is a clean string
        # GETTING MORE LANGUAGE EXAMPLES IN IT ####################################
        examples = get_examples(l, jp_en)[0]
        ###########################################################################
        a = remove_fromtext(l, remove_furigana=False)  # a has furigana
        ###########################################################################

        updated_fields = {}  # dict containing all edits
        updated_fields[sentence_field] = examples[0].replace(l, f"<span class='AnkiPy'>{a}</span>") # JP Phrase
        updated_fields[translation_field] = examples[1]  # EN Phrase
        updated_fields[language] = a
        updated_fields[translation_field] = examples[1]

        sf = sf.replace('<span class="AnkiPy">','').replace('</span>','').replace(l,f"<span class='AnkiPy'>{l}</span>")
        updated_fields['Sentence'] = sf
        pth = r"C:\Users\Igor\AppData\Roaming\Anki2\User 1\collection.media"
        updated_fields[audio_field] = f'[sound:{text_to_speech(examples[0], pth)}]'

        count('editing notes now')
        update_note(card['noteId'], updated_fields)
        add_tag(card['noteId'], 'AnkiPy')  # invoke('addTags', notes=[ID, ID], tags='AnkiPy')
        ###########################################################################
        count(f'{l} changed')
        print(f'############################################################')
    except :
        count('edit attempt failed')
        add_tag(card['noteId'], 'AnkiPyNoExample')  # invoke('addTags', notes=[ID, ID], tags='AnkiPy')
        #print(f'{l} examples not found')
        pass


def filter_note_by_tag(notes, include=None, exclude=None):
    if include:
        notes = [n for n in notes if include in n['tags']]
    if exclude:
        notes = [n for n in notes if exclude not in n['tags']]
    return notes


queries = ["deck:Default::Downloaded::JLPT::N5", "deck:Default::Downloaded::JLPT::N4", "deck:Default::Downloaded::JLPT::N3", "deck:Default::Downloaded::JLPT::N2", "deck:Default::Downloaded::JLPT::N1"]
target_sentence_field = 'Japanese'
for q in queries:  # individual query terms
    notes = filter_note_by_tag(search_notes(q), exclude='AnkiPy') # searches query, filters it, assign to var
    notes = [n for n in notes if not n['fields'][target_sentence_field]['value']]
    print(f'there are {len(notes)} notes to edit')
    for note in notes:  # individual notes
          edit_anki_note(note, language='Expression', sentence_field=target_sentence_field)  # starts editing it
    print(f'finished fucking {q}')


# edit_anki_note(language='Expression', sentence_field='Japanese')

# STARTS HERE###########################################################################################################
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
# FINISHES HERE#########################################################################################################

# match_translation('東京へ行くのに２時間かかった', 'It took two hours to go to Tokyo')  # test
# abc = get_examples('clean', jp_en)
# grammar = match_translation(abc[1][0], abc[1][1])

#todo: change parameters