import pygame
import math
import random
from config import *
from bullet import Bullet

pg = pygame


def collide_entity_with_boundaries(ent):
    x = ent.pos_x
    y = ent.pos_y
    size = ent.size
    if x < 0:
        ent.set_pos(0, y)
        x = 0
    if x + size > WIDTH:
        ent.set_pos(WIDTH - size, y)
        x = WIDTH - size
    if y < 0:
        ent.set_pos(x, 0)
    if y + size > HEIGHT:
        ent.set_pos(x, HEIGHT - size)


def distance_btp(a, b):
    dist = math.hypot(math.fabs(a[0] - b[0]), math.fabs(a[1] - b[1]))
    return dist


def calc_around_object(obj, rad):
    around_player = [obj.center[0] + random.randint(-rad, rad), obj.center[1] + random.randint(-rad, rad)]
    return around_player


def check_if_coordinates_away_from_object(spawn_pos, obj, dist):
    if spawn_pos[0] in range(obj.pos_x - dist, obj.pos_x+obj.size+dist) and \
            spawn_pos[1] in range(obj.pos_y - dist, obj.pos_y+obj.size+dist):
        return True
    else:
        return False


def get_angle_btw_p1_and_p2(pt1, pt2):
    x_diff = pt2[0] - pt1[0]
    y_diff = pt2[1] - pt1[1]
    a = -math.degrees(math.atan2(y_diff, x_diff))
    # print("Angle btw: [" + str(p1) + "][" + str(p2) + "]: " + str(a))
    return a + 90


def shot(bullets, obj):
    if pg.mouse.get_pressed() == (1, 0, 0):
        shot_angle = get_angle_btw_p1_and_p2(obj.pos, pg.mouse.get_pos())
        bullets.append(Bullet(obj.pos, BULLET_SIZE, shot_angle))



