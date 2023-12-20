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


import curses
from game2048 import Game2048


def main(stdscr):
    # Clear screen
    game = Game2048()
    key_lookup = {
        'KEY_LEFT': 'L',
        'KEY_RIGHT': 'R',
        'KEY_UP': 'U',
        'KEY_DOWN': 'D',
    }
    stdscr.keypad(True)

    iteration = 0

    def disp(msg):
        stdscr.clear()
        stdscr.addstr(str(game.grid))
        stdscr.addstr(f"\nIteration {iteration}\n")
        stdscr.addstr(f"Max Value {game.max_value()}\n")
        stdscr.addstr(msg + '\n')
        stdscr.refresh()

    msg = ""
    while True:
        disp(msg)
        iteration = 0
        while True:
            disp(msg)
            key = stdscr.getkey()
            msg = ""
            if key == 'q':
                print("QUIT")
                return
            elif key in key_lookup:
                iteration += 1
                direction = key_lookup[key]
                game.slide(direction)
                if not game.add_tile():
                    msg = "FAILURE..."
                    break
            else:
                msg = f"INVALID KEY {key}"

        msg = msg + " Press 'q' to quit and 'r' to restart"
        while True:
            disp(msg)
            key = stdscr.getkey()
            if key == 'r':
                break
            elif key == 'q':
                return
        game.reset()
        msg = ''


if __name__ == "__main__":
    curses.wrapper(main)
