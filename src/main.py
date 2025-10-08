from app.game_app import GameApp


def main():
    snake_app = GameApp(fps=60, tps=10)
    snake_app.run()
    snake_app.destroy()


if __name__ == "__main__":
    main()
