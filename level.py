import os
import pyxel

from random import randint
from itertools import islice


class Level():
    def __init__(self, asset_dir, map_file, tile_size):
        self.tile_size = tile_size
        self.map_file = os.path.join(asset_dir, map_file)

        self.collision = Tilemap(build_tilemap(self.map_file, 'layer 1'))
        self.foreground = Tilemap(build_tilemap(self.map_file, 'layer 2'), True)
        self.background = Tilemap(build_tilemap(self.map_file, 'layer 0'), True)

        self.map_width = len(self.collision.matrix[0])
        self.map_height = len(self.collision.matrix)

        self.climbable = [0, 1, 6, 7]

        # TODO: Create one more layer for spawns and checkpoints, then read those into memory and set
        # spawn and checkpoints for the player.

    def render(self, camera, tilemap, colkey):
        # render the tileset based on each Tilemap's matrix.
        base_x = camera.offset_x // self.tile_size
        mod_offset_x = camera.offset_x % self.tile_size
        base_y = camera.offset_y // self.tile_size
        mod_offset_y = camera.offset_y % self.tile_size
        for idy, arr in enumerate(tilemap.matrix[base_y:base_y+camera.height_in_tiles+1]):
            for idx, val in enumerate(arr[base_x:base_x+camera.width_in_tiles+1]):
                if val != -1:
                    x = idx * self.tile_size - mod_offset_x
                    y = idy * self.tile_size - mod_offset_y
                    sx = (val % self.tile_size) * self.tile_size
                    sy = (val // (256 // self.tile_size)) * self.tile_size
                    pyxel.blt(x, y, 1, sx, sy, self.tile_size, self.tile_size, colkey)


class Tilemap():
    def __init__(self, matrix, mutable=False):
        self.matrix = matrix
        self.mutable = mutable

    def update_tile(self, x, y, val):
        if self.mutable:
            self.matrix[x][y] = val


def build_tilemap(map_file, layer):
    matrix = []
    with open(map_file, 'r') as data:
        for line in data:
            if layer in line:
                break
        for line_after in data:
            if not line_after.strip():
                break
            else:
                matrix.append([int(x) for x in line_after.strip().rstrip(',').split(',')])
    return matrix
