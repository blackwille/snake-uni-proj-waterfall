from app.snake_app import SnakeApp


def main():
    snake_app = SnakeApp(fps=60, tps=10)
    snake_app.run()
    snake_app.destroy()


if __name__ == "__main__":
    main()
