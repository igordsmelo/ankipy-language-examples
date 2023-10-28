from utils.anki_requests import filter_note_by_tag, search_notes
from utils.formatting import edit_anki_note


def main(query: str or list, target_sentence_field: str = 'Japanese') -> None:
    """
    Adds example sentences to cards in deck.
    :param query: what to search for. In Anki terms.
    :param target_sentence_field: field where phrases will be stored.
    """
    queries = str(query) if isinstance(query, str) else query
    for q in queries:
        # Search for notes with the given query and exclude those with the tag 'AnkiPy'.
        notes = filter_note_by_tag(search_notes(q), exclude='AnkiPy')
        # Filter out notes that already have a value in the target sentence field.
        notes = [n for n in notes if not n['fields'][target_sentence_field]['value']]
        # Print the number of notes that will be edited.
        print(f'There are {len(notes)} notes to edit.')
        # Edit each note by adding an example sentence to the target sentence field.
        for note in notes:
            edit_anki_note(note, language='Expression', sentence_field=target_sentence_field)
        print(f'Finished notes matching query: "{q}".')


search_queries = [
    "deck:Default::Downloaded::JLPT::N5",
    "deck:Default::Downloaded::JLPT::N4",
    "deck:Default::Downloaded::JLPT::N3",
    "deck:Default::Downloaded::JLPT::N2",
    "deck:Default::Downloaded::JLPT::N1"
]

if __name__ == '__main__':
    main(search_queries)