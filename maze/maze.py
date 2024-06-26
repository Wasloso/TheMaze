from __future__ import annotations
import random

# Non modular import to avoid circural import
from .cell import Cell
from .player import Direction


class Maze:
    def __init__(
            self,
            cell_size: int,
            rows: int = 20,
            columns: int = 32,
            player_start: tuple[int, int] = None,
            objective_position: tuple[int, int] = None,
            name: str = None,
    ):
        self.rows: int = rows
        self.columns: int = columns
        self.cell_size: int = cell_size
        self.player_start = player_start
        self.objective_position = objective_position
        self.grid: list[list[Cell]] = []
        self.name = name
        self.player_start_pos = None
        self.objective_position_pos = None

    def create_grid(self) -> list[list[Cell]]:
        grid = []
        for y in range(self.rows):
            row = [Cell(x, y, self.cell_size, True) for x in range(self.columns)]
            grid.append(row)
        self.grid = grid
        return grid

    def randomize_maze(self) -> None:
        self.grid = self.create_grid()

        def get_frontier(cell: Cell) -> list[Cell]:
            frontier = []
            for direction in Direction:
                next_cell = tuple(map(sum, zip(cell.position, direction.value)))
                if 0 < next_cell[1] < self.rows - 1 and 0 < next_cell[0] < self.columns - 1:
                    frontier.append(self.grid[next_cell[1]][next_cell[0]])
            return frontier

        def choose_starting_pos() -> Cell:
            return random.choice([cell for row in self.grid for cell in row])

        starting_pos = choose_starting_pos()
        while starting_pos.position[0] in [0, self.columns - 1] or starting_pos.position[1] in [0, self.rows - 1]:
            starting_pos = choose_starting_pos()
        starting_pos.collidable = False
        self.player_start = starting_pos.rect.center
        last_pos = starting_pos
        frontier = get_frontier(starting_pos)
        while frontier:
            next_cell = frontier.pop(random.randint(0, len(frontier) - 1))
            neighbour_cells = get_frontier(next_cell)
            number_of_path_cells = sum([not cell.collidable for cell in neighbour_cells])
            if number_of_path_cells == 1:
                next_cell.collidable = False
                frontier += neighbour_cells
            last_pos = next_cell
        self.objective_position = last_pos.rect.center

    def __repr__(self) -> str:
        return f"Maze({self.cell_size=}, {self.rows=}, {self.columns=}, {self.player_start=}, {self.objective_position=}, {self.name=})"

    @staticmethod
    def from_json(json) -> Maze:
        grid = json["grid"]

        maze = Maze(json["cell_size"], len(grid[0]), len(grid), name=json["name"])
        for i, row in enumerate(grid):
            maze_row = []
            for j, cell in enumerate(row):
                collidable: bool = cell
                if cell == "P":
                    maze.player_start_pos = (i, j)
                    maze.player_start = maze.get_rect_position(i, j)
                    collidable = False
                if cell == "O":
                    maze.objective_position_pos = (i, j)
                    maze.objective_position = maze.get_rect_position(i, j)
                    collidable = False

                maze_row.append(Cell(j, i, maze.cell_size, collidable))
            maze.grid.append(maze_row)
        return maze

    def to_json(self) -> dict:
        player_pos = self.get_cell_index(*self.player_start)
        objective_pos = self.get_cell_index(*self.objective_position)
        grid = []
        for row in self.grid:
            grid_row = []
            for cell in row:
                if (
                        row.index(cell) == player_pos[0]
                        and self.grid.index(row) == player_pos[1]
                ):
                    grid_row.append("P")

                elif (
                        row.index(cell) == objective_pos[0]
                        and self.grid.index(row) == objective_pos[1]
                ):
                    grid_row.append("O")
                elif cell.collidable:
                    grid_row.append(1)
                else:
                    grid_row.append(0)
            grid.append(grid_row)
        return {
            "name": self.name,
            "cell_size": self.cell_size,
            "grid": grid,
        }

    def get_cell_index(self, x, y) -> tuple[int, int]:
        return x // self.cell_size, y // self.cell_size

    def get_rect_position(self, row, column) -> tuple[int, int]:
        return (
            column * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )

    def reset_visibility(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.visited = False
