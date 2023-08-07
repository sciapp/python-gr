from math import sqrt

import grm.plot


LENGTH = 50


def test_plot() -> None:
    plot = [0.0 for _ in range(LENGTH**3)]
    for i in range(LENGTH):
        for j in range(LENGTH):
            for k in range(LENGTH):
                x = i / (LENGTH / 2) - 1
                y = j / (LENGTH / 2) - 1
                z = k / (LENGTH / 2) - 1
                plot[i * LENGTH**2 + j * LENGTH + k] = 1.0 - sqrt(x**2 + y**2 + z**2)

    grm.plot.isosurface(c=plot, c_dims=(LENGTH, LENGTH, LENGTH), isovalue=0.2)
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
