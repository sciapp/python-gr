from math import sqrt
from typing import Dict

import grm


LENGTH = 50


def test_plot() -> None:
    plot = [0.0] * LENGTH**3
    for i in range(LENGTH):
        for j in range(LENGTH):
            for k in range(LENGTH):
                x = i / (LENGTH / 2.0) - 1
                y = j / (LENGTH / 2.0) - 1
                z = k / (LENGTH / 2.0) - 1
                plot[i * LENGTH**2 + j * LENGTH + k] = 1.0 - sqrt(x**2 + y**2 + z**2)

    args: Dict[str, grm.args._ElemType] = {
        "c": plot,
        "c_dims": (LENGTH, LENGTH, LENGTH)
    }
    print("plot volume with algorithm 'emission'")
    grm.plot.volume(args, algorithm="emission")
    input("Press enter to continue")

    print("plot volume with algorithm 'absorption'")
    grm.plot.volume(args, algorithm="absorption")
    input("Press enter to continue")

    print("plot volume with algorithm 'maximum'")
    grm.plot.volume(args, algorithm="maximum")
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
