from game2048 import Game2048
from grid4x4 import Grid4x4

def test_slide_left():
    grid = Grid4x4("""
                   1122
                   .3.3
                   .414
                   5665
                   """)
    game = Game2048(grid)
    game.slide("L")

    expect = Grid4x4("""
                     23..
                     4...
                     414.
                     575.
                     """)
    
    assert game.grid == expect, f"\n{game.grid}"