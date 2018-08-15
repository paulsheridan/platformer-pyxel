import os
import pyxel

from random import randint
from itertools import islice
from camera import Camera
from player import Player
from level import Level
from particle_emitter import ParticleEmitter


class App:
    def __init__(self):
        pyxel.init(240, 160, caption='test game')

        self.levelname = 'level1'
        self.assets_dir = 'assets'
        self.assets = os.path.realpath(
            os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                self.assets_dir,
                self.levelname
            )
        )

        pyxel.image(0).load(0, 0, os.path.join(self.assets, '../animation.png'))
        pyxel.image(1).load(0, 0, os.path.join(self.assets, 'tileset.png'))
        pyxel.image(2).load(0, 0, os.path.join(self.assets, 'background.png'))


        self.level = Level(self.assets, 'mapfile.txt', 16)
        self.camera = Camera(self.level)
        self.player = Player()
        self.sparkle_emitter = ParticleEmitter(self.player)

        self.test_val = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.player.run(-1)
        if pyxel.btn(pyxel.KEY_D):
            self.player.run(1)
        if pyxel.btn(pyxel.KEY_I):
            self.test_val += 1
        if pyxel.btn(pyxel.KEY_O):
            self.test_val -= 1
        if pyxel.btnp(pyxel.KEY_S, 60, 30):
            print(pyxel.frame_count)
            if self.player.grounded:
                self.player.charge()
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.player.grounded:
                self.player.jump()
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_T):
            pyxel.pal(1, 7)
        else:
            pyxel.pal()
        if pyxel.btn(pyxel.KEY_P):
            import pdb; pdb.set_trace()

        self.camera.last_offset_x, self.camera.last_offset_y = self.camera.offset_x, self.camera.offset_y
        self.update_player()

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(0, 0, 2, 0, 0, 240, 70, 1)
        # render the city
        for i in range(2):
            pyxel.blt(i * 240 - self.camera.offset_x/2, 39, 2, 0, 82, 240, 82, 1)
        # render the clouds
        for i in range(2):
            pyxel.blt(i * 240 - self.camera.offset_x/50, 10, 2, 0, 168, 240, 40, 1)
        self.level.render(self.camera, self.level.background, 1)
        self.level.render(self.camera, self.level.collision, 1)
        self.player.render()
        self.sparkle_emitter.render_particles()
        self.level.render(self.camera, self.level.foreground, 1)

    def update_player(self):
        self.player.x, self.camera.offset_x = update_axis(
            self.player.x,
            self.player.vx,
            self.camera.offset_x,
            self.camera.max_scroll_x,
            pyxel.width,
        )
        self.player.x_collision(self.camera, self.level)

        self.player.y, self.camera.offset_y = update_axis(
            self.player.y,
            self.player.vy,
            self.camera.offset_y,
            self.camera.max_scroll_y,
            pyxel.height,
        )
        self.player.y_collision(self.camera, self.level)

        self.sparkle_emitter.update_position(self.offset_delta())

        self.player.vy = min(self.player.vy + 1, 7)
        if self.player.vx > 0:
            self.player.vx = self.player.vx - 1
        elif self.player.vx < 0:
            self.player.vx = self.player.vx + 1

        if self.player.jump_chg >= 4:
            self.sparkle_emitter.sparkle(self.test_val)

    def offset_delta(self):
        return self.camera.offset_x - self.camera.last_offset_x, self.camera.offset_y - self.camera.last_offset_y


def update_axis(pos, vel, offset, max_scroll, viewport):
    if vel < 0:
        if offset < abs(vel):
            offset = 0
            pos += vel
        elif offset > 0 and pos < viewport // 2:
            offset += vel
        else:
            pos += vel
    elif vel > 0:
        if offset < max_scroll and pos > viewport // 2:
            offset += vel
        else:
            pos += vel
    return pos, offset


App()
