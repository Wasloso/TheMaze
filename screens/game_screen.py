from pygame import Rect
from pygame.surface import Surface

from maze import Maze, Direction, Objective, Cell, Player, Solver
from screens.screen_base import *
from ui_components import Button
from assets.assets_loader import AssetsLoader


class GameScreen(ScreenBase):
    def __init__(
        self,
        previous_screen: Optional[ScreenBase],
        manager,  # FIXME: add type hint here (now gives an Importerror)
        maze: Maze,
        ai: bool = False,
    ) -> None:
        super().__init__(previous_screen, manager, GAME)
        self.maze: Maze = maze
        self.ai: bool = ai
        self.maze.reset_visibility()

        self.player: Player = Player(
            start_position=self.maze.player_start,
            velocity=2,
            size=self.maze.cell_size // 3,
            image=AssetsLoader.get_player("idle" if not ai else "idle_ai"),
        )
        self.objective: Objective = Objective(
            position=self.maze.objective_position, size=self.maze.cell_size // 2
        )
        self.back_button: Button = Button.go_back_button(
            position=(25, 25),
            desired_size=(50, 50),
            callback=lambda: self.manager.back(previous_screen),
        )
        self.cells: list[Cell] = [cell for row in self.maze.grid for cell in row]
        self.collidable_cells: list[Cell] = [
            cell.rect for cell in self.cells if cell.collidable
        ]
        self.wallImage: Surface = pygame.transform.scale(
            AssetsLoader.get_cell("wall"), (self.maze.cell_size, self.maze.cell_size)
        )
        self.floorImage: Surface = pygame.transform.scale(
            AssetsLoader.get_cell("floor"), (self.maze.cell_size, self.maze.cell_size)
        )
        if self.ai:
            self.solver = Solver(self.maze, self.player)

        self.visibility_scale: int = 5
        self.fog_overlay = pygame.Surface((self.maze.cell_size, self.maze.cell_size))
        self.fog_overlay.fill((0, 0, 0))
        self.fog_overlay.set_alpha(128)

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        visibility_rect = self.player.rect.inflate(
            self.player.rect.width * self.visibility_scale,
            self.player.rect.height * self.visibility_scale,
        )

        for cell in self.cells:
            if cell.visited or visibility_rect.colliderect(cell.rect):
                cell.visited = True
                # cell.visited = False
                surface.blit(
                    self.wallImage if cell.collidable else self.floorImage,
                    cell.rect.topleft,
                )
            else:
                surface.blit(self.wallImage, cell.rect.topleft)
                surface.blit(self.fog_overlay, cell.rect.topleft)
        self.player.draw(surface)
        if visibility_rect.colliderect(self.objective.rect):
            self.objective.draw(surface)

        self.back_button.draw(surface)

    def update(self, events: list, keys: list) -> None:
        if self.ai and self.solver:
            self.solver.update()
        else:
            self.handle_buttons_click(keys)

        for event in events:
            self.back_button.update(event)

        self.player.update(events, keys)

        if self.objective.check_collision(self.player.rect):
            # TODO: Implement win screen
            pass

    def handle_buttons_click(self, keys) -> None:
        multiplier: int = 2 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move_player(Direction.UP, multiplier)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move_player(Direction.DOWN, multiplier)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_player(Direction.LEFT, multiplier)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_player(Direction.RIGHT, multiplier)

    def move_player(self, direction, multiplier=1) -> None:
        new_rect: Rect = self.player.try_move(direction, multiplier)
        if new_rect.collidelist(self.collidable_cells) == -1:
            self.player.rect = new_rect
