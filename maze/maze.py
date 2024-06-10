import math
from .cell import Cell
import random
from pygame import Surface
import json
import ast


class Maze:
    def __init__(
        self,
        cell_size: int,
        rows: int = 20,
        columns: int = 32,
        player_start: tuple[int, int] = None,
        objective_position: tuple[int, int] = None,
    ):
        self.rows: int = rows
        self.columns: int = columns
        self.cell_size: int = cell_size
        self.player_start = player_start
        self.objective_position = objective_position
        self.grid: list[list[Cell]] = None

    def create_grid(self) -> list[list[Cell]]:
        grid = []
        for y in range(self.columns):
            row = []
            for x in range(self.rows):
                cell = Cell(
                    self.cell_size, x * self.cell_size, y * self.cell_size, True
                )
                row.append(cell)
            grid.append(row)
        return grid

    def randomize_maze(self):
        for row in self.grid:
            for cell in row:
                if random.random() < 0.2:
                    cell.change_collidable(True)

    def __repr__(self):
        return f"Maze({self.grid=}, {self.cell_size=}, {self.rows=}, {self.columns=}, {self.player_start=}, {self.objective_position=})"

    # TODO jakas fajna metoda generowania losowego labiryntu
    @staticmethod
    def generate_maze(cell_size, rows, columns):
        maze = Maze(cell_size, rows, columns)
        maze.grid = maze.create_grid()

        player_start = (
            random.randint(1, rows - 2) * cell_size + cell_size // 2,
            random.randint(1, columns - 2) * cell_size + cell_size // 2,
        )
        maze.player_start = player_start
        objective_position = (
            random.randint(1, rows - 2) * cell_size + cell_size // 2,
            random.randint(1, columns - 2) * cell_size + cell_size // 2,
        )
        maze.objective_position = objective_position
        cp, rp = player_start[0] // cell_size, player_start[1] // cell_size
        maze.change_collidable(cp, rp)
        co, ro = objective_position[0] // cell_size, objective_position[1] // cell_size
        maze.change_collidable(co, ro)
        return maze

    def change_collidable(self, column, row):
        self.grid[row][column].change_collidable()
        if self.grid[row][column].collidable:
            self.collidable_cells.append(self.grid[row][column])
        else:
            self.collidable_cells.remove(self.grid[row][column])

    @staticmethod
    def from_json(json):
        grid = json["grid"]
        columns = len(grid)
        rows = len(grid[0])
        maze = Maze(json["cell_size"], rows, columns)
        maze.grid = []
        for j, row in enumerate(grid):
            maze_row = []
            for i, cell in enumerate(row):
                if cell == 1:
                    cell = Cell(
                        maze.cell_size, i * maze.cell_size, j * maze.cell_size, True
                    )
                    maze_row.append(cell)
                else:
                    if cell == "P":
                        maze.player_start = maze.set_rect_position(j, i)
                    elif cell == "O":
                        maze.objective_position = maze.set_rect_position(j, i)
                    maze_row.append(
                        Cell(
                            maze.cell_size,
                            i * maze.cell_size,
                            j * maze.cell_size,
                            False,
                        )
                    )
            maze.grid.append(maze_row)

        return maze

    def set_rect_position(self, row, column):
        return (
            column * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )
