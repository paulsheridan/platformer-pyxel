# import pyxel
#
# class Animation():
#     def __init__(self, anchor, anim_width, default_frame, anim_ost_x, anim_ost_y):
#         self.anchor = anchor
#         self.anim_width = anim_width
#         self.default_frame = default_frame
#         self.anim_ost_x = anim_ost_y
#         self.anim_ost_y = anim_ost_y
#         self.zero_frame = 0
#
#     def single_frame(self, frame):
#         pass
#
#     def anim_one_time(self, start, length):
#         pass
#
#     def anim_loop(self, start, length):
#         self.zero_frame = pyxel.frame_count
#         frame_x = self.anim_width * (6 + ((pyxel.frame_count - self.zero_frame) // 4) % 6)
#
#     def render_anim(self):
#         pyxel.blt(self.x-1, self.y-5, 0, frame_x, 16, -self.direction*self.width+(3*-self.direction), self.height+5, 1)
