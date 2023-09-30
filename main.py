from WIP.script_ankilangsamples.utils.anki_sentences import filter_note_by_tag, edit_anki_note
from WIP.script_ankilangsamples.utils.url_requests import search_notes

a = 'test'
def main():
    queries = ["deck:Default::Downloaded::JLPT::N5",
               "deck:Default::Downloaded::JLPT::N4",
               "deck:Default::Downloaded::JLPT::N3",
               "deck:Default::Downloaded::JLPT::N2",
               "deck:Default::Downloaded::JLPT::N1"]
    target_sentence_field = 'Japanese'
    for q in queries:  # individual query terms
        notes = filter_note_by_tag(search_notes(q), exclude='AnkiPy')  # searches query, filters it, assign to var
        notes = [n for n in notes if not n['fields'][target_sentence_field]['value']]
        print(f'there are {len(notes)} notes to edit')
        for note in notes:  # individual notes
            edit_anki_note(note, language='Expression', sentence_field=target_sentence_field)  # starts editing it
        print(f'finished fucking {q}')
