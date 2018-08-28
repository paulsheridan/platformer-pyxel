import pyxel

class AnimationManager():
    def __init__(self, anchor, default_width, offset_x=0, offset_y=0):
        self.anchor = anchor
        self.default_width = default_width
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.zero_frame = 0
        self.speed = 4
        self.key = {}

    def single_frame(self, frame):
        pass

    def one_time(self, start, length):
        pass

    def loop(self, start, length):
        self.zero_frame = pyxel.frame_count
        frame_x = self.anim_width * (6 + ((pyxel.frame_count - self.zero_frame) // 4) % 6)

    def render(self):
        pyxel.blt(self.anchor.x-1, self.anchor.y-5, 0, frame_x, 16, -self.direction*self.width+(3*-self.direction), self.height+5, 1)
