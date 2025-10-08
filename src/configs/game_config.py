import json
import os


class GameConfig:
    __instance = None

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is not None:
            return cls.__instance
        instance = super().__new__(cls)
        cls.__instance = instance
        return instance

    def __init__(self):
        relative_config_path = "../../game_config.json"
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), relative_config_path)
        )
        config_file = open(config_path, "r")
        config_dict = json.load(config_file)
        config_file.close()

        self.cell_size: int = config_dict["cell_size"]
        self.map_size: tuple[int, int] = (
            config_dict["map_size"]["width"],
            config_dict["map_size"]["height"],
        )
        self.regular_font_size: int = config_dict["regular_font_size"]
        self.large_font_size: int = config_dict["large_font_size"]
        self.mini_font_size: int = config_dict["mini_font_size"]
        self.max_frames_per_second: int = config_dict["max_frames_per_second"]
        self.max_ticks_per_second: int = config_dict["max_ticks_per_second"]
