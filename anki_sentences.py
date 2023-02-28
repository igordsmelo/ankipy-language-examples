import time

from data import jp_en, get_examples
from formatting import remove_fromtext
from requests import search_notes, update_note, add_tag
from text_and_speech import text_to_speech

########################################################################################################################
counter = time.time()
def count(func_took='function took'):
    print(f'{func_took}: {time.time() - counter}')


########################################################################################################################


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