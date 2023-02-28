import json
import urllib.request


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

############################################################ Anki specifics.


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
