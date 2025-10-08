from views.i_game_view import IGameView
from controllers.i_game_controller import IGameController
from data.game_state import GameState
from data.events import Event
from data.stages import Stage
from dearpygui import dearpygui as dpg
import os
import threading

LARGE_FONT_SIZE = 38
REGULAR_FONT_SIZE = 28
MINI_FONT_SIZE = 22
CELL_SIZE = 20


class GameView(IGameView):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is not None:
            raise RuntimeError("Only one GameView can be created")
        instance = super().__new__(cls)
        cls.__instance = instance
        return instance

    def __init__(self, lock: threading.Lock) -> None:
        super().__init__()
        self.__lock: threading.Lock = lock
        self.__current_state: GameState = GameState()
        self.__controller: IGameController | None = None

        dpg.create_context()

        self.__main_window_tag = "main_window"
        with dpg.window(
            tag=self.__main_window_tag,
        ):
            with dpg.font_registry():
                relative_font_path = "../../fonts/Roboto-Regular.ttf"
                font_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), relative_font_path)
                )
                large_font = dpg.add_font(font_path, LARGE_FONT_SIZE)
                regular_font = dpg.add_font(font_path, REGULAR_FONT_SIZE)
                mini_font = dpg.add_font(font_path, MINI_FONT_SIZE)
            dpg.bind_font(regular_font)

            self.__start_menu_label_tag = dpg.add_text(default_value="SNAKE GAME")
            dpg.bind_item_font(self.__start_menu_label_tag, large_font)

            self.__start_menu_button_start_tag = dpg.add_button(label="START")

            self.__game_score_label_tag = dpg.add_text(
                default_value=f"SCORE: {len(self.__current_state.snake)}"
            )
            dpg.bind_item_font(self.__game_score_label_tag, mini_font)

            self.__drawlist_container_tag = dpg.add_group()
            self.__drawlist_tag = dpg.add_drawlist(
                width=-1, height=-1, parent=self.__drawlist_container_tag
            )

            self.__fail_label_tag = dpg.add_text(default_value="GAME OVER")
            dpg.bind_item_font(self.__fail_label_tag, large_font)

            self.__fail_button_restart_tag = dpg.add_button(label="PLAY AGAIN")

        dpg.create_viewport(title="Snake Game")
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(window=self.__main_window_tag, value=True)

    def destroy(self) -> None:
        dpg.destroy_context()
        GameView.__instance = None

    def watch_events(self) -> None:
        if self.__controller is None:
            return

        event = Event.PASS
        if dpg.get_item_state(item=self.__start_menu_button_start_tag)["clicked"]:
            event = Event.TO_GAME
        if dpg.get_item_state(item=self.__fail_button_restart_tag)["clicked"]:
            event = Event.TO_START_MENU
        if dpg.is_key_pressed(dpg.mvKey_Spacebar):
            event = Event.PAUSE
        if dpg.is_key_down(dpg.mvKey_Up):
            event = Event.MOVE_UP
        if dpg.is_key_down(dpg.mvKey_Down):
            event = Event.MOVE_DOWN
        if dpg.is_key_down(dpg.mvKey_Left):
            event = Event.MOVE_LEFT
        if dpg.is_key_down(dpg.mvKey_Right):
            event = Event.MOVE_RIGHT

        self.__controller.handle_event(event)

    def set_controller(self, controller: IGameController) -> None:
        self.__controller = controller

    def show(self) -> bool:
        if not dpg.is_dearpygui_running():
            return False

        if self.__current_state.stage == Stage.START_MENU:
            self.__set_start_menu_page()
        if self.__current_state.stage == Stage.GAME:
            self.__set_game_page()
        if self.__current_state.stage == Stage.FAIL:
            self.__set_fail_page()

        with self.__lock:
            dpg.render_dearpygui_frame()

        return True

    def update(self, state: GameState) -> None:
        self.__current_state = state
        self.__update_game_page_by_state()

    def __set_start_menu_page(self) -> None:
        dpg.hide_item(self.__game_score_label_tag)
        dpg.hide_item(self.__drawlist_container_tag)
        dpg.hide_item(self.__fail_label_tag)
        dpg.hide_item(self.__fail_button_restart_tag)
        dpg.show_item(self.__start_menu_label_tag)
        dpg.show_item(self.__start_menu_button_start_tag)

        win_w = dpg.get_item_width(self.__main_window_tag)
        win_h = dpg.get_item_height(self.__main_window_tag)
        if win_w is None or win_h is None:
            return

        label = self.__start_menu_label_tag
        label_rect = dpg.get_item_rect_size(label)
        if label_rect is None:
            return
        dpg.configure_item(
            label, pos=(win_w // 2 - label_rect[0] // 2, win_h // 2 - label_rect[1])
        )

        PADDING = LARGE_FONT_SIZE // 2
        button = self.__start_menu_button_start_tag
        button_rect = dpg.get_item_rect_size(button)
        if button_rect is None:
            return
        dpg.configure_item(
            button, pos=(win_w // 2 - button_rect[0] // 2, win_h // 2 + PADDING)
        )

    def __set_game_page(self) -> None:
        dpg.hide_item(self.__start_menu_label_tag)
        dpg.hide_item(self.__start_menu_button_start_tag)
        dpg.hide_item(self.__fail_label_tag)
        dpg.hide_item(self.__fail_button_restart_tag)
        dpg.show_item(self.__game_score_label_tag)
        dpg.show_item(self.__drawlist_container_tag)

        win_w = dpg.get_item_width(self.__main_window_tag)
        win_h = dpg.get_item_height(self.__main_window_tag)
        if win_w is None or win_h is None:
            return

        game_score = self.__game_score_label_tag
        game_score_rect = dpg.get_item_rect_size(game_score)
        if game_score_rect is None:
            return
        dpg.configure_item(game_score, pos=(win_w // 2 - game_score_rect[0] // 2, 0))

        PADDING = MINI_FONT_SIZE // 4
        drawlist_container = self.__drawlist_container_tag
        drawlist_rect = dpg.get_item_rect_size(drawlist_container)
        if drawlist_rect is None:
            return
        drawlist_container_x = win_w // 2 - drawlist_rect[0] // 2
        drawlist_container_y = win_h // 2 - drawlist_rect[1] // 2
        if drawlist_container_y < game_score_rect[1] + PADDING:
            drawlist_container_y = game_score_rect[1] + PADDING
        dpg.configure_item(
            drawlist_container,
            pos=(
                drawlist_container_x,
                drawlist_container_y,
            ),
        )

    def __set_fail_page(self) -> None:
        dpg.hide_item(self.__start_menu_label_tag)
        dpg.hide_item(self.__start_menu_button_start_tag)
        dpg.hide_item(self.__drawlist_container_tag)
        dpg.show_item(self.__fail_label_tag)
        dpg.show_item(self.__fail_button_restart_tag)

        win_w = dpg.get_item_width(self.__main_window_tag)
        win_h = dpg.get_item_height(self.__main_window_tag)
        if win_w is None or win_h is None:
            return

        PADDING = LARGE_FONT_SIZE // 2
        label = self.__fail_label_tag
        label_rect = dpg.get_item_rect_size(label)
        if label_rect is None:
            return
        dpg.configure_item(
            label,
            pos=(win_w // 2 - label_rect[0] // 2, win_h // 2 - label_rect[1] - PADDING),
        )

        game_score = self.__game_score_label_tag
        game_score_rect = dpg.get_item_rect_size(game_score)
        if game_score_rect is None:
            return
        dpg.configure_item(
            game_score, pos=(win_w // 2 - game_score_rect[0] // 2, win_h // 2)
        )

        button = self.__fail_button_restart_tag
        button_rect = dpg.get_item_rect_size(button)
        if button_rect is None:
            return
        dpg.configure_item(
            button,
            pos=(
                win_w // 2 - button_rect[0] // 2,
                win_h // 2 + game_score_rect[1] + PADDING,
            ),
        )

    def __update_game_page_by_state(self) -> None:
        if self.__current_state.stage == Stage.FAIL:
            return

        dpg.configure_item(
            self.__game_score_label_tag,
            default_value=f"SCORE: {len(self.__current_state.snake)}",
        )

        drawlist_w = self.__current_state.map_size[0] * CELL_SIZE
        drawlist_h = self.__current_state.map_size[1] * CELL_SIZE
        dpg.configure_item(self.__drawlist_tag, width=drawlist_w, height=drawlist_h)
        for x in range(self.__current_state.map_size[0]):
            for y in range(self.__current_state.map_size[1]):
                if dpg.does_item_exist(f"map_cell_{x}_{y}"):
                    continue
                left_up_corner = (CELL_SIZE * x, CELL_SIZE * y)
                right_down_corner = (
                    CELL_SIZE + CELL_SIZE * x,
                    CELL_SIZE + CELL_SIZE * y,
                )
                dpg.draw_rectangle(
                    left_up_corner,
                    right_down_corner,
                    tag=f"map_cell_{x}_{y}",
                    parent=self.__drawlist_tag,
                    fill=(255, 255, 255),
                    color=(100, 100, 100),
                    thickness=1,
                )

        LAYER_SNAKE_W_APPLE_TAG = "draw_layer_snake_apple"
        dpg.delete_item(LAYER_SNAKE_W_APPLE_TAG)
        with dpg.draw_layer(tag=LAYER_SNAKE_W_APPLE_TAG, parent=self.__drawlist_tag):
            for coord in self.__current_state.snake:
                x = coord.x
                y = coord.y
                left_up_corner = (CELL_SIZE * x, CELL_SIZE * y)
                right_down_corner = (
                    CELL_SIZE + CELL_SIZE * x,
                    CELL_SIZE + CELL_SIZE * y,
                )
                dpg.draw_rectangle(
                    left_up_corner,
                    right_down_corner,
                    fill=(0, 0, 0),
                    color=(100, 100, 100),
                )
            x = self.__current_state.apple.x
            y = self.__current_state.apple.y
            left_up_corner = (CELL_SIZE * x, CELL_SIZE * y)
            right_down_corner = (
                CELL_SIZE + CELL_SIZE * x,
                CELL_SIZE + CELL_SIZE * y,
            )
            dpg.draw_rectangle(
                left_up_corner,
                right_down_corner,
                fill=(255, 0, 0),
                color=(100, 100, 100),
            )
