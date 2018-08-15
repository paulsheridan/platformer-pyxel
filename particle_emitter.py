import pyxel

from random import randint


class ParticleEmitter():
    def __init__(self, anchor):
        self.anchor = anchor
        self.spawn_area = 8, 12
        self.particles = []

    def update_position(self, delta):
        for particle in self.particles:
            particle['x'] -= delta[0] + particle['v']
            particle['y'] -= delta[1]

    def sparkle(self, v):
        if pyxel.frame_count % 2 == 0:
            self.particles.append({
                'zero_frame': pyxel.frame_count,
                'x': randint(self.anchor.x-2, self.anchor.x+self.spawn_area[0]),
                'y': randint(self.anchor.y-2, self.anchor.y+self.spawn_area[1]),
                'color': randint(8, 14),
                'v': v
            })

    def render_particles(self):
        for idx, particle in enumerate(self.particles):
            if pyxel.frame_count - particle['zero_frame'] >= 20:
                del self.particles[idx]
            else:
                pyxel.pix(particle['x'], particle['y'], particle['color'])
