import math
from math_functions import *




class Satellite():
    def __init__(self, rad):
        self.rad = rad
        self.pos = [0, 0]

    def make_turn(self, base_point, mouse_pos):
        bp = base_point
        rad = self.rad
        a = math.radians(get_angle_btw_p1_and_p2(base_point, mouse_pos))
        sin_a = math.sin(a)
        cos_a = math.cos(a)
        self.pos[0] = int(bp[0] + rad*sin_a)
        self.pos[1] = int(bp[1] + rad*cos_a)
        # print("sat pos: " + str(pos) + str((sin_a, cos_a)))
