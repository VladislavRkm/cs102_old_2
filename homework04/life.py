import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for x in range(self.cols)] for y in range(self.rows)]
        else:
            grid = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.grid = grid
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        self.neighbours = []
        y_index = cell[0]
        x_index = cell[1]

        mask_main = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        add_mask = []
        if x_index == 0:
            add_mask.append([[0, 1, 1] for i in range(3)])
        if x_index == self.cols - 1:
            add_mask.append([[1, 1, 0] for i in range(3)])
        if y_index == 0:
            add_mask.append([[0, 0, 0] if i == 0 else [1, 1, 1] for i in range(3)])
        if y_index == self.rows - 1:
            add_mask.append([[0, 0, 0] if i == 2 else [1, 1, 1] for i in range(3)])
        for mask in add_mask:
            for i in range(3):
                for j in range(3):
                    mask_main[i][j] *= mask[i][j]

        for i in range(3):
            for j in range(3):
                if mask_main[i][j]:
                    self.neighbours.append(self.grid[y_index - 1 + i][x_index - 1 + j])

        return self.neighbours

    def get_next_generation(self) -> Grid:
        for i in range(self.rows):
            for j in range(self.cols):
                count = 0
                for k in self.get_neighbours((i, j)):
                    if k:
                        count += 1
                if self.grid[i][j] == 0:
                    if count == 3:
                        self.grid[i][j] = 1
                else:
                    if count != 2 and count != 3:
                        self.grid[i][j] = 0
        return self.grid

        pass

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.max_generations >= self.generations
        else:
            return True
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        temp_grid = []
        rows = sum(1 for line in open(filename))
        with open(filename, "r") as file:
            for i in range(rows):
                lines = file.readline().replace("\n", "")
                for j in lines:
                    temp_grid.append(int(j))
                grid.append(temp_grid)
                temp_grid = []
        cols = len(grid[0])
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = grid.copy()
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        out = ""
        with open(filename, "w") as file:
            for row in range(self.rows):
                out += "".join(map(str, self.curr_generation[row])) + "\n"
            out = out.rstrip("\n")
            file.write(out)
        pass
