from config import *
import math


class Entity():
    def __init__(self, pos, size):
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.size = size
        self.speed_x = 0
        self.speed_y = 0
        self.rect = self.center = []
        self.update_pos()

    def update_pos(self):
        self.rect = [self.pos_x, self.pos_y, self.size, self.size]
        self.center = [self.pos_x + self.size//2, self.pos_y + self.size//2]

    def make_turn(self):
        if abs(self.speed_y) > MAX_SPEED:
            self.speed_y = MAX_SPEED
        if abs(self.speed_x) > MAX_SPEED:
            self.speed_x = MAX_SPEED
        self.pos_x += int(self.speed_x)
        self.pos_y += int(self.speed_y)
        self.update_pos()

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def bounce_up(self):
        self.speed_y *= -2

    def bounce_side(self):
        self.speed_x *= -2

    def slow_down(self):
        self.speed_y *= 0.9
        self.speed_x *= 0.9

    def move_to_player(self, angle, is_move):
        if is_move:
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)
            # self.pos_x += int(10 * sin_a)
            # self.pos_y += int(10 * cos_a)
            self.speed_x = int(30 * sin_a)
            self.speed_y = int(30 * cos_a)
            self.update_pos()
        # else:
        #     self.speed_x *= 0.3
        #     self.speed_y *= 0.3

    def calc_direction(self, move):
        speed = 20
        acceleration = 5
        deceleration = 5
        if move[0]:
            if self.speed_y > -speed:
                self.speed_y -= acceleration
        elif self.speed_y < 0:
            self.speed_y += deceleration

        if move[1]:
            if self.speed_x > -speed:
                self.speed_x -= acceleration
        elif self.speed_x < 0:
            self.speed_x += deceleration

        if move[2]:
            if self.speed_y < speed:
                self.speed_y += acceleration
        elif self.speed_y > 0:
            self.speed_y -= deceleration

        if move[3]:
            if self.speed_x < speed:
                self.speed_x += acceleration
        elif self.speed_x > 0:
            self.speed_x -= deceleration
