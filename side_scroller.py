import os
import json
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
        self.assets = os.path.join(
            os.getcwd(),
            os.path.dirname(__file__),
            'assets',
        )

        pyxel.image(0).load(0, 0, os.path.join(self.assets, 'animation.png'))
        pyxel.image(1).load(0, 0, os.path.join(self.assets, self.levelname, 'tileset.png'))
        pyxel.image(2).load(0, 0, os.path.join(self.assets, self.levelname, 'background.png'))

        self.level = Level(os.path.join(self.assets, self.levelname), 'mapfile.txt', 16)
        self.camera = Camera(self.level)
        self.player = Player(self.assets)
        self.sparkle_emitter = ParticleEmitter(self.player)

        self.zero_frame = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.player.run(-1)
        if pyxel.btn(pyxel.KEY_D):
            self.player.run(1)
        if pyxel.btn(pyxel.KEY_W):
            if self.player.on_wall:
                self.player.climb(-1)
        if pyxel.btn(pyxel.KEY_S):
            if self.player.on_wall:
                self.player.climb(1)
        if pyxel.btnp(pyxel.KEY_L):
            self.player.attack()
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.player.on_wall:
                self.player.wall_jump()
            elif self.player.grounded:
                self.player.jump()
            elif self.player.double_primed:
                self.player.double_jump()
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

        self.camera.update_last_offset()
        self.update_player()

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(0, 0, 2, 0, 0, 240, 70, 1)
        # render the city
        # for i in range(2):
        #     pyxel.blt(i * 240 - self.camera.offset_x/2, 39, 2, 0, 82, 240, 82, 1)
        # render the clouds
        for i in range(2):
            pyxel.blt(i * 240 - self.camera.offset_x//50, 10 - self.camera.offset_y//50, 2, 0, 168, 240, 40, 1)
        self.level.render(self.camera, self.level.background, 1)
        self.level.render(self.camera, self.level.collision, 1)
        self.sparkle_emitter.render_particles()
        self.player.update_anim()
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

        self.player.update_gravity()
        self.sparkle_emitter.update_position(self.camera.offset_delta())
        self.sparkle_emitter.sparkle(0, 1, 12)

    # def respawn(self):
    #     self.zero_frame = pyxel.frame_count
    #     pyxel.cls()


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
