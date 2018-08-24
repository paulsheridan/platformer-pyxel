import pyxel

class Camera():
    def __init__(self, level):
        self.offset_x = 0
        self.offset_y = 0
        self.last_offset_x = 0
        self.last_offset_y = 0
        self.max_scroll_x = level.map_width * level.tile_size - pyxel.width
        self.max_scroll_y = level.map_height * level.tile_size - pyxel.height

        self.height_in_tiles = pyxel.height // level.tile_size
        self.width_in_tiles = pyxel.width // level.tile_size

    def update_last_offset(self):
        self.last_offset_x, self.last_offset_y = self.offset_x, self.offset_y

    def offset_delta(self):
        return (self.offset_x - self.last_offset_x), (self.offset_y - self.last_offset_y)
