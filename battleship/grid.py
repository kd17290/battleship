from battleship.exceptions import CoordinateParseException


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols


class Position:
    def __init__(self, row_no, col_no):
        self.row_no = row_no
        self.col_no = col_no

    def __repr__(self):
        return "{0}{1}".format(chr(65 + self.row_no), self.col_no + 1)

    def __eq__(self, other):
        return other.row_no == self.row_no and other.col_no == self.col_no

    def __hash__(self):
        return self.__repr__().__hash__()

    @staticmethod
    def parse_position(pos_str):
        try:
            if not (pos_str and len(pos_str) > 1):
                raise CoordinateParseException("Invalid position string")
            row_no = ord(pos_str[0]) - 65
            col_no = int(pos_str[1:]) - 1
        except CoordinateParseException as e:
            raise e
        except Exception as e:
            raise CoordinateParseException("Invalid position string")
        return Position(row_no=row_no, col_no=col_no)


class Direction:
    X = "X"
    Y = "Y"


class ShipPosition:
    def __init__(self, ship, direction, position):
        self.ship = ship
        self.direction = direction
        self.position = position
        self.hits = set()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{0} at {1} in {2} direction".format(self.ship, self.position, self.direction)

    def get_cells(self):
        # return all cells this ship occupies
        if self.direction == Direction.X:
            return [Position(row_no=self.position.row_no, col_no=col) for col in
                    range(self.position.col_no, self.position.col_no + self.ship.length)]
        else:
            return [Position(row_no=row, col_no=self.position.col_no) for row in
                    range(self.position.row_no, self.position.row_no + self.ship.length)]

    def is_sunk(self):
        return len(self.hits) == self.ship.length

    def is_head_cell(self, position):
        return position == self.position
