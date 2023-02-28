#todo: get data from tatoeba if not found

jp_en = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-English - 2022-10-26.txt"
jp_fr = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-French - 2022-10-27.txt"
jp_sp = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Spanish - 2022-10-27.txt"
jp_kr = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Korean - 2022-10-27.txt"
jp_pt = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Portuguese - 2022-10-27.txt"
jp_es = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Esperanto - 2022-10-27.txt"
jp_ge = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-German - 2022-10-27.txt"
jp_cn = r"D:\Users\Igor\Downloads\Sentence pairs in Japanese-Mandarin Chinese - 2022-10-27.txt"

############################################################


def get_examples(word, database, word_limit=None, shuffle=False):
    from random import shuffle
    try:
        database = open(database, encoding="utf8").readlines()
    except FileNotFoundError:
        print('database not found. Download it from tatoeba.org or another site of your own choosing.')
    shuffle(database) if shuffle else database.sort(key=len)  # shuffles sentences or sort them by length.
    matching_sentences = [get_sentence(lines) for lines in database if all(w in lines for w in word.split(', '))]
    return matching_sentences[0:word_limit+1] if word_limit is not None else matching_sentences


def get_sentence(sentence):
    s = sentence.split('\t')  # 1 for japanese sentence, 3 for english translation
    return [s[1], s[3]]  # [hi, oi]

get_examples('hi', jp_en)