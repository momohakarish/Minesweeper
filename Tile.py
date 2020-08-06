class Tile:

    def __init__(self):
        self.number = 0
        self.bomb = False
        self.flagged = False
        self.revealed = False

    def __repr__(self):
        if self.bomb:       # Checks if the tile contains a bomb
            return 'B'
        else:
            return str(self.number)

    def __eq__(self, other):
        return self.number == other.number and self.bomb == other.bomb and self.revealed == other.revealed

