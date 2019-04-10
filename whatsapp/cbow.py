from itertools import tee


def cbow(input):
    window_size = 5
    centre = 2

    y, X = [], []

    for window in _window(input, size=window_size):
        y.append(window.pop(centre))
        X.append(window)

    return y, X


def _window(iterable, size):
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    yield from (
        list(window)
        for window in zip(*iters)
    )
