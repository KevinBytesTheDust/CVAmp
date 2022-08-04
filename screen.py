import logging

logger = logging.getLogger(__name__)


def get_screen_resolution(kind):

    try:
        import tkinter as tk

        root = tk.Tk()
    except Exception as e:
        logger.exception(e)
        return 500

    return_value = None

    if kind == "width":
        return_value = root.winfo_screenwidth()
    if kind == "height":
        return_value = root.winfo_screenheight()

    root.destroy()
    return return_value


class Screen:
    def __init__(self, window_width, window_height):
        self.window_width_offset = 100
        self.window_height_offset = 50

        self.window_width = window_width
        self.window_height = window_height

        self.screen_width = get_screen_resolution("width")
        self.screen_height = get_screen_resolution("height")

        self.spawn_locations = self.generate_spawn_locations()

    def generate_spawn_locations(self):
        spawn_locations = []

        cols = int(self.screen_width / (self.window_width - self.window_width_offset))
        rows = int(self.screen_height / (self.window_height - self.window_height_offset))

        index = 0
        for row in range(rows):
            for col in range(cols):
                spawn_locations.append(
                    {
                        "index": index,
                        "x": col * (self.window_width - self.window_width_offset),
                        "y": row * (self.window_height - self.window_height_offset),
                        "width": self.window_width,
                        "height": self.window_height,
                        "free": True,
                    }
                )

                index += 1

        return spawn_locations

    def get_free_screen_location(self):
        free_keys = [screen_info for screen_info in self.spawn_locations if screen_info["free"]]

        if not free_keys:
            return None

        lowest_location_info = free_keys[0]
        lowest_location_info["free"] = False

        return lowest_location_info

    def get_default_location(self):
        return self.spawn_locations[0]
