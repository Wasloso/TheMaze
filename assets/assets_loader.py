from pygame.image import load
from pygame.surface import Surface
import os


# I think it can be done better
class AssetsLoader:
    _dir = "assets"
    _backgroundDir = os.path.join(_dir, "backgrounds")
    _buttonDir = os.path.join(_dir, "buttons")
    _playerDir = os.path.join(_dir, "player")
    _mazeDir = os.path.join(_dir, "maze")
    _objectiveDir = os.path.join(_dir, "objective")

    paths = {
        "background": {
            "main_menu_screen": os.path.join(_backgroundDir, "main_menu_screen.png"),
            "play_screen": os.path.join(_backgroundDir, "play_screen.png"),
            "options_screen": os.path.join(_backgroundDir, "options_screen.png"),
            "game_screen": os.path.join(_backgroundDir, "game_screen.png"),
        },
        "button": {
            "play_button": os.path.join(_buttonDir, "play_button.png"),
            "play_button_hovered": os.path.join(_buttonDir, "play_button_hovered.png"),
            "settings_button": os.path.join(_buttonDir, "settings_button.png"),
            "settings_button_hovered": os.path.join(
                _buttonDir, "settings_button_hovered.png"
            ),
            "quit_button": os.path.join(_buttonDir, "quit_button.png"),
            "quit_button_hovered": os.path.join(_buttonDir, "quit_button_hovered.png"),
            "back_button": os.path.join(_buttonDir, "back_button.png"),
            "back_button_hovered": os.path.join(_buttonDir, "back_button_hovered.png"),
            "credits_button": os.path.join(_buttonDir, "credits_button.png"),
            "credits_button_hovered": os.path.join(
                _buttonDir, "credits_button_hovered.png"
            ),
        },
        "player": {
            "idle": os.path.join(_playerDir, "idle.png"),
            "walk_UP": os.path.join(_playerDir, "walk_UP.png"),
            "walk_DOWN": os.path.join(_playerDir, "walk_DOWN.png"),
            "walk_LEFT": os.path.join(_playerDir, "walk_LEFT.png"),
            "walk_RIGHT": os.path.join(_playerDir, "walk_RIGHT.png"),
        },
        "objective": {
            "objective": os.path.join(_objectiveDir, "objective.png"),
            "objective_reached": os.path.join(_objectiveDir, "objective_reached.png"),
        },
        "maze": {
            "wall": os.path.join(_mazeDir, "wall.png"),
            "floor": os.path.join(_mazeDir, "floor.png"),
        },
    }

    @staticmethod
    def get_image(category: str, name: str) -> Surface:
        try:
            path = AssetsLoader.paths[category][name]
            return load(path).convert_alpha()
        except KeyError:
            print(f"Image {name} not found in category {category}.")
            return load(os.path.join(AssetsLoader._dir, "missing.png"))
        except FileNotFoundError:
            print(f"File {path} not found.")
            return load(os.path.join(AssetsLoader._dir, "missing.png"))

    @classmethod
    def get_background(cls, name: str) -> Surface:
        return cls.get_image("background", name)

    @classmethod
    def get_button(cls, name: str, hovered: bool = False) -> Surface:
        name = name + "_hovered" if hovered else name
        return cls.get_image("button", name)

    @classmethod
    def get_player(cls, name: str) -> Surface:
        return cls.get_image("player", name)

    @classmethod
    def get_maze(cls, name: str) -> Surface:
        return cls.get_image("maze", name)

    @classmethod
    def get_objective(cls, reached: bool = False) -> Surface:
        name = "objective_reached" if reached else "objective"
        return cls.get_image("objective", name)

    @classmethod
    def get_cell(cls, name) -> Surface:
        return cls.get_image("maze", name)
