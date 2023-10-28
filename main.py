from utils.formatting import edit_anki_note
from WIP.script_ankilangsamples.utils.anki_requests import search_notes


# TODO: find out what this function does.
def main(query: str or list, target_sentence_field: str = 'Japanese'):
    """
    Adds example sentences to cards in deck.
    :param query: what to search for. In Anki terms.
    :param target_sentence_field: field where phrases will be stored.
    """
    queries = str(query) if type(query) == str else query
    for q in queries:  # individual query terms
        notes = filter_note_by_tag(search_notes(q), exclude='AnkiPy')  # searches query, filters it, assign to var
        notes = [n for n in notes if not n['fields'][target_sentence_field]['value']]
        print(f'there are {len(notes)} notes to edit')
        for note in notes:  # individual notes
            edit_anki_note(note, language='Expression', sentence_field=target_sentence_field)  # starts editing it
        print(f'finished notes matching query: "{q}"')


search_queries = ["deck:Default::Downloaded::JLPT::N5",
                  "deck:Default::Downloaded::JLPT::N4",
                  "deck:Default::Downloaded::JLPT::N3",
                  "deck:Default::Downloaded::JLPT::N2",
                  "deck:Default::Downloaded::JLPT::N1"]
if __name__ == '__main__':
    main(search_queries)


def filter_note_by_tag(notes, include=None, exclude=None):
    filtered_notes = notes
    if include:
        filtered_notes = [n for n in notes if include in n['tags']]
    if exclude:
        filtered_notes = [n for n in notes if exclude not in n['tags']]
    return filtered_notes
