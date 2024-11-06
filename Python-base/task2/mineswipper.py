import random


class Cell:
    """
    Класс для представления одной ячейки на игровом поле.

    Attrs:
        around_mines (int): Число мин в ближайших ячейках
        mine (bool): Указывает, является ли данная ячейка миной
        is_open (bool): Указывает, открыта ли ячейка
    """

    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        """
        Инициализирует ячейку с указанным количеством мин вокруг
        и флагом, обозначающим есть ли мина в данной ячейке.

        Args:
            around_mines (int): Количество мин вокруг ячейки.
            mine (bool): True при наличии мины в ячейке, иначе False
        """

        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.is_open: bool = False

    def __str__(self) -> str:
        """
        Возвращает строковое представление ячейки, в зависимости
        от ее состояния: "*" если мина, "#" если ячейка закрыта,
        количество мин вокруг, если ячейка не мина и открыта.
        """

        if self.mine:
            return "*"
        if not self.is_open:
            return "#"
        return str(self.around_mines)


class GamePole:
    """
    Класс, представляющий игровое поле с заданными
    размером и общим количеством мин.

    Attrs:
        __mines_number (int): Общее число мин на поле
        __matrix_size (int): Размер грового поля
        __pole (list[list[Cell]]): Двумерный список ячеек, представляющий игровое поле
    """

    def __init__(self, n: int, m: int) -> None:
        """
        Инициализирует игровое поле с заданными размером и общим количеством мин.

        Args:
            n (int): Размер игрового поля
            m (int): Общее число мин на поле
        """

        self.__mines_number: int = m
        self.__matrix_size: int = n
        self.__pole: list[list[Cell]] = [[Cell() for _ in range(n)] for _ in range(n)]
        self.__lay_mines()
        self.__fill_mine_around_cells()

    def __lay_mines(self) -> None:
        """
        Размечает случайным образом мины на игровом поле.
        """

        cell_positions = []
        for i in range(self.__matrix_size):
            for k in range(self.__matrix_size):
                cell_positions.append((i, k))

        random.shuffle(cell_positions)

        for raw, col in cell_positions[: self.__mines_number]:
            self.__pole[raw][col].mine = True

    def __fill_mine_around_cells(self) -> None:
        """
        Заполняет каждую ячейку, не занятую миной, числом
        мин, находящихся вокруг нее.
        """

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

    def show(self) -> None:
        """
        Отображает в консоли игровое поле.
        """

        for row in self.__pole:
            print(*[cell for cell in row], sep=" ")


game = GamePole(10, 12)
