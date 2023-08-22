from math import pi, sin
from typing import Dict, List

import grm


LENGTH = 1000


def test_size_container() -> None:
    x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    y = [sin(x[i]) for i in range(LENGTH)]

    size: List[Dict[str, grm.args._ElemType]] = [
        {
            "value": 2.0 + (1 - i) * 1.0,
            "unit": "dm"
        }
        for i in range(2)
    ]
    print("plotting data in a window of size (3.0 dm, 2.0 dm)")
    grm.plot.line(x=x, y=y, hold_plots=True, size=size)
    input("Press enter to continue")

    size[0]["value"] = 10.0
    size[0]["unit"] = "cm"
    size[1]["value"] = 500
    size[1]["unit"] = "px"
    print("Change the output size to (10.0 cm, 500 px)")
    grm.plot.line(x=x, y=y, hold_plots=True, size=size)
    input("Press enter to continue")

    size[0]["value"] = 0.25
    size[0]["unit"] = "ft"
    size[1]["value"] = 3
    size[1]["unit"] = "in"
    print("Change the output size to (0.25 ft, 3 in)")
    grm.plot.line(x=x, y=y, hold_plots=True, size=size)
    input("Press enter to continue")


if __name__ == "__main__":
    test_size_container()
