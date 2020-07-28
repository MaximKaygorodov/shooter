import pygame
import sys
import random
from config import *
from entity import Entity
from satellite import Satellite, get_angle_btw_p1_and_p2
from bullet import Bullet
import math

pygame.init()
pg = pygame
dude = pg.image.load("dude.png")


def distance_btp(a, b):
    dist = math.hypot(math.fabs(a[0] - b[0]), math.fabs(a[1] - b[1]))
    return dist


def shot(cool_down):
    cool_down += 1
    if pg.mouse.get_pressed() == (1, 0, 0) and cool_down > RELOAD_SPEED:
        shot_angle = get_angle_btw_p1_and_p2(player.center, pg.mouse.get_pos())
        bullets.append(Bullet(players_satellite.pos, BULLET_SIZE, shot_angle))
        cool_down = 0
    return cool_down


def calc_around_player(rad):
    around_player = [player.center[0] + random.randint(-rad, rad), player.center[1] + random.randint(-rad, rad)]
    return around_player


def move_enemies(enemy_cd):
    enemy_cd += 1
    if enemy_cd > ENEMY_COOLDOWN:
        for enemy in enemies:
            around_player = calc_around_player(PLAYER_SIZE)
            angle = get_angle_btw_p1_and_p2(enemy.center, around_player)
            enemy.move_to_player(math.radians(angle), True)
        spawn_enemy()

        enemy_cd = 0
    for enemy in enemies:
        enemy.slow_down()
        enemy.make_turn()
        collide_entities()
        collide_with_boundaries(enemy)
    return enemy_cd


def spawn_enemy():
    away_form_player = 100
    spawn_pos = [random.randint(0, WIDTH - ENEMY_SIZE),
                 random.randint(0, HEIGHT - ENEMY_SIZE)]
    if spawn_pos[0] in range(player.pos_x - away_form_player, player.pos_x+player.size+away_form_player):
        if spawn_pos[1] in range(player.pos_y - away_form_player, player.pos_y+player.size+away_form_player):
            spawn_enemy()
    else:
        enemies.append(Entity(spawn_pos, ENEMY_SIZE))


def collide_entities():
    global game_over
    for enemy in enemies:
        if distance_btp(enemy.center, player.center) < 110:
            game_over = True
        for any_other_enemy in enemies:
            if any_other_enemy != enemy and distance_btp(enemy.center, any_other_enemy.center) < 60:
                 enemy.bounce_away_from(any_other_enemy)
        for any_bullet in bullets:
            if distance_btp(enemy.center, any_bullet.center) < BULLET_SPEED:
                enemies.remove(enemy)
                bullets.remove(any_bullet)
    return game_over


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
players_satellite = Satellite(SATELLITE_RADIUS)
bullets = []
enemies = []


def restart_menu():
    while True:
        # listening for keys
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    start_game()
                if event.key == pg.K_ESCAPE:
                    sys.exit()


# main loop
def start_game():
    global player, players_satellite,bullets, enemies, game_over
    player = Entity([200, 200], PLAYER_SIZE)
    players_satellite = Satellite(SATELLITE_RADIUS)
    bullets = []
    enemies = []
    game_over = False

    move_keys = [False, False, False, False]  # move [w, a, s, d]
    shot_cool_down_tracker = 0
    enemy_cool_down = 0
    while not game_over:
        # listening for keys
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    move_keys[0] = True
                if event.key == pg.K_a:
                    move_keys[1] = True
                if event.key == pg.K_s:
                    move_keys[2] = True
                if event.key == pg.K_d:
                    move_keys[3] = True
                if event.key == pg.K_e:
                    spawn_enemy()

            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    move_keys[0] = False
                if event.key == pg.K_a:
                    move_keys[1] = False
                if event.key == pg.K_s:
                    move_keys[2] = False
                if event.key == pg.K_d:
                    move_keys[3] = False

        # calculating
        player.calc_direction(move_keys)
        player.make_turn()  # Goes after all changes in speed
        enemy_cool_down = move_enemies(enemy_cool_down)
        collide_with_boundaries(player)  # Goes after all moves/turns that can collide
        for bullet in bullets:
            bullet.make_turn()
        players_satellite.make_turn(player.center, pg.mouse.get_pos())

        shot_cool_down_tracker = shot(shot_cool_down_tracker)

        screen.fill(GREEN)

        # rendering
        for enemy in enemies:
            pg.draw.rect(screen, enemy.color, enemy.rect)
        for bullet in bullets:
            pg.draw.rect(screen, RED, bullet.rect)
        pg.draw.circle(screen, RED, players_satellite.pos, 8)
        # pg.draw.rect(screen, RED, player.rect)
        screen.blit(dude, [player.pos_x, player.pos_y])

        # updating
        clock.tick(30)
        pg.display.update()
    restart_menu()


start_game()
