from formatting import split_example

# todo: get data from tatoeba if not found
jp_en = r"../anki-language-samples/langs/Sentence pairs in Japanese-English - 2022-10-26.txt"
jp_fr = r"../anki-language-samples/langs/Sentence pairs in Japanese-French - 2022-10-27.txt"
jp_sp = r"../anki-language-samples/langs/Sentence pairs in Japanese-Spanish - 2022-10-27.txt"
jp_kr = r"../anki-language-samples/langs/Sentence pairs in Japanese-Korean - 2022-10-27.txt"
jp_pt = r"../anki-language-samples/langs/Sentence pairs in Japanese-Portuguese - 2022-10-27.txt"
jp_es = r"../anki-language-samples/langs/Sentence pairs in Japanese-Esperanto - 2022-10-27.txt"
jp_ge = r"../anki-language-samples/langs/Sentence pairs in Japanese-German - 2022-10-27.txt"
jp_cn = r"../anki-language-samples/langs/Sentence pairs in Japanese-Mandarin Chinese - 2022-10-27.txt"


############################################################

def get_examples(word, database, word_limit=None, shuffle=False):
    """Reads text file containing sentences with translation."""
    from random import shuffle
    try:
        database = open(database, encoding="utf8").readlines()
        shuffle(database) if shuffle else database.sort(key=len)  # shuffles sentences or sort them by length.
        matching_sentences = [split_example(lines) for lines in database if all(w in lines for w in word.split(', '))]
        return matching_sentences[0:word_limit + 1] if word_limit is not None else matching_sentences
    except FileNotFoundError:
        print('database not found. Download it from tatoeba.org or another site of your own choosing.')
        dtbs = input('add path to database. \n')
        get_examples(word, dtbs)




# SIMPLE TEST:
#a = get_examples('hi', jp_en)