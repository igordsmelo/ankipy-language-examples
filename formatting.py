def remove_fromtext(text,remove=["&nbsp;", "<rt>.*?</rt>", "<rubytitle=.*?>", "<.*?>"], remove_furigana=True):
    ''''removes parts of the text from string using regex'''
    import re  # IMPORTS REGEX MODULE
    text = text.replace("<rt>", "[").replace("</rt>", "]")
    replace = []
    if len(remove) > 0:
        for r in ["&nbsp;", "<rt>.*?</rt>", "<rubytitle=.*?>", "<.*?>"]:
            replace += [*set(re.findall(r, text))]  # set removes duplicates from list. Went from hundreds to a few strs
        for r in replace:
            text = text.replace(r, '')
    if remove_furigana:
        for r in re.findall("\[.*?\]", text):
            text = text.replace(r, '')
    return text
