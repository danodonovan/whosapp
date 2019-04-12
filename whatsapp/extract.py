import string


def extract_text(text):
    for line in text.readlines():
        if "\u200E" in line:
            continue
        split_string = line.split(":", 3)
        yield split_string[-1].strip()


def clean_text(text, table):
    stripped = [
        word.translate(table).lower()
        for word in text.split(" ")
    ]
    return stripped


def clean_text_lines(text_lines):
    table = str.maketrans("", "", string.punctuation)
    for text_line in text_lines:
        yield clean_text(text_line, table)


def build_word2id(words):
    return _to_dict(
        (word, index)
        for index, word in enumerate(set(words))
    )


def build_id2word(word2id):
    return _to_dict(
        (index, word)
        for word, index in word2id.items()
    )


def _to_dict(values):
    result = dict()

    for key, value in values:
        if key in result:
            raise ValueError("Multiple values for key: {}".format(repr(key)))
        else:
            result[key] = value

    return result
