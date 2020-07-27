import pygame
import sys
import random
from config import *
from entity import Entity
from satellite import Satellite, get_angle_btw_player_and_cursor
from bullet import Bullet
import math

pygame.init()
pg = pygame
dude = pg.image.load("dude.png")


def shoot(cool_down):
    cool_down += 1
    if pg.mouse.get_pressed() == (1, 0, 0) and cool_down > RELOAD_SPEED:
        bullets.append(Bullet(pl_satellite.pos, BULLET_SIZE, get_angle_btw_player_and_cursor(player.center)))
        cool_down = 0
    return cool_down

def collide_with_boundaries(ent):
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


player = Entity([200, 200], PLAYER_SIZE)
radius = 50
pl_satellite = Satellite(radius)
bullets = []
move_player = [False, False, False, False]    # move [w, a, s, d]
cool_down_tracker = 0

# main loop
while True:
    # listening for keys
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                move_player[0] = True
            if event.key == pg.K_a:
                move_player[1] = True
            if event.key == pg.K_s:
                move_player[2] = True
            if event.key == pg.K_d:
                move_player[3] = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                move_player[0] = False
            if event.key == pg.K_a:
                move_player[1] = False
            if event.key == pg.K_s:
                move_player[2] = False
            if event.key == pg.K_d:
                move_player[3] = False

    # calculating
    player.add_speed(20, move_player)
    player.make_turn()                  # Goes after all changes in speed
    collide_with_boundaries(player)     # Goes after all moves/turns that can collide
    for bullet in bullets:
        bullet.make_turn()
    satellite_pos = pl_satellite.make_turn(player.center)

    cool_down_tracker = shoot(cool_down_tracker)

    screen.fill(GREEN)

    # rendering

    for bullet in bullets:
        pg.draw.rect(screen, RED, bullet.rect)
    pg.draw.circle(screen, RED, satellite_pos, 8)
    # pg.draw.rect(screen, RED, player.rect)
    screen.blit(dude, [player.pos_x, player.pos_y])

    # updating
    clock.tick(30)
    pg.display.update()
