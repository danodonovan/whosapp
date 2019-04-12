from textwrap import dedent
import io
import string

from precisely import (
    assert_that, contains_exactly, is_mapping, all_of, is_instance,
    less_than_or_equal_to
)

from whatsapp.extract import (
    extract_text, clean_text, clean_text_lines, build_word2id, build_id2word
)


def test_extract_text_extracts_text_strings():
    text = io.StringIO(dedent("""\
        [05/06/2018, 18:54:06] John Smith: Flights booked. Maybe we can meet up and cook all together?
        [17/08/2018, 23:52:10] John Smith: Oh my! At least it went a hip!!! 😬
        [13/01/2019, 22:20:03] Glenn Quagmire: Happy Anniversary to you Jim.
    """))

    text_lines = extract_text(text)

    assert_that(text_lines, contains_exactly(
        "Flights booked. Maybe we can meet up and cook all together?",
        "Oh my! At least it went a hip!!! 😬",
        "Happy Anniversary to you Jim."
    ))


def test_extract_drops_lines_containing_left_to_right_mark_character():
    text = io.StringIO(dedent("""\
        [02/08/2016, 06:44:26] \u200eYou added Gary Barker
        [17/08/2018, 23:52:10] John Smith: Oh my! At least it went a hip!!! 😬
    """))

    text_lines = extract_text(text)

    assert_that(text_lines, contains_exactly(
        "Oh my! At least it went a hip!!! 😬",
    ))


def test_clean_text_removes_normalises_text():
    text = "Oh my! At least it went a hip!!! 😬"
    table = str.maketrans("", "", string.punctuation)

    cleaned_text = clean_text(text, table=table)

    assert_that(cleaned_text, contains_exactly(
        "oh", "my", "at", "least", "it", "went", "a", "hip", "😬"
    ))


def test_clean_text_lines_removes_normalised_text_lines():
    text_lines = [
        "Flights booked. Maybe we can meet up and cook all together?",
        "Oh my! At least it went a hip!!! 😬",
        "Happy Anniversary to you Jim."
    ]

    cleaned_lines = clean_text_lines(text_lines)

    assert_that(cleaned_lines, contains_exactly(
        contains_exactly(
            "flights", "booked", "maybe", "we", "can", "meet", "up", "and",
            "cook", "all", "together",
        ),
        contains_exactly(
            "oh", "my", "at", "least", "it", "went", "a", "hip", "😬"
        ),
        contains_exactly(
            "happy", "anniversary", "to", "you", "jim"
        )
    ))


def _is_in_range(max_value):
    return all_of(
        is_instance(int),
        less_than_or_equal_to(max_value)
    )


def test_build_word2id_creates_word_id_mapping():
    words = [
        "flights", "booked", "booked",
        "cook", "all", "together",
    ]
    word2id = build_word2id(words)

    assert_that(word2id, is_mapping({
        "flights": _is_in_range(4),
        "booked": _is_in_range(4),
        "cook": _is_in_range(4),
        "all": _is_in_range(4),
        "together": _is_in_range(4),
    }))


def test_build_id2word_reverses_word2id_mapping():
    word2id = {
        "flights": 0,
        "booked": 1,
        "cook": 2,
        "all": 3,
        "together": 4,
    }
    id2word = build_id2word(word2id)

    assert_that(id2word, is_mapping({
        0: is_instance(str),
        1: is_instance(str),
        2: is_instance(str),
        3: is_instance(str),
        4: is_instance(str),
    }))
