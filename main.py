import sys

from battleship.game import Game
from battleship.grid import Grid
from battleship.ships import Ship

if __name__ == "__main__":
    is_debug = "--debug" in sys.argv
    try:
        # Initialize grid and the game
        if is_debug:
            print("Initializing game...")
        ships = [
            Ship(length=2, name="Patrol"),
            Ship(length=3, name="Submarine"),
            Ship(length=4, name="Battleship"),
            Ship(length=5, name="Carrier")
        ]
        grid = Grid(10, 10)
        game = Game(grid=grid, ships=ships)
        if is_debug:
            print("Game initialized...")
            game.print_grid()
        game.play()
    except KeyboardInterrupt:
        print("")
        exit()
