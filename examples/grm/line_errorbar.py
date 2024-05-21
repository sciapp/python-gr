from math import sin
from typing import Dict

import grm


LENGTH = 50


def test_plot() -> None:
    plot = [
        [i / (LENGTH - 1) * 2 - 1 for i in range(LENGTH)],
        [sin(i / (LENGTH - 1) * 2 - 1) for i in range(LENGTH)]
    ]
    errors = [plot[0][i] * plot[1][i] for i in range(LENGTH)]
    errors = errors * 2

    error = {
        "absolute": (errors[:LENGTH], errors[LENGTH:]),
        "upward_scap_color": 2,
        "downward_scap_color": 3,
        "error_bar_color": 4
    }
    args: Dict[str, grm.args._ElemType] = {
        "x": plot[0],
        "y": plot[1],
        "error": error
    }

    grm.plot.line(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
