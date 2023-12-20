#!/usr/bin/env python

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


from itertools import product
from grid4x4 import Grid4x4
from typing import Optional
import random


class Game2048:
    _all_idxs = list(product(range(4), range(4)))

    def __init__(self, grid: Optional[Grid4x4] = None):
        # grid values are distributed this way
        self.grid = Grid4x4(grid)
        if grid is None:
            self.reset()

    def display(self):
        self.grid.display()

    def save(self):
        return {'grid': self.grid._grid[:]}

    def restore(self, data):
        self.grid._grid = data['grid']

    def resetRandom(self, max_cells, max_value):
        self.grid = Grid4x4()
        init_cells = random.choice(list(range(2, max_cells+1)))
        init_idxs = random.sample(Game2048._all_idxs, init_cells)
        values = list(range(1, max_value+1))
        for x, y in init_idxs:
            v = random.choice(values)
            self.grid[x, y] = v  # value of 2

    def reset(self):
        # fill 2 spots with either 2 or 4
        self.grid = Grid4x4()
        init_idxs = random.sample(Game2048._all_idxs, 2)
        for x, y in init_idxs:
            # 10% chance of a 4 instead of a 2
            v = 2 if (random.random() > 0.9) else 1
            self.grid[x, y] = v  # value of 2

    def add_tile(self) -> bool:
        open_idxs = [
            (x, y) for x, y in Game2048._all_idxs if (self.grid[x, y] == 0)
        ]
        if len(open_idxs) == 0:
            return False
        x, y = random.choice(open_idxs)
        v = 2 if (random.random() > 0.9) else 1
        self.grid[x, y] = v
        return True

    def max_value(self):
        return max(self.grid._grid)

    def slide(self: 'Game2048', direction: str):
        if direction == 'L':
            def get(x, y): return self.grid[x, y]
            def set(x, y, v): self.grid[x, y] = v
        elif direction == 'R':
            def get(x, y): return self.grid[3-x, y]
            def set(x, y, v): self.grid[3-x, y] = v
        elif direction == 'U':
            def get(x, y): return self.grid[y, x]
            def set(x, y, v): self.grid[y, x] = v
        elif direction == 'D':
            def get(x, y): return self.grid[y, 3-x]
            def set(x, y, v): self.grid[y, 3-x] = v
        else:
            raise RuntimeError(f"invalid direction {direction}")

        for y in range(4):
            prev = 0
            xo = 0
            for x in range(4):
                v = get(x, y)
                if v > 0:
                    if v == prev:
                        # merge values
                        set(xo-1, y, v+1)
                        prev = 0
                    else:
                        # move value
                        set(xo, y, v)
                        xo += 1
                        prev = v
            while xo < 4:
                set(xo, y, 0)
                xo += 1
