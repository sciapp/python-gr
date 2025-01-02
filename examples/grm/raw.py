import math
import os

import gr
from base64 import b64encode
from gr import pygr
import grm


GRAPHICS_FILENAME = "gr.xml.base64"


def create_example_graphics_export() -> None:
    x = [2 * math.pi * i / 100 for i in range(100)]
    y = [math.sin(c) for c in x]
    gr.begingraphics(GRAPHICS_FILENAME)  # type: ignore
    pygr.plot(x, y)  # type: ignore
    gr.endgraphics()  # type: ignore
    with open(GRAPHICS_FILENAME, "rb") as f:
        graphics_data = f.read()
    base64_encoded_graphics_data = b64encode(graphics_data)
    with open(GRAPHICS_FILENAME, "wb") as f:
        f.write(base64_encoded_graphics_data)


def test_raw() -> None:
    with open(GRAPHICS_FILENAME, "r") as f:
        graphics_data = f.read()

    grm.plot.plot(raw=graphics_data)
    input("Press enter to continue")


def remove_example_file() -> None:
    os.remove(GRAPHICS_FILENAME)


def main() -> None:
    create_example_graphics_export()
    test_raw()
    remove_example_file()


if __name__ == "__main__":
    main()
