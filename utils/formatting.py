import time

from utils.data import get_sentence_examples, jp_en
from utils.text_and_speech import text_to_speech
from utils.anki_requests import update_note, add_tag


def remove_fromtext(text, remove=("&nbsp;", "<rt>.*?</rt>", "<rubytitle=.*?>", "<.*?>"), remove_furigana=True):
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
        for r in re.findall("\[.*?]", text):
            text = text.replace(r, '')
    return text


def split_example(sentence):
    """Formats individual sentence and its translation."""
    s = sentence.split('\t')  # 1 for original, 3 for translation
    return [s[1], s[3]]  # [hi, oi]


def edit_anki_note(card, language='Word', sentence_field='Sentence',
                   translation_field='English', audio_field='Sentence Audio'):
    print(f'\n\n\n############################################################')
    count('starting editing')

    l = card['fields'][language.title()]['value']
    sf = card['fields'][sentence_field]['value']
    print(f'sf = {sf}')
    try:
        # print(f"{language}:{l} \n {baselanguage}: {bl} \n {sentence_field}:{sf}")
        l = remove_fromtext(l)  # l is a clean string
        # GETTING MORE LANGUAGE EXAMPLES IN IT ####################################
        examples = get_sentence_examples(l, jp_en)[0]
        ###########################################################################
        a = remove_fromtext(l, remove_furigana=False)  # a has furigana
        ###########################################################################
        updated_fields = {sentence_field: examples[0].replace(l, f"<span class='AnkiPy'>{a}</span>"),
                          translation_field: examples[1], language: a}  # dict containing all edits
        sf = (sf.replace('<span class="AnkiPy">', '')
              .replace('</span>', '').replace(l, f"<span class='AnkiPy'>{l}</span>"))
        updated_fields['Sentence'] = sf
        pth = r"C:\Users\Igor\AppData\Roaming\Anki2\User 1\collection.media"
        updated_fields[audio_field] = f'[sound:{text_to_speech(examples[0], pth)}]'

        count('editing notes now')
        update_note(card['noteId'], updated_fields)
        add_tag(card['noteId'], 'AnkiPy')  # invoke('addTags', notes=[ID, ID], tags='AnkiPy')
        ########################################################################
        count(f'{l} changed')
        print(f'############################################################')
    except Exception as e:
        print(e)
        count('edit attempt failed')
        add_tag(card['noteId'], 'AnkiPyNoExample')  # invoke('addTags', notes=[ID, ID], tags='AnkiPy')
        # print(f'{l} examples not found')
        pass


counter = time.time()
def count(func_took='function took'):
    print(f'{func_took}: {time.time() - counter}')
