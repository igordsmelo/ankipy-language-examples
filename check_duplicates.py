from anki_language_samples import url_requests

SIX_K = url_requests.search_notes("tag:Languages::Japanese::Core6K")
MAIN = url_requests.search_notes("tag:Languages::Japanese::Main")

for notes in SIX_K[:10]:
    print(notes['fields']['Word']['value'])

for notes in MAIN[:10]:
    print(notes['fields']['Word']['value'])

for notes_2, notes_1 in zip(SIX_K, MAIN):
    print(notes_2['fields']['Word']['value'], ' | ',
          notes_1['fields']['Word']['value'])
    break

six_k = {notes['fields']['Word']['value']: notes['noteId'] for notes in SIX_K}
main = {notes['fields']['Word']['value']: notes['noteId'] for notes in MAIN}
duplicate = set(six_k) & set(main)
duplicate = list(duplicate)

print(duplicate[0])

# duplicates = [notes['Word'] for notes in 6K if notes['Word'] in Main]
