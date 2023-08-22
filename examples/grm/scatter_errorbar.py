from math import pi, cos
from random import random, seed
from typing import Dict

import grm


LENGTH = 200


def test_plot() -> None:
    seed(151515)
    x = [i / 200 * pi * 3 for i in range(LENGTH)]
    y = [cos(x[i]) + random() for i in range(LENGTH)]
    errors = [random() * (0.5 + cos(i / 200 * pi)) / 5 for i in range(LENGTH)]
    errors.extend([random() * (0.5 + cos(i / 200 * pi)) / 5 for i in range(LENGTH)])

    error = {
        "absolute": (errors[:LENGTH], errors[LENGTH:]),
        "upwardscap_color": -1,
        "downwardscap_color": -1,
        "errorbar_color": 4
    }
    args: Dict[str, grm.args._ElemType] = {
        "x": x,
        "y": y,
        "error": error,
        "size": (1000.0, 1000.0)
    }
    grm.plot.scatter(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
