from anki_language_samples import url_requests

SIX_K = url_requests.search_notes("tag:Languages::Japanese::Core6K")
MAIN = url_requests.search_notes("tag:Languages::Japanese::Main")

print('anki checked')
six_k = {notes['fields']['Word']['value']: notes['noteId'] for notes in SIX_K}
main = {notes['fields']['Word']['value']: notes['noteId'] for notes in MAIN}
duplicate = set(six_k) & set(main)
duplicate = list(duplicate)
print('duplicates checked')

for d in duplicate:
    print(six_k[d], main[d])
    six_k_note = [n for n in SIX_K if n['noteId'] == six_k[d]][0]
    main_note = [n for n in MAIN if n['noteId'] == main[d]][0]
    main_note_ntags = [tags for tags in main_note['tags'] if 'Languages::Japanese::JLPT::N' in tags]
    for tags in main_note_ntags:
        print(f'adding "{tags}"')
        url_requests.add_tag(six_k_note['noteId'], tags)

# #########################################################################
# duplicates = {"Languages::Japanese::JLPT::N5":'',
#               "Languages::Japanese::JLPT::N4":'',
#               "Languages::Japanese::JLPT::N3":'',
#               "Languages::Japanese::JLPT::N2":'',
#               "Languages::Japanese::JLPT::N1":'', }
# for d in duplicate:
#     six_k_note = [n for n in SIX_K if n['noteId'] == six_k[d]][0]
#     main_note = [n for n in MAIN if n['noteId'] == main[d]][0]
#     main_note_ntags = [tags for tags in main_note['tags'] if 'Languages::Japanese::JLPT::N' in tags]
#     for tags in main_note_ntags:
#         duplicates[tags] += f" {six_k_note['noteId']}"
# for tags in duplicates:
#     duplicates[tags] = duplicates[tags].split()
#     id_list = [int(ids) for ids in duplicates[tags]]
#     url_requests.add_tag(id_list, tags)
#     print(f"tag: {tags}, added to: \n {duplicates[tags]} \n\n\n\n\n\n")
#
# #########################################################################
# duplicates = [notes['Word'] for notes in 6K if notes['Word'] in Main]
