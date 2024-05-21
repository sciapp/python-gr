from math import pi, sin, cos
from typing import Dict

import grm


ROWS = 20
COLS = 40


def test_plot() -> None:
    plot = [0.0 for _ in range(ROWS * COLS)]
    for i in range(COLS):
        for j in range(ROWS):
            plot[j * COLS + i] = sin(4.0 * i / COLS - 2.0) + cos(pi * j / ROWS)

    args: Dict[str, grm.args._ElemType] = {
        "title": "imshow-test",
        "c": plot,
        "c_dims": (COLS, ROWS),
        "colormap": 44
    }
    # TODO title missing?
    grm.plot.imshow(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
