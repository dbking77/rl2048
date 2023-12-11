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


from game2048 import Game2048
import math
import random
import numpy as np


class PlayerRandom:
    def __init__(self, game):
        self.game = game

    def run(self, max_iterations):
        self.game.reset()
        directions = "LDUR"
        for iteration in range(max_iterations):
            direction = random.choice(directions)
            self.game.slide(direction)
            if not self.game.add_tile():
                break
        max_value = self.game.max_value()
        return (iteration, max_value)


class PlayerMaxScore:
    def __init__(self, game):
        self.game = game

    def get_score(self):
        score = 0.0
        for v in self.game.grid._grid:
            score += (1 << v)**2
        return math.sqrt(score)

    def run(self, max_iterations):
        self.game.reset()
        directions = "LDUR"
        for iteration in range(max_iterations):
            best_score = 0
            best_direction = None
            checkpoint = self.game.save()
            for direction in directions:
                self.game.slide(direction)
                score = self.get_score()
                if score > best_score:
                    best_score = score
                    best_direction = direction
                self.game.restore(checkpoint)
            self.game.slide(best_direction)
            if not self.game.add_tile():
                break
        max_value = self.game.max_value()
        return (iteration, max_value)


class PlayerCorner(PlayerMaxScore):
    def __init__(self, game):
        self.game = game

    def get_score(self):
        score = super().get_score()
        # if max
        max_value = 0
        max_loc = None
        for x in range(4):
            for y in range(4):
                v = self.game.grid[x, y]
                if v > max_value:
                    max_value = v
                    max_loc = (x, y)
        if max_loc in [(0, 3), (0, 0), (3, 0), (3, 3)]:
            score += (1 << max_value)
        return score


def main():
    game = Game2048()
    debug = False
    players = {
        'random': PlayerRandom(game),
        'max_score': PlayerMaxScore(game),
        'corner': PlayerCorner(game),
    }
    max_iterations = 1200
    player_results = {}
    for name, player in players.items():
        results = []
        for trial in range(10):
            iteration, max_value = player.run(max_iterations)
            results.append((iteration, max_value))
            if debug:
                print("Iteration ", iteration, "max value ", max_value)
                game.display()
            else:
                if trial % 100 == 0:
                    print(f"{name} : trial {trial}")
        player_results[name] = results

    print("-"*80)
    print(f"{'name':<20s} {'iter':<10} {'raw':<10} {'value':<10}")
    print("-"*80)
    for name, results in player_results.items():
        iters = []
        raws = []
        vals = []
        for trial, (iter, raw) in enumerate(results):
            iters.append(iter)
            raws.append(raw)
            vals.append(1 << raw)
        iters = np.array(iters)
        raws = np.array(raws)
        vals = np.array(vals)

        print(f"{name:<20s}")
        for stat in ('mean', 'max'):
            msg = f"    {stat:<20s}"
            for arr in (iters, raws, vals):
                v = getattr(arr, stat)()
                msg += f" {v:<10.2f}"
            print(msg)


if __name__ == "__main__":
    main()
