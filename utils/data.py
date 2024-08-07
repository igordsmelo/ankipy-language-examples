from utils.formatting import split_example

jp_en = r"ui/Japanese-English.txt"
jp_fr = r"ui/Japanese-French.txt"
jp_sp = r"ui/Japanese-Spanish.txt"
jp_kr = r"ui/Japanese-Korean.txt"
jp_pt = r"ui/Japanese-Portuguese.txt"
jp_es = r"ui/Japanese-Esperanto.txt"
jp_ge = r"ui/Japanese-German.txt"
jp_cn = r"ui/Japanese-MandarinChinese.txt"

###########################################################


def get_sentence_examples(word: str, database: str, word_limit: int = None, shuffle: bool = False) -> list:
    """
    Returns example sentences, with a specific word, from one of the databases in 'ui' folder.
    :param word: word that'll be searched for in the database. Returns phrases and translations with said word.
    :param database: database to get the examples from
    :param word_limit: how many words each example can have.
    :param shuffle: shuffle list, to avoid reusing the same words over and over again.
    :return: a list, with lists, each containing a sentence and it's translation.
    >>> get_sentence_examples('computer', jp_en)
    """

    try:
        # reads line inside database
        database = open(database, encoding="utf8").readlines()
        # shuffles sentences or sort them by length.
        shuffle(database) if shuffle else database.sort(key=len)
        # returns sentences containing the keyword in 'word' parameter.
        matching_sentences = [split_example(lines) for lines in database if all(w in lines for w in word.split(', '))]
        # returns found sentences, limited by word_limit if true, else return them all.
        return matching_sentences[0:word_limit + 1] if word_limit is not None else matching_sentences
    except FileNotFoundError:
        print("database not found. Download it from tatoeba.org or another site of your own choosing.")
        db = input("Please, rerun this code, or paste path to your sentences' database here. \n")
        get_sentence_examples(word, db)