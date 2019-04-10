from precisely import assert_that, is_sequence

from whatsapp.cbow import cbow


def test_cbow():
    input = list(range(1, 10))

    y, X = cbow(input)

    assert_that(y, is_sequence(3, 4, 5, 6, 7))

    assert_that(X, is_sequence(
        is_sequence(1, 2, 4, 5),
        is_sequence(2, 3, 5, 6),
        is_sequence(3, 4, 6, 7),
        is_sequence(4, 5, 7, 8),
        is_sequence(5, 6, 8, 9),
    ))
