import pyxel

class Player():
    def __init__(self):
        self.height = 11
        self.width = 8

        self.x = 72
        self.y = 60
        self.vx = 0
        self.vy = 0

        self.grounded = False
        self.double_primed = True
        self.wall_climb = False
        self.direction = 1
        self.charge = 0

        self.anim_w = 11
        self.anim_zero_frame = 0

    def charge_up(self):
        self.charge = min(self.charge + 1, 200)

    def jump(self):
        self.vy = -8
        self.grounded = False
        self.double_primed = True

    def double_jump(self):
        self.vy = -8
        self.double_primed = False

    def run(self, direction):
        self.direction = direction
        if not self.wall_climb:
            self.vx = 2 * direction

    def climb(self, direction):
        if self.wall_climb:
            self.vy = 2 * direction

    def set_coll_defaults(self, camera):
        # player coordinates are base 0, so the distance right and down from the 0th element
        # of the player sprite has to be decremented by 1
        top = self.y + camera.offset_y
        bottom = self.y + camera.offset_y + self.height - 1
        right = self.x + camera.offset_x + self.width - 1
        left = self.x + camera.offset_x
        return top, bottom, right, left

    def x_collision(self, camera, level):
        top, bottom, right, left = self.set_coll_defaults(camera)

        if self.vx < 0:
            for coord in [left, top], [left, bottom]:
                tile = [
                    (coord[0] + self.vx) // level.tile_size,
                    coord[1] // level.tile_size
                ]
                if level.collision.matrix[tile[1]][tile[0]] != -1:
                    self.x = (tile[0]
                              * level.tile_size
                              + level.tile_size
                              - camera.offset_x)
                    self.check_climbable(tile, level)
                else:
                    self.wall_climb = False
                    break

        elif self.vx > 0:
            for coord in [right, top], [right, bottom]:
                tile = [
                    (coord[0] + self.vx) // level.tile_size,
                    coord[1] // level.tile_size
                ]
                if level.collision.matrix[tile[1]][tile[0]] != -1:
                    self.x = (tile[0]
                              * level.tile_size
                              - self.width
                              - camera.offset_x)
                    self.check_climbable(tile, level)
                else:
                    self.wall_climb = False
                    break

    def check_climbable(self, tile, level):
        self.wall_climb = level.collision.matrix[tile[1]][tile[0]] in level.climbable

    def y_collision(self, camera, level):
        top, bottom, right, left = self.set_coll_defaults(camera)

        if self.y >= 0 and self.vy > 0:
            for coord in [left, bottom], [right, bottom]:
                tile = [
                    coord[0] // level.tile_size,
                    (coord[1] + self.vy) // level.tile_size
                ]
                if level.collision.matrix[tile[1]][tile[0]] != -1:
                    self.vy = 0
                    self.y = (tile[1]
                              * level.tile_size
                              - self.height
                              - camera.offset_y)
                    self.grounded = True
                    self.wall_climb = False
                    self.double_primed = True
                    break
                else:
                    self.grounded = False

        elif self.y >= 0 and self.vy < 0:
            for coord in [left, top], [right, top]:
                tile = [
                    coord[0] // level.tile_size,
                    (coord[1] + self.vy) // level.tile_size
                ]
                if level.collision.matrix[tile[1]][tile[0]] != -1:
                    self.vy = 0
                    self.y = (tile[1]
                              * level.tile_size
                              + level.tile_size
                              - camera.offset_y)
                    break

    def update_gravity(self):
        if not self.wall_climb:
            self.vy = min(self.vy + 1, 7)
        else:
            self.vy = 0
        if self.vx > 0:
            self.vx = self.vx - 1
        elif self.vx < 0:
            self.vx = self.vx + 1

    def render(self):
        frame_x = self.anim_w * 7
        if not self.grounded:
            if not self.wall_climb:
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
            else:
                if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
                    self.anim_zero_frame = pyxel.frame_count
                frame_x = self.anim_w * (6 + ((pyxel.frame_count - self.anim_zero_frame) // 4) % 6)

        # TODO: make the rendering offset between player collision box
        # and the image blt dynamic based on frame size and hit box size
        pyxel.blt(self.x-1, self.y-5, 0, frame_x, 16, -self.direction*self.width+(3*-self.direction), self.height+5, 1)
