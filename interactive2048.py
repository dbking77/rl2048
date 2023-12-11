#!/usr/bin/env python3

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
