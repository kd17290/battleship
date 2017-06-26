import random
from collections import OrderedDict

from battleship.exceptions import CoordinateParseException
from battleship.grid import Direction, Position, ShipPosition


class Game:
    def __init__(self, grid, ships):
        self.grid = grid
        self.ships = []
        for ship in ships:
            self.ships.append(self.get_random_position(self.grid, ship, self.ships))
        self.played_coords = set()

    def _print_col_header(self, cols):
        print("|___", end="")
        print("|{0}|".format("|".join(
            ["_{:2d}".format(col_no + 1) for col_no in range(cols)]
        )), end="")

    def _print_row_header(self, row_no):
        print("|_{0}_".format(chr(65 + row_no)), end="")

    def print_grid(self):
        grid = OrderedDict()
        for row in range(self.grid.rows):
            grid[str(row)] = OrderedDict({str(col): "___" for col in range(self.grid.cols)})
        for ship in self.ships:
            cells = set(ship.get_cells())
            intact_cells = cells - ship.hits
            for cell in intact_cells:
                if ship.direction == Direction.X:
                    cell_str = "_<-" if ship.is_head_cell(cell) else "_-_"
                else:
                    cell_str = "_↑_" if ship.is_head_cell(cell) else "_|_"
                grid[str(cell.row_no)][str(cell.col_no)] = cell_str
            for cell in ship.hits:
                grid[str(cell.row_no)][str(cell.col_no)] = "_x_"

        self._print_col_header(self.grid.cols)
        print("")
        for row_no in range(self.grid.rows):
            self._print_row_header(int(row_no))
            for col_no in range(self.grid.cols):
                print("|{0}".format(grid[str(row_no)][str(col_no)]), end="")
            print("|")

    @classmethod
    def get_random_position(cls, grid, ship, existing_ships):
        direction = cls.get_random_direction()
        if direction == Direction.X:
            rows_range = (0, grid.rows)
            cols_range = (0, grid.cols - ship.length)
        else:
            rows_range = (0, grid.rows - ship.length)
            cols_range = (0, grid.cols)
        row_no = random.randrange(*rows_range)
        col_no = random.randrange(*cols_range)
        position = Position(row_no=row_no, col_no=col_no)
        ship_to_add = ShipPosition(ship=ship, position=position, direction=direction)
        if cls.check_ship_collision(existing_ships, ship_to_add):
            return cls.get_random_position(grid, ship, existing_ships)
        return ship_to_add

    @classmethod
    def check_collision(cls, ships, position):
        for ship in ships:
            if cls.check_arrays_intersection(ship.get_cells(), [position]):
                return ship
        return False

    @classmethod
    def check_ship_collision(cls, ships, ship_to_check):
        for ship in ships:
            if cls.check_arrays_intersection(ship.get_cells(), ship_to_check.get_cells()):
                return True
        return False

    @classmethod
    def check_arrays_intersection(cls, arr1, arr2):
        for item in arr1:
            if item in arr2:
                return True
        return False

    @classmethod
    def get_random_direction(cls):
        return random.choice([Direction.X, Direction.Y])

    def check_hit(self, position):
        ship = self.check_collision(self.ships, position)
        if ship:
            ship.hits.add(position)
        return ship

    def check_all_ships_hit(self):
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

    def play(self):
        while True:
            input_command = input("Enter a coordinate: ")
            if input_command == "I LOSE":
                self.print_grid()
                break
            else:
                try:
                    position = Position.parse_position(input_command)
                    if position.col_no not in range(self.grid.cols) or position.row_no not in range(self.grid.rows):
                        raise CoordinateParseException("Please enter a valid coordinate")
                    if position in self.played_coords:
                        raise CoordinateParseException(
                            "You've already played this coordinate. Please enter a different coordinate"
                        )
                except CoordinateParseException as e:
                    print(e)
                    continue
                self.played_coords.add(position)
                ship = self.check_hit(position)
                if not ship:
                    print("MISS")
                    continue
                if ship.is_sunk():
                    print("SINK")
                else:
                    print("HIT")
                if self.check_all_ships_hit():
                    print("WIN")
                    break
                continue
