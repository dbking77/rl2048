# Introduction
Simple DeepQ RL demo for the 2048 Game using pytorch

## Files
- deep-q.ipynb : notebook with Deep-Q learning for 2048
- game2048.py : core 2048 game logic
- grid4x4.py : 4x4 grid, with some useful utility functions
- interactive2048.py : interactive (keyboard/curses) game
- gym_env.py : different semi-compatible [OpenAI Gym environments](https://gymnasium.farama.org/) for training
- players.py : different hand-coded players for 2048

## TODO
- github actions
    - run typing checks
    - run flake8

## Deep-Q RL
[See Deep-Q RL](doc/deep_q/deep_q.md)

## Interactive
There is an interactive version of the game that uses curses library to display game board and capture input
```
./interactive2048.py
```

Use arrow keys to slide values or 'q' to quit.
Displayed values are log2 of 2048 values (1 --> 2, 2 --> 4, 3 --> 8).
```
..33
...2
....
1..1

Iteration 10
Max Value 3
```

When game board fills you lose.  Use 'r' to restart.
```
2651
4312
1641
2312

Iteration 108
Max Value 6
FAILURE... Press 'q' to quit and 'r' to restart
```

## Players
Hand-coded 2048 players as base-line for other approaches.

```
--------------------------------------------------------------------------------
name                 iter       raw        value     
--------------------------------------------------------------------------------
random              
    avg              82.92      5.90       67.92     
    max              197.00     8.00       256.00    
max_score           
    avg              237.36     7.81       251.49    
    max              497.00     9.00       512.00    
corner              
    avg              250.63     7.92       271.81    
    max              614.00     10.00      1024.00    
```

### Random
Randomly pick action including same action twice

### Max Score

Tries moving in each direction and scores each result (before adding random tile).   
Always chooses direction with best score.
Score is sum of raw values squared.

### Corner

Similar to max_score, with a bonus to keeping maximum block in corner