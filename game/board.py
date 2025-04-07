import random
from .cell import Cell
from .utils import get_neighbors

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self._place_mines()
        self._calculate_neighbor_mines()

    def _place_mines(self):
        all_coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        mines = random.sample(all_coords, self.num_mines)
        for x, y in mines:
            self.grid[x][y].is_mine = True

    def _calculate_neighbor_mines(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                if cell.is_mine:
                    continue
                neighbors = get_neighbors(x, y, self.width, self.height)
                count = sum(1 for nx, ny in neighbors if self.grid[nx][ny].is_mine)
                cell.neighbor_mines = count

    def reveal(self, x, y):
        cell = self.grid[x][y]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        if cell.neighbor_mines == 0 and not cell.is_mine:
            for nx, ny in get_neighbors(x, y, self.width, self.height):
                self.reveal(nx, ny)

    def toggle_flag(self, x, y):
        cell = self.grid[x][y]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def print_board(self, reveal_mines=False):
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                cell = self.grid[x][y]
                if reveal_mines and cell.is_mine:
                    row += '* '
                else:
                    row += str(cell) + ' '
            print(row)
