import pyxel

class Animation():
    def __init__(self, anchor, anim_width, default_frame, anim_ost_x, anim_ost_y):
        self.anchor = anchor
        self.anim_width = anim_width
        self.default_frame = default_frame
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.zero_frame = 0
        self.frame_x = 0
        self.frame_y = 0

    def single_frame(self, frame):
        pass

    def one_time(self, start, length):
        pass

    def loop(self, start, length):
        self.zero_frame = pyxel.frame_count
        frame_x = self.anim_width * (6 + ((pyxel.frame_count - self.zero_frame) // 4) % 6)

    def render(self):
        pyxel.blt(self.anchor.x-1, self.anchor.y-5, 0, frame_x, 16, -self.direction*self.width+(3*-self.direction), self.height+5, 1)
