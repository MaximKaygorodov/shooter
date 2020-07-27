import pygame as pg

WIDTH = 1200
HEIGHT = 800
MAX_SPEED = 40
BULLET_SPEED = 100
BULLET_SIZE = 8
RELOAD_SPEED = 2
PLAYER_SIZE = 120

GREEN = (136, 223, 88)
RED = (200, 70, 70)

screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()