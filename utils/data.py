from utils.formatting import split_example

jp_en = r"data/Sentence pairs in Japanese-English - 2022-10-26.txt"
jp_fr = r"data/Sentence pairs in Japanese-French - 2022-10-27.txt"
jp_sp = r"data/Sentence pairs in Japanese-Spanish - 2022-10-27.txt"
jp_kr = r"data/Sentence pairs in Japanese-Korean - 2022-10-27.txt"
jp_pt = r"data/Sentence pairs in Japanese-Portuguese - 2022-10-27.txt"
jp_es = r"data/Sentence pairs in Japanese-Esperanto - 2022-10-27.txt"
jp_ge = r"data/Sentence pairs in Japanese-German - 2022-10-27.txt"
jp_cn = r"data/Sentence pairs in Japanese-Mandarin Chinese - 2022-10-27.txt"

###########################################################


def get_sentence_examples(word: str, database: str, word_limit=None, shuffle=False) -> list:
    """
    Returns example sentences, with a specific word, from one of the databases in 'data' folder.
    :param word: word that'll be searched for in the database. Returns phrases and translations with said word.
    :param database: database to get the examples from
    :param word_limit: how many words each example can have.
    :param shuffle: shuffle list, to avoid reusing the same words over and over again.
    :return: a list, with lists, each containing a sentence and it's translation.
    >>> get_sentence_examples('computer', jp_en)
    """

    try:
        database = open(database, encoding="utf8").readlines()
        shuffle(database) if shuffle else database.sort(key=len)  # shuffles sentences or sort them by length.
        matching_sentences = [split_example(lines) for lines in database if all(w in lines for w in word.split(', '))]
        return matching_sentences[0:word_limit + 1] if word_limit is not None else matching_sentences
    except FileNotFoundError:
        print('database not found. Download it from tatoeba.org or another site of your own choosing.')
        db = input('add path to database. \n')
        get_sentence_examples(word, db)

