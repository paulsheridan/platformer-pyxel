import pyxel

from random import randint


class ParticleEmitter():
    def __init__(self, anchor):
        self.anchor = anchor
        self.spawn_area = 5, 5
        self.particles = []

    def update_position(self, delta):
        for particle in self.particles:
            particle['x'] -= delta[0] + particle['vx']
            particle['y'] -= delta[1] + particle['vy']

    def sparkle(self, vx, vy, color):
        if pyxel.frame_count % 2 == 0:
            self.particles.append({
                'zero_frame': pyxel.frame_count,
                'x': randint(self.anchor.x-2, self.anchor.x+self.spawn_area[0]),
                'y': randint(self.anchor.y-2, self.anchor.y+self.spawn_area[1]),
                'color': color,
                'vx': vx,
                'vy': vy,
            })

    def render_particles(self):
        for idx, particle in enumerate(self.particles):
            if pyxel.frame_count - particle['zero_frame'] >= 20:
                del self.particles[idx]
            else:
                pyxel.pset(particle['x'], particle['y'], particle['color'])
