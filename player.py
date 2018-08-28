import os
import random
import math
import json
import pyxel

from animation import AnimationManager

class Player():
    def __init__(self, assets_path):
        self.height = 11
        self.width = 8

        self.x = 72
        self.y = 60
        self.vx = 0
        self.vy = 0

        self.speed = 3

        self.attack_zero_frame = 0
        self.attack_frame_count = 6
        self.attacking = False

        self.grounded = False
        self.double_primed = True

        self.on_wall = False
        self.can_climb = []

        self.direction = 1
        self.charge = 0

        self.anim_w = 11
        self.anim_zero_frame = 0

        self.anim_mgr = AnimationManager(self, 11, -1, -5)

        with open(os.path.join(assets_path, 'animation_key.json')) as data:
            self.anim_mgr.key = json.load(data)

    def charge_up(self):
        self.charge = min(self.charge + 1, 200)

    def jump(self):
        self.vy = -8
        self.grounded = False
        self.double_primed = True

    def double_jump(self):
        self.vy = -8
        self.double_primed = False

    def wall_jump(self):
        self.vy = -8
        self.vx = -4 * self.direction
        self.double_primed = True
        self.on_wall = False

    def run(self, direction):
        if not self.on_wall:
            self.direction = direction
            self.vx = self.speed * direction

    def climb(self, direction):
        if self.on_wall:
            self.vy = self.speed * direction

    def attack(self):
        self.attacking = True
        self.attack_zero_frame = pyxel.frame_count
        if self.on_wall:
            self.on_wall = False
            self.vx = -1 * self.direction

    def set_coll_defaults(self, camera):
        # player coordinates are base 0, so the distance right and down from the 0th element
        # of the player sprite has to be decremented by 1
        top = self.y + camera.offset_y
        bottom = self.y + camera.offset_y + self.height - 1
        right = self.x + camera.offset_x + self.width - 1
        left = self.x + camera.offset_x
        return top, bottom, right, left

    def x_collision(self, camera, level):
        self.can_climb = [False, False]
        top, bottom, right, left = self.set_coll_defaults(camera)

        if self.vx < 0:
            for idx, coord in enumerate([[left, top], [left, bottom]]):
                left = get_tile_x(coord[0], coord[1], self.vx, level.tile_size)
                if level.collision.matrix[left[1]][left[0]] != -1:
                    self.x = left[0] * level.tile_size + level.tile_size - camera.offset_x
                self.can_climb[idx] = check_climbable(left, level)

        elif self.vx > 0:
            for idx, coord in enumerate([[right, top], [right, bottom]]):
                right = get_tile_x(coord[0], coord[1], self.vx, level.tile_size)
                if level.collision.matrix[right[1]][right[0]] != -1:
                    self.x = right[0] * level.tile_size - self.width - camera.offset_x
                self.can_climb[idx] = check_climbable(right, level)

    def y_collision(self, camera, level):
        top, bottom, right, left = self.set_coll_defaults(camera)

        if self.y >= 0 and self.vy > 0:
            for coord in [left, bottom], [right, bottom]:
                floor = get_tile_y(coord[0], coord[1], self.vy, level.tile_size)
                if level.collision.matrix[floor[1]][floor[0]] != -1:
                    self.vy = 0
                    self.y = floor[1] * level.tile_size - self.height - camera.offset_y
                    self.grounded = True
                    self.on_wall = False
                    self.double_primed = True
                    break
                else:
                    self.grounded = False
            # if self.on_wall and not self.can_climb[1]:
            #     self.vy = 0
            #     self.y = floor[1] * level.tile_size - self.height - camera.offset_y - 2
            #     self.can_climb[1] = True

        elif self.y >= 0 and self.vy < 0:
            for coord in [left, top], [right, top]:
                ceiling = get_tile_y(coord[0], coord[1], self.vy, level.tile_size)
                if level.collision.matrix[ceiling[1]][ceiling[0]] != -1:
                    self.vy = 0
                    self.y = ceiling[1] * level.tile_size + level.tile_size - camera.offset_y
                    break
            # if self.on_wall and not self.can_climb[0]:
            #     self.vy = 0
            #     self.y = ceiling[1] * level.tile_size + level.tile_size - camera.offset_y - 2
                self.can_climb[0] = True
                # TODO: Troubleshoot weird shaking error when climbing against a non-climbable wall and on_wall becoming false after second time.

    def update_gravity(self):
        self.on_wall = bool(all(self.can_climb) and not self.grounded)
        if self.on_wall:
            if self.vy > 0:
                self.vy = self.vy - 1
            elif self.vy < 0:
                self.vy = self.vy + 1
        else:
            self.vy = min(self.vy + 1, 7)
            if self.vx > 0:
                self.vx = self.vx - 1
            elif self.vx < 0:
                self.vx = self.vx + 1

    def update_anim(self):
        frame_x = self.anim_w * 7
        if not self.grounded:
            if not self.on_wall:
                if self.vy >= 0:
                    frame_x = self.anim_w * 13
                else:
                    frame_x = self.anim_w * 12
            else:
                if self.vy > 0:
                    # climb up animation
                    pass
                elif self.vy < 0:
                    # climb down animation
                    pass
                else:
                    # not climbing, but on wall animation
                    pass
        else:
            if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_D):
                if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_D):
                    self.anim_zero_frame = pyxel.frame_count
                frame_x = self.anim_w * (((pyxel.frame_count - self.anim_zero_frame) // 4) % 6)
                # TODO: set running and idle frame counts and use those instead of just ints.
            else:
                if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
                    self.anim_zero_frame = pyxel.frame_count
                frame_x = self.anim_w * (6 + ((pyxel.frame_count - self.anim_zero_frame) // 4) % 6)

        # TODO: make the rendering offset between player collision box
        # and the image blt dynamic based on frame size and hit box size
        pyxel.blt(self.x-1, self.y-5, 0, frame_x, 16, -self.direction*self.width+(3*-self.direction), self.height+5, 1)

        if self.attacking:
            if pyxel.btnp(pyxel.KEY_L):
                self.attack_zero_frame = pyxel.frame_count
            else:
                if pyxel.frame_count < self.attack_zero_frame + self.attack_frame_count:
                    frame_x = self.anim_w * (17 + (pyxel.frame_count - self.attack_zero_frame) // 2)
                    pyxel.blt(self.x+self.direction*4, self.y-5, 0, frame_x, 16, -self.direction*self.width+(3*-self.direction), self.height+5, 1)
                else:
                    self.attacking = False


def get_tile_x(x, y, vx, tile_size):
    return [
        (x + vx) // tile_size,
        y // tile_size
    ]

def get_tile_y(x, y, vy, tile_size):
    return [
        x // tile_size,
        (y + vy) // tile_size
    ]

def check_climbable(tile, level):
    return level.collision.matrix[tile[1]][tile[0]] in level.climbable_tiles
