def extract_text(text):
    for line in text.readlines():
        split_string = line.split(":", 3)
        yield split_string[-1].strip()
