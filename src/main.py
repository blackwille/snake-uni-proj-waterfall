from app.game_app import GameApp
from configs.game_config import GameConfig


def main():
    game_config = GameConfig()

    snake_app = GameApp(
        fps=game_config.max_frames_per_second, tps=game_config.max_ticks_per_second
    )
    snake_app.run()
    snake_app.destroy()


if __name__ == "__main__":
    main()
