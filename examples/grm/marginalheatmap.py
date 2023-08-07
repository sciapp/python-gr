from typing import Dict

import grm


ROWS = 4
COLS = 4
XMIN = 0
XMAX = 4
YMIN = 0
YMAX = 4


def test_marginalheatmap() -> None:
    df = [
        [1.0, 2.0, 3.0, 4.0],
        [2.0, 8.0, 4.0, 5.0],
        [3.0, 4.0, 5.0, 6.0],
        [4.0, 5.0, 6.0, 7.0]
    ]
    xi = [0.0] * COLS
    yi = [0.0] * ROWS
    zi = [0.0] * (COLS * ROWS)

    for row in range(ROWS):
        yi[row] = YMIN + (YMAX - YMIN) * (row / (ROWS - 1))
        for col in range(COLS):
            if row == 0:
                xi[col] = XMIN + (XMAX - XMIN) * (col / (COLS - 1))
            zi[row * COLS + col] = df[col][row]

    print("plot a marginalheatmap with x, y and z")
    grm.plot.marginal_heatmap(x=xi, y=yi, z=zi, marginal_heatmap_kind="all", algorithm="sum")
    input("Press enter to continue")

    print("plot a special type of marginalheatmap where only one line and column is shown")
    grm.plot.marginal_heatmap(x=xi, y=yi, z=zi, marginal_heatmap_kind="line", algorithm="sum", x_ind=1, y_ind=2)
    input("Press enter to continue")


if __name__ == "__main__":
    test_marginalheatmap()
