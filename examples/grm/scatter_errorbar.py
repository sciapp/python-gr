from math import pi, cos
from typing import Dict
import platform
import ctypes

import grm


LENGTH = 200
INT_MAX = ctypes.c_uint(-1).value // 2


def test_plot() -> None:
    try:
        if platform.system() == "Darwin":
            libc = ctypes.cdll.LoadLibrary("libSystem.dylib")  # type: ignore
        else:
            libc = ctypes.cdll.LoadLibrary("libc.so.6")  # type: ignore
    except OSError:
        libc = None

    libc.srand(151515)

    x = [i / 200 * pi * 3 for i in range(LENGTH)]
    y = []
    errors1 = []
    errors2 = []
    for i in range(len(x)):
        y.append(cos(x[i]) + libc.rand() / INT_MAX)
        errors1.append(libc.rand() / INT_MAX * (0.5 + cos(i / 200 * pi)) / 5)
        errors2.append(libc.rand() / INT_MAX * (0.5 + cos(i / 200 * pi)) / 5)

    error = {
        "absolute": (errors1, errors2),
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
