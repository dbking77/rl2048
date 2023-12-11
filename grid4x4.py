#!/usr/bin/env python3

from typing import Iterable, Iterator, Optional, Tuple, Union


class Grid4x4:
    """ 4x4 grid of integer values between 0 and 15"""

    GridListType = Iterable[Iterable[int]]

    def __init__(self,
                 vals: Optional[Union[GridListType, str, 'Grid4x4']] = None):
        # TODO use numpy array instead of flat list
        self._grid = [0 for _ in range(16)]
        if vals is None:
            pass
        elif isinstance(vals, Grid4x4):
            self._grid = vals._grid[:]
        elif isinstance(vals, str):
            lookup = {c: i for i, c in enumerate(".123456789ABCDEF")}
            y = 0
            for line in vals.split('\n'):
                line = line.strip()
                if len(line) == 0:
                    continue
                assert len(line) == 4
                for x, c in enumerate(line):
                    self[x, y] = lookup[c]
                y += 1
        else:
            for y, row in enumerate(vals):
                for x, v in enumerate(row):
                    assert 0 <= v < 16
                    self[x, y] = v

    def __getitem__(self: 'Grid4x4', idx: Tuple[int, int]) -> int:
        x, y = idx
        assert 0 <= x < 4
        assert 0 <= y < 4
        return self._grid[y*4 + x]

    def __setitem__(self: 'Grid4x4', idx: Tuple[int, int], value: int):
        x, y = idx
        assert 0 <= x < 4
        assert 0 <= y < 4
        self._grid[y*4 + x] = value

    def enum_xy(self: 'Grid4x4') -> Iterator[Tuple[int, int, int]]:
        """return tuples x,y,value for grid"""
        for y in range(4):
            for x in range(4):
                yield (x, y, self[x, y])

    def flip(self: "Grid4x4",
             flip_x: bool,
             flip_y: bool,
             swap_xy: bool) -> "Grid4x4":
        xo, xi = (3, -1) if flip_x else (0, 1)
        yo, yi = (3, -1) if flip_y else (0, 1)
        new_grid = Grid4x4()
        old_grid = self
        for y in range(4):
            for x in range(4):
                xn, yn = (x*xi + xo, y*yi + yo)
                if swap_xy:
                    xn, yn = (yn, xn)
                new_grid[xn, yn] = old_grid[x, y]
        return new_grid

    def heavy_side(self):
        # return L,D,U,R for the "heavy-side" of grid
        xsum = 0.0
        ysum = 0.0
        for y in range(4):
            for x in range(4):
                v = 1 if self[x, y] > 0 else -1
                xsum += v * (x-1.5)
                ysum += v * (y-1.5)
        if abs(xsum) > abs(ysum):
            side = 'R' if (xsum > 0) else 'L'
        else:
            side = 'D' if (ysum > 0) else 'U'
        return (side, xsum, ysum)

    def heavy_side_flip(self):
        """
        Will flip grid so most non-zero elements are on left top
        Will also swap x and y axes so most element are on left versus top
        """
        _, xside, yside = self.heavy_side()
        return self.flip(xside > 0, yside > 0, abs(yside) > abs(xside))

    def __str__(self) -> str:
        msg = ""
        for y in range(4):
            for x in range(4):
                v = self[x, y]
                if v == 0:
                    msg += '.'
                elif v < 10:
                    msg += chr(ord('0') + v)
                else:
                    msg += chr(ord('A') + v - 10)
            msg += '\n'
        return msg

    def __repr__(self) -> str:
        return self.__str__()

    NotImplementedType = type(NotImplemented)

    def __eq__(self: 'Grid4x4', other: object) -> bool:
        if not isinstance(other, Grid4x4):
            return NotImplemented
        return self._grid == other._grid

    def __ne__(self: 'Grid4x4', other: object) -> bool:
        if not isinstance(other, Grid4x4):
            return NotImplemented
        return self._grid != other._grid

    def display(self: 'Grid4x4'):
        print(self)
