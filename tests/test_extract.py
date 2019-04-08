from textwrap import dedent
import io

from precisely import assert_that, contains_exactly

from whatsapp.extract import extract_text


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
