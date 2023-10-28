from utils.data import get_sentence_examples, jp_en
from utils.text_and_speech import what_is_this_word


def match_translation(og_txt, eng_translation) -> list:
    """finds out what each word in two translated texts mean in the other language."""
    from googletrans import Translator as gT
    o_lang = gT().detect(og_txt).lang  # finds out which language the og_txt is in. ja, pt, etc.
    grammar_info = what_is_this_word(eng_translation)
    matches = []
    for w in grammar_info:  # for individual words in the english translation.
        try:
            translated_w = gT().translate(w[0], dest=o_lang).text  # if translated words match original text.
            if translated_w in og_txt:
                # found ('Tokyo', 'NNP') translation (東京) in 東京へ行くのに２時間かかった. Tokyo(東京) is a NNP
                print(f'{translated_w}({w[0]}) found in {og_txt}. \n{w[0]}({translated_w}) is a {w[1]}')
                if w[1] not in ['.', ',', '?', '!', '@', '|']:
                    matches.append([translated_w, w[0], w[1]])
            else:
                pass
                print(f"{translated_w} not in {og_txt}")
        except TypeError:
            pass
    return matches


if __name__ == '__main__':
    match_translation('東京へ行くのに２時間かかった', 'It took two hours to go to Tokyo')  # test
    abc = get_sentence_examples('clean', jp_en)
    grammar = match_translation(abc[1][0], abc[1][1])
