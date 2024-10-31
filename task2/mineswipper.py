import random


class Cell:
    def __init__(self, around_mines: int = 0, mine: bool = False):
        self.around_mines = around_mines
        self.mine = mine
        self.is_open: bool = False

    def __str__(self):
        if self.mine:
            return "*"
        if not self.is_open:
            return "#"
        return str(self.around_mines)


class GamePole:
    def __init__(self, n: int, m: int):
        self.__mines_number = m
        self.__matrix_size = n
        self.__pole = [[Cell() for _ in range(n)] for _ in range(n)]
        self.__lay_mines()
        self.__fill_mine_around_cells()

    def __lay_mines(self):
        cell_positions = []
        for i in range(self.__matrix_size):
            for k in range(self.__matrix_size):
                cell_positions.append((i, k))

        random.shuffle(cell_positions)

        for raw, col in cell_positions[:self.__mines_number]:
            self.__pole[raw][col].mine = True

    def __fill_mine_around_cells(self):
        neighbor_cells_offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for row in range(self.__matrix_size):
            for col in range(self.__matrix_size):

                if not self.__pole[row][col].mine:
                    mines_count = 0

                    for x, y in neighbor_cells_offsets:
                        neighbor_row = row + x
                        neighbor_col = col + y

                        if (
                            0 <= neighbor_row < self.__matrix_size
                            and 0 <= neighbor_col < self.__matrix_size
                        ):
                            if self.__pole[neighbor_row][neighbor_col].mine:
                                mines_count += 1

                    self.__pole[row][col].around_mines = mines_count

    def show(self):
        for row in self.__pole:
            print(*[cell for cell in row], sep=" ")


game = GamePole(10, 12)
game.show()
