from config import *


class Entity():
    def __init__(self, pos, size):
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.size = size
        self.speed_x = 0
        self.speed_y = 0
        self.rect = [pos[0], pos[1], size, size]
        self.center = [pos[0] + size//2, pos[1] + size//2]

    def make_turn(self):
        if abs(self.speed_y) > MAX_SPEED:
            self.speed_y = MAX_SPEED
        if abs(self.speed_x) > MAX_SPEED:
            self.speed_x = MAX_SPEED
        self.pos_x += int(self.speed_x)
        self.pos_y += int(self.speed_y)
        self.rect = [self.pos_x, self.pos_y, self.size, self.size]
        self.center = [self.pos_x + self.size//2, self.pos_y + self.size//2]

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def bounce_up(self):
        self.speed_y *= -2

    def bounce_side(self):
        self.speed_x *= -2

    def add_speed(self, value, move):
        acceleration = 5
        deceleration = 5
        if move[0]:
            if self.speed_y > -value:
                self.speed_y -= acceleration
        elif self.speed_y < 0:
            self.speed_y += deceleration

        if move[1]:
            if self.speed_x > -value:
                self.speed_x -= acceleration
        elif self.speed_x < 0:
            self.speed_x += deceleration

        if move[2]:
            if self.speed_y < value:
                self.speed_y += acceleration
        elif self.speed_y > 0:
            self.speed_y -= deceleration

        if move[3]:
            if self.speed_x < value:
                self.speed_x += acceleration
        elif self.speed_x > 0:
            self.speed_x -= deceleration
