import time

from WIP.script_ankilangsamples.utils.data import jp_en, get_examples
from WIP.script_ankilangsamples.utils.formatting import remove_fromtext
from WIP.script_ankilangsamples.utils.text_and_speech import text_to_speech
from url_requests import update_note, add_tag

############################################################ performance analysis.
counter = time.time()


def count(func_took='function took'):
    print(f'{func_took}: {time.time() - counter}')
############################################################


def edit_anki_note(card, language='Word', sentence_field='Sentence',
                   translation_field='English', audio_field='Sentence Audio'):
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
        ####
        ########################################################################
        count(f'{l} changed')
        print(f'############################################################')
    except :
        count('edit attempt failed')
        add_tag(card['noteId'], 'AnkiPyNoExample')  # invoke('addTags', notes=[ID, ID], tags='AnkiPy')
        #print(f'{l} examples not found')
        pass


def filter_note_by_tag(notes, include=None, exclude=None):
    filtered_notes = notes
    if include:
        filtered_notes = [n for n in notes if include in n['tags']]
    if exclude:
        filtered_notes = [n for n in notes if exclude not in n['tags']]
    return filtered_notes


