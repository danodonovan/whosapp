import string


def extract_text(text):
    for line in text.readlines():
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
