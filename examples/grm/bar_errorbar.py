from math import sin
from typing import Dict

import grm


LENGTH = 50


def test_plot() -> None:
    plot = [sin(i / (LENGTH - 1)) for i in range(LENGTH)]
    errors = [plot[i] * (i / (LENGTH - 1)) / 5 for i in range(LENGTH)]

    error = {
        "absolute": (errors[:LENGTH], errors[LENGTH:]),
        "upward_scap_color": 2,
        "downward_scap_color": 3,
        "error_bar_color": 4
    }
    args: Dict[str, grm.args._ElemType] = {
        "y": plot,
        "error": error
    }
    grm.plot.barplot(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
