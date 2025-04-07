class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def __repr__(self):
        if self.is_flagged:
            return "F"
        elif not self.is_revealed:
            return "□"
        elif self.is_mine:
            return "*"
        else:
            return str(self.neighbor_mines)
