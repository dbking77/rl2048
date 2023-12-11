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

import gymnasium as gym
import math
import random
from game2048 import Game2048


class EnvironmentBase:
    def __init__(self):
        self.game = Game2048()
        self.reset()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(0, 11, shape=(16,))

    def get_observation(self):
        raise RuntimeError("TODO")

    def get_observation_one_hot(self):
        obs = []

        def to_one_hot(value: int):
            vec = [0 for _ in range(12)]
            vec[value] = 1
            return vec
        for v in self.game.grid._grid:
            obs += to_one_hot(v)
        return obs

    def get_observation_bit_vec(self):
        obs = []

        def to_bit_vec(value: int):
            vec = []
            for i in range(4):
                vec.append(value & 1)
                value >>= 1
            return vec
        for v in self.game.grid._grid:
            obs += to_bit_vec(v)
        return obs

    def get_reward(self, success):
        terminated = False
        if not success:
            reward = -2048.0
            terminated = True
        else:
            max_value = self.game.max_value()
            score = 1 << max_value
            if score > self.prev_score:
                reward = score - self.prev_score
                self.prev_score = score
            else:
                reward = -1.0
            if max_value >= 2048:
                terminated = True
        return (terminated, reward)

    def reset(self):
        self.game.reset()
        self.prev_score = 0
        state = self.get_observation()
        info = None  # TODO
        return (state, info)

    def step(self, action):
        direction = "LDUR"[action]
        self.game.slide(direction)
        success = self.game.add_tile()
        terminated, reward = self.get_reward(success)
        truncated = False
        info = {}
        observation = self.get_observation()
        return (observation, reward, terminated, truncated, info)

    def render(self):
        self.game.display()

    def close(self):
        print("CLOSE")


class Environment1(EnvironmentBase):
    def get_observation(self):
        return self.game.grid._grid[:]


class Environment2(EnvironmentBase):
    def get_observation(self):
        return self.get_observation_bit_vec()


class Environment3(EnvironmentBase):
    def get_observation(self):
        return self.get_observation_one_hot()


class Environment4(EnvironmentBase):
    def get_observation(self):
        return self.get_observation_one_hot()

    def get_reward(self, success):
        terminated = False
        if not success:
            reward = -(2048.0**2)
            terminated = True
        else:
            score = 0.0
            for v in self.game.grid._grid:
                score += (1 << v)**2
            # score would automatically increase when getting a new tile
            # each new
            drag = 5.2  # (4*0.9 + 16*0.1)
            reward = score - self.prev_score - drag
            self.prev_score = score
            if self.game.max_value() >= 2048:
                terminated = True
        return (terminated, reward)


class Environment5(Environment4):
    def get_observation(self):
        self.game.grid = self.game.grid.heavy_side_flip()
        return self.get_observation_one_hot()


class Environment6(Environment5):
    def reset(self):
        super().reset()
        if random.random() > 0.75:
            self.game.resetRandom(5, 7)
            self.game.slide("U")
            self.game.slide("L")
        state = self.get_observation()
        info = None  # TODO
        return (state, info)


class Environment7(EnvironmentBase):
    def get_observation(self):
        self.game.grid = self.game.grid.heavy_side_flip()
        return self.get_observation_one_hot()

    def get_reward(self, success):
        terminated = False
        if not success:
            reward = -2048.0
            terminated = True
        elif self.game.max_value() >= 2048:
            reward = 2048.0
            terminated = True
        else:
            reward = 1.0
        return (terminated, reward)


class Environment8(EnvironmentBase):
    def reset(self):
        super().reset()
        self.prev_score = self.get_score()
        state = self.get_observation()
        info = None  # TODO
        return (state, info)

    def get_observation(self):
        self.game.grid = self.game.grid.heavy_side_flip()
        return self.get_observation_one_hot()

    def get_score(self):
        score = 0.0
        for v in self.game.grid._grid:
            score += (1 << v)**2
        score = math.sqrt(score)
        return score

    def get_reward(self, success):
        terminated = False
        if not success:
            reward = -2048.0
            terminated = True
        else:
            score = self.get_score()
            self.prev_score = score
            reward = score - self.prev_score
            if self.game.max_value() >= 2048:
                reward += 2048.0
                terminated = True
        return (terminated, reward)


class Environment9(EnvironmentBase):
    def __init__(self):
        self.iterations = 0
        super().__init__()

    def reset(self):
        super().reset()
        self.iterations += 1
        random_stop_iteration = 40000
        random_thresh = self.iterations / random_stop_iteration
        print("Random thresh", random_thresh)
        if random.random() > random_thresh:
            self.game.resetRandom(7, 9)
            self.game.slide("U")
            self.game.slide("L")
            self.game.grid = self.game.grid.heavy_side_flip()
            self.game.display()
        self.prev_score = self.get_score()
        state = self.get_observation()
        info = None  # TODO
        return (state, info)

    def get_observation(self):
        self.game.grid = self.game.grid.heavy_side_flip()
        return self.get_observation_one_hot()

    def get_score(self):
        score = 0.0
        for v in self.game.grid._grid:
            score += (1 << v)**2
        score = math.sqrt(score)
        return score

    def get_reward(self, success):
        terminated = False
        if not success:
            reward = -2048.0
            terminated = True
        else:
            score = self.get_score()
            self.prev_score = score
            reward = score - self.prev_score
            if self.game.max_value() >= 2048:
                reward += 2048.0
                terminated = True
        reward /= 2048.0
        return (terminated, reward)


class Environment10(EnvironmentBase):
    def __init__(self):
        super().init()
        self.iterations = 0

    def reset(self):
        super().reset()
        self.iterations += 1
        random_stop_iteration = 10000
        random_thresh = self.iterations / random_stop_iteration
        print("Random thresh", random_thresh)
        if random.random() > random_thresh:
            self.game.resetRandom(7, 9)
            self.game.slide("U")
            self.game.slide("L")
            self.game.grid = self.game.grid.heavy_side_flip()
            self.game.display()
        self.prev_score = self.get_score()
        state = self.get_observation()
        info = None  # TODO
        return (state, info)

    def get_observation(self):
        self.game.grid = self.game.grid.heavy_side_flip()
        return self.get_observation_one_hot()

    def get_reward(self, success):
        terminated = False
        if not success:
            reward = -2048.0
            terminated = True
        elif self.game.max_value() >= 2048:
            reward = 2048.0
            terminated = True
        else:
            reward = 1.0
        return (terminated, reward)
