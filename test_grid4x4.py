#!/usr/bin/env python3

# MIT License

# Copyright (c) 2023 Derek King

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from grid4x4 import Grid4x4
from itertools import product


def test_init():
    grid = Grid4x4()
    for x in range(4):
        for y in range(4):
            assert grid[x, y] == 0


def test_rw():
    grid = Grid4x4()

    def val(x, y): return x*7 + y*13
    for x in range(4):
        for y in range(4):
            grid[x, y] = val(x, y)
    for x in range(4):
        for y in range(4):
            assert grid[x, y] == val(x, y)


def test_str():
    grid = Grid4x4()
    i = 0
    for y in range(4):
        for x in range(4):
            grid[x, y] = i
            i += 1
    msg = str(grid)

    expect = [
        ".123",
        "4567",
        "89AB",
        "CDEF",
    ]
    assert msg.split() == expect


def test_enum_xy():
    grid = Grid4x4()
    def val(x, y): return x*5 + y*11
    for y in range(4):
        for x in range(4):
            grid[x, y] = val(x, y)
    for x, y, v in grid.enum_xy():
        assert v == val(x, y)


def test_load_str():
    grid = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    for x, y, v in grid.enum_xy():
        assert v == (x + y*4)


def test_load_iterable():
    grid = Grid4x4([
        range(4,),
        [4, 5, 6, 7],
        (8, 9, 10, 11),
        range(12, 16),
    ])
    for x, y, v in grid.enum_xy():
        assert v == (x + y*4)


def test_eq():
    grid1 = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    grid2 = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    assert grid1 == grid2
    grid1[0, 0] += 1
    assert grid1 != grid2
    grid1[0, 0] -= 1
    assert grid1 == grid2


def test_grid_copy():
    grid1 = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    grid2 = Grid4x4(grid1)
    assert grid2._grid is not grid1._grid
    assert grid2._grid == grid1._grid
    assert grid1 == grid2
    assert grid2 == grid1
    grid2[0, 0] = 4
    assert grid2 != grid1


def test_flip_x():
    grid1 = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    grid2 = Grid4x4("""
    321.
    7654
    BA98
    FEDC
    """)
    grid1_flipped = grid1.flip(True, False, False)
    assert grid1_flipped == grid2
    assert grid2.flip(True, False, False) == grid1


def test_flip_y():
    grid1 = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    grid2 = Grid4x4("""
    CDEF
    89AB
    4567
    .123
    """)
    assert grid2 == grid1.flip(False, True, False)


def test_flip_swap_xy():
    grid1 = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    grid2 = Grid4x4("""
    .48C
    159D
    26AE
    37BF
    """)
    assert grid2 == grid1.flip(False, False, True)


def test_flip_all():
    grid_orig = Grid4x4("""
    .123
    4567
    89AB
    CDEF
    """)
    for flip_x, flip_y, swap_xy in product((False, True), repeat=3):
        grid1 = Grid4x4(grid_orig)
        if flip_x:
            grid1 = grid1.flip(True, False, False)
        if flip_y:
            grid1 = grid1.flip(False, True, False)
        if swap_xy:
            grid1 = grid1.flip(False, False, True)
        grid2 = Grid4x4(grid_orig).flip(flip_x, flip_y, swap_xy)
        if flip_x or flip_y or swap_xy:
            assert grid1 != grid_orig
        assert grid1 == grid2


def test_heavyside_flip_x():
    grid1 = Grid4x4("""
    ...1
    ..32
    ..4.
    ....
    """)

    grid2 = Grid4x4("""
    1...
    23..
    .4..
    ....
    """)
    grid1_flipped = grid1.heavy_side_flip()
    assert grid1_flipped == grid2


def test_heavyside_flip_y():
    grid1 = Grid4x4("""
    ....
    ....
    8...
    9A..
    """)

    grid2 = Grid4x4("""
    9A..
    8...
    ....
    ....
    """)
    grid1_flipped = grid1.heavy_side_flip()
    assert grid1_flipped == grid2


def test_heavyside_swap_xy():
    grid1 = Grid4x4("""
    56.8
    ..7.
    ....
    ....
    """)

    grid2 = Grid4x4("""
    5...
    6...
    .7..
    8...
    """)
    grid1_flipped = grid1.heavy_side_flip()
    assert grid1_flipped == grid2


def test_heavyside_none():
    grid1 = Grid4x4("""
    56..
    7...
    ....
    ...A
    """)

    grid2 = Grid4x4("""
    56..
    7...
    ....
    ...A
    """)
    grid1_flipped = grid1.heavy_side_flip()
    assert grid1_flipped == grid2


def test_heavyside_all():
    grid1 = Grid4x4("""
    ....
    ....
    ...D
    .CBA
    """)

    grid2 = Grid4x4("""
    AD..
    B...
    C...
    ....
    """)
    grid1_flipped = grid1.heavy_side_flip()
    assert grid1_flipped == grid2
