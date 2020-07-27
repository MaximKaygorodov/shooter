from config import *
import math

class Bullet:
    def __init__(self, pos, size, angle):
        self.center = pos
        self.x = pos[0] - size//2
        self.y = pos[1] - size // 2
        self.size = size
        self.speed = BULLET_SPEED
        self.angle = angle
        self.rect = [self.x, self.y, self.size, self.size]

    def make_turn(self):
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        self.x += int(self.speed * sin_a)
        self.y += int(self.speed * cos_a)
        self.update_pos()

    def update_pos(self):
        self.rect = [self.x, self.y, self.size, self.size]
        self.center = [self.x + self.size//2, self.y + self.size//2]
