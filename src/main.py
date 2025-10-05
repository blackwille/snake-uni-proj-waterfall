import dearpygui.dearpygui as dpg
import time


def main():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.add_window(label="tutorial", width=500, height=500, tag="main_window")
    dpg.set_primary_window(window="main_window", value=True)
    
    while dpg.is_dearpygui_running():
        drawlist_size = (dpg.get_item_width("main_window") - 20, dpg.get_item_height("main_window") - 20)

        dpg.delete_item("drawlist")
        dpg.add_drawlist(width=drawlist_size[0], height=drawlist_size[1], tag="drawlist", parent="main_window")
        
        GRID_SIZE = 10
        SQUARE_SIZE = min(drawlist_size[0] // GRID_SIZE, drawlist_size[1] // GRID_SIZE)
        
        squares = [[((SQUARE_SIZE * i, SQUARE_SIZE * j), (SQUARE_SIZE + SQUARE_SIZE * i, SQUARE_SIZE + SQUARE_SIZE * j)) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                dpg.delete_item(f"square_{i}_{j}")
                dpg.draw_rectangle(squares[i][j][0], squares[i][j][1], tag=f"square_{i}_{j}", parent="drawlist", fill=(255, 0, 0))
        
        fps = 60
        frame_time = 1 / fps
        time.sleep(frame_time)
            
        dpg.render_dearpygui_frame()
        
    dpg.destroy_context()

if __name__ == "__main__":
    main()
