from Tile import Tile
import random


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = self.__create_board()

    # Returning a string representation as a grid
    def __repr__(self):
        mat = ''
        for row in self.board:
            mat += row.__repr__() + '\n'
        return mat

    def get_cell(self, x, y):
        return self.board[y][x]

    def __create_board(self):
        temp = []
        for row in range(self.width):
            temp.append([])
            for column in range(self.height):
                temp[row].append(Tile())
        return temp

    def fill_board(self, bomb_amount, coordinates):
        count = 0       # Number of bombs placed
        while count < bomb_amount:
            # Generating the coordinates
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if x == coordinates[0] and y == coordinates[1]:      # The first click can't be on a bomb so we exclude the first position clicked on from bomb placement
                continue
            # Placing the bomb and updating neighbouring cells accordingly
            if not self.board[y][x].bomb:
                self.board[y][x].bomb = True
                self.__update_neighbours(x, y)
                count += 1

    # Updates all the numbers of neighbours of the bombs placed
    # O(1) Time complexity
    def __update_neighbours(self, x, y):
        cells = self.__get_neighbour_cells(x, y)
        for cell in cells:
            cell.number += 1

    # Returns a list of cells of all cells neighbouring a cell in the board
    # O(1) Time complexity
    def __get_neighbour_cells(self, x, y):
        cells = []
        if self.__valid_point(x - 1, y - 1):   # Top left
            cells.append(self.board[y-1][x-1])
        if self.__valid_point(x, y - 1):     # Top
            cells.append(self.board[y-1][x])
        if self.__valid_point(x + 1, y - 1):   # Top right
            cells.append(self.board[y-1][x+1])
        if self.__valid_point(x - 1, y):     # Left
            cells.append(self.board[y][x-1])
        if self.__valid_point(x + 1, y):     # Right
            cells.append(self.board[y][x+1])
        if self.__valid_point(x - 1, y + 1):     # Bottom left
            cells.append(self.board[y+1][x-1])
        if self.__valid_point(x, y + 1):     # Bottom
            cells.append(self.board[y+1][x])
        if self.__valid_point(x + 1, y + 1):     # Bottom Right
            cells.append(self.board[y+1][x+1])
        return cells

    # Inner function for revealing all zeroes and creating a list of their neighbours
    def __reveal_zeros(self, x, y, cells):
        # Stop check
        if not self.__valid_point(x,  y) or self.board[y][x].number != 0 or self.board[y][x].revealed:
            return

        # Adding cells to the list
        temp = self.__get_neighbour_cells(x, y)
        cells.extend(temp)

        # Recursion continuation
        self.board[y][x].revealed = True
        self.__reveal_zeros(x + 1, y, cells)
        self.__reveal_zeros(x - 1, y, cells)
        self.__reveal_zeros(x, y + 1, cells)
        self.__reveal_zeros(x, y - 1, cells)

    def reveal_zeroes(self, x, y):
        cells = []
        self.__reveal_zeros(x, y, cells)
        for cell in cells:
            if not cell.bomb:
                cell.revealed = True

    # Checks if a point in the matrix is valid
    # O(1) Time complexity
    def __valid_point(self, x, y):
        if self.width > x >= 0 and self.height > y >= 0:
            return True
        return False

    def get_revealed(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell.revealed:
                    count += 1
        return count

    def get_bombed(self):
        cells = []
        for row in self.board:
            for cell in row:
                if cell.bomb:
                    cells.append(cell)
        return cells
