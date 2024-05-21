from math import pi, sin, cos

import grm


LENGTH = 1000


def test_subplots() -> None:
    x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    plots = [
        [sin(sin((i * 2) * pi / LENGTH)) for i in range(LENGTH)],
        [sin(sin((i * 4) * pi / LENGTH)) for i in range(LENGTH)],
        [sin(cos((i * 2) * pi / LENGTH)) for i in range(LENGTH)],
        [sin(cos((i * 4) * pi / LENGTH)) for i in range(LENGTH)]
    ]

    subplots = [
        {
            "x": x,
            "y": plots[i],
            "subplot": (0.5 * (i % 2), 0.5 * (i % 2 + 1), 0.5 * (i // 2), 0.5 * (i // 2 + 1))
        }
        for i in range(4)
    ]
    grm.plot.line(subplots=subplots)
    input("Press enter to continue")


if __name__ == "__main__":
    test_subplots()
