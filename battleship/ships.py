class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def __repr__(self):
        return "({0} , {1})".format(self.name, self.length)
