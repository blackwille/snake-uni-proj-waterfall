import dearpygui.dearpygui as dpg
import time


def main():
    dpg.create_context()

    with dpg.window(label="Snake Game", width=50, height=50, tag="main_window"):
        with dpg.drawlist(width=-1, height=-1, tag="drawlist"):
            dpg.draw_rectangle(pmin=(0, 0), pmax=(100, 100), color=(255, 0, 0, 255))

    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(window="main_window", value=True)
    
    squares = []
    while dpg.is_dearpygui_running():
        fps = 60
        frame_time = 1 / fps
        time.sleep(frame_time)
        dpg.render_dearpygui_frame()
        
        window_width = dpg.get_item_width("main_window")
        window_height = dpg.get_item_height("main_window")
        dpg.configure_item("drawlist", width=window_width, height=window_height)
        
        if window_width is None or window_height is None:
            continue
        
        SQUARE_SIZE = 50
        GRID_SIZE = min(window_width // SQUARE_SIZE, window_height // SQUARE_SIZE)

        for i in range(len(squares)):
            for j in range(len(squares[0])):
                dpg.delete_item(f"square_{i}_{j}")
        squares = [
            [
                (
                    (SQUARE_SIZE * i, SQUARE_SIZE * j),
                    (SQUARE_SIZE + SQUARE_SIZE * i, SQUARE_SIZE + SQUARE_SIZE * j),
                )
                for i in range(GRID_SIZE)
            ]
            for j in range(GRID_SIZE)
        ]
        for i in range(len(squares)):
            for j in range(len(squares[0])):
                dpg.draw_rectangle(
                    squares[i][j][0],
                    squares[i][j][1],
                    tag=f"square_{i}_{j}",
                    parent="drawlist",
                    fill=(255, 0, 0),
                )

    dpg.destroy_context()


if __name__ == "__main__":
    main()
