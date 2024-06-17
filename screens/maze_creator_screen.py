from typing import Optional

import pygame
from pygame.surface import Surface
from pygame.transform import scale

from assets.assets_loader import AssetsLoader
from maze.cell import Cell
from maze.maze import Maze
from ui_components.button import Button
from . import ScreenBase
from .screen_base import MAZE_CREATOR


class MazeCreatorScreen(ScreenBase):
    def __init__(
        self,
        previous_screen: Optional[ScreenBase],
        manager,
        maze_manager,
        maze: Maze = None,
    ) -> None:
        super().__init__(previous_screen, manager, screen_name=MAZE_CREATOR)

        self.maze_manager = maze_manager
        self.maze: Maze = maze
        self.back_button: Button = Button.go_back_button(
            position=(25, 25),
            desired_size=(50, 50),
            callback=lambda: self.manager.back(self.previous_screen),
        )

        self.confirm_button = Button(
            desired_size=(50, 50),
            position=(75, 25),
            image=AssetsLoader.get_button("confirm_button"),
            alt_image=AssetsLoader.get_button("confirm_button", hovered=True),
            callback=(lambda: self.manager.back(previous_screen)) if maze else None,
        )
        if not maze:
            maze = Maze(40)
            maze.create_grid()
            self.maze = maze

        self.player_img = scale(
            AssetsLoader.get_player("idle"),
            (self.maze.cell_size // 3, self.maze.cell_size // 3),
        )
        self.objective_img = scale(
            AssetsLoader.get_objective(),
            (self.maze.cell_size // 2, self.maze.cell_size // 2),
        )
        self.randomize_button = Button(
            desired_size=(50, 50),
            image=AssetsLoader.get_button("randomize_button"),
            alt_image=AssetsLoader.get_button("randomize_button", hovered=True),
            callback=(lambda m=self.maze: m.randomize_maze()) if maze else None,
        )

        transparent_surf = Surface(
            (self.maze.cell_size, self.maze.cell_size), pygame.SRCALPHA
        )
        transparent_surf.fill((0, 0, 0, 0))
        self.wall_img = pygame.transform.scale(
            AssetsLoader.get_cell("wall"), (self.maze.cell_size, self.maze.cell_size)
        )
        self.floor_img = pygame.transform.scale(
            AssetsLoader.get_cell("floor"), (self.maze.cell_size, self.maze.cell_size)
        )

        self.cell_buttons = []
        self.cells = []
        for i, row in enumerate(self.maze.grid):
            cell: Cell
            for j, cell in enumerate(row):
                self.cells.append(cell)
                self.cell_buttons.append(
                    Button(
                        image=transparent_surf,
                        position=cell.rect.center,
                        desired_size=(self.maze.cell_size, self.maze.cell_size),
                        callback=(
                            (lambda c=cell: c.change_collidable())
                            if 0 < i < len(self.maze.grid) - 1 and 0 < j < len(row) - 1
                            else None
                        ),
                    )
                )

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        [
            surface.blit(
                self.wall_img if cell.collidable else self.floor_img, cell.rect.topleft
            )
            for row in self.maze.grid
            for cell in row
        ]
        [button.draw(surface) for button in self.cell_buttons]
        self.back_button.draw(surface)
        self.confirm_button.draw(surface)
        self.randomize_button.rect.topright = surface.get_rect().topright
        self.randomize_button.draw(surface)

        if self.maze.player_start:
            rect = self.player_img.get_rect()
            rect.center = self.maze.player_start
            surface.blit(self.player_img, rect)
        if self.maze.objective_position:
            rect = self.objective_img.get_rect()
            rect.center = self.maze.objective_position
            surface.blit(self.objective_img, rect)

    def update(self, events, keys) -> None:
        for event in events:
            self.confirm_button.update(event)
            self.back_button.update(event)
            self.randomize_button.update(event)
            [button.update(event) for button in self.cell_buttons]

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == pygame.BUTTON_RIGHT
            ):
                grid_pos = self.maze.get_cell_index(*pygame.mouse.get_pos())
                if not self.maze.grid[grid_pos[1]][grid_pos[0]].collidable:
                    objective_pos = (
                        self.maze.get_cell_index(*self.maze.objective_position)
                        if self.maze.objective_position
                        else None
                    )
                    player_pos = (
                        self.maze.get_cell_index(*self.maze.player_start)
                        if self.maze.player_start
                        else None
                    )

                    if keys[pygame.K_LSHIFT] and grid_pos != player_pos:
                        self.maze.objective_position = self.maze.get_rect_position(grid_pos[1], grid_pos[0])
                        self.maze.objective_position_pos = grid_pos[1], grid_pos[0]
                    elif grid_pos != objective_pos:
                        self.maze.player_start = self.maze.get_rect_position(grid_pos[1], grid_pos[0])
                        self.maze.player_start_pos = grid_pos[1], grid_pos[0]
            if self.maze.player_start and self.maze.objective_position and self.confirm_button.callback is None:
                self.confirm_button.callback = lambda m=self.maze: self.add_maze()

    def add_maze(self):
        self.maze_manager.add_maze(self.maze)
        self.previous_screen.reload()
        self.manager.back(self.previous_screen)
