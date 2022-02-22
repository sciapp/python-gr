# -*- coding: utf-8 -*-

# standard library

# third party

# local library
import gr
from gr.pygr import Coords2DList, Coords2D, Coords3DList, Coords3D


def test_char():
    gr.char("t")
    gr.char(u"t")


def test_coords2DList_minmax():
    a = Coords2D([10, 20, 30], [10, 20, 30])
    coords = Coords2DList([a])
    assert coords.xmin == 10
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 30

    coords.append(Coords2D([5, 10], [20, 40]))
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 40

    b = Coords2D([1, 2, 3], [1, 2, 3])
    coords += [b]
    assert coords.xmin == 1
    assert coords.xmax == 30
    assert coords.ymin == 1
    assert coords.ymax == 40

    tmp = coords.pop(coords.index(b))
    assert tmp == b
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 40

    coords.extend([b])
    assert coords.xmin == 1
    assert coords.xmax == 30
    assert coords.ymin == 1
    assert coords.ymax == 40

    coords.remove(b)
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 40

    coords.append(Coords2D([10, 10], [0, 0]))
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 0
    assert coords.ymax == 40

    coords.append(Coords2D([10, 10], [200, 400]))
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 0
    assert coords.ymax == 400


def test_coords2DList_empty():
    a = Coords2D([10, 20, 30], [10, 20, 30])
    coords = Coords2DList([a])
    coords.remove(a)
    assert coords.xmin is None
    assert coords.xmax is None
    assert coords.ymin is None
    assert coords.ymax is None


def test_coords2DList_update():
    a = Coords2D([10, 20, 30], [10, 20, 30])
    b = Coords2D([5], [40])
    coords = Coords2DList([a, b])
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 40

    b.x = [15]
    b.y = [25]
    coords.updateMinMax(b)
    assert coords.xmin == 5
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 40

    coords.updateMinMax(*coords, reset=True)
    assert coords.xmin == 10
    assert coords.xmax == 30
    assert coords.ymin == 10
    assert coords.ymax == 30

    coords.updateMinMax(b, reset=True)
    assert coords.xmin == 15
    assert coords.xmax == 15
    assert coords.ymin == 25
    assert coords.ymax == 25


def test_coords3DList_minmax():
    coords = Coords3DList([Coords3D([1, 2], [1, 2], [-42, 42])])
    assert coords.xmin == 1
    assert coords.xmax == 2
    assert coords.ymin == 1
    assert coords.ymax == 2
    assert coords.zmin == -42
    assert coords.zmax == 42
