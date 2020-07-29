import pygame
import sys
import random
from config import *
from entity import Entity
from satellite import Satellite
from math_functions import *

pygame.init()
pg = pygame
dude = pg.image.load("dude.png")


def enemies_make_turn(pl, enemies):
    for enemy in enemies:
        around_player = calc_around_object(pl, PLAYER_SIZE)
        angle = get_angle_btw_p1_and_p2(enemy.center, around_player)
        enemy.move_in_direction(math.radians(angle), True)
    spawn_enemy(enemies, pl)


def spawn_enemy(enemies, player):
    spawn_pos = [random.randint(0, WIDTH - ENEMY_SIZE),
                 random.randint(0, HEIGHT - ENEMY_SIZE)]
    if check_if_coordinates_away_from_object(spawn_pos, player, 100):
        spawn_enemy(enemies, player)
    else:
        enemies.append(Entity(spawn_pos, ENEMY_SIZE))


def collide_entities(bullets, enemies, player):
    game_over = False
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


# player = Entity([200, 200], PLAYER_SIZE)
# players_satellite = Satellite(SATELLITE_RADIUS)
# bullets = []
# enemies = []


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
    player = Entity([200, 200], PLAYER_SIZE)
    players_satellite = Satellite(SATELLITE_RADIUS)
    bullets = []
    enemies = []
    game_over = False

    move_keys = [False, False, False, False]  # move [w, a, s, d]
    shot_cool_down = 0
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
                    spawn_enemy(enemies, player)

            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    move_keys[0] = False
                if event.key == pg.K_a:
                    move_keys[1] = False
                if event.key == pg.K_s:
                    move_keys[2] = False
                if event.key == pg.K_d:
                    move_keys[3] = False

        # moving player
        player.calc_direction(move_keys)
        player.make_turn()  # Goes after all changes in speed

        # making enemies move to player
        if enemy_cool_down == ENEMY_COOLDOWN:
            enemies_make_turn(player, enemies)
            enemy_cool_down = 0
        else:
            enemy_cool_down += 1

        # moving enemies
        for enemy in enemies:
            enemy.slow_down()
            enemy.make_turn()
            collide_entity_with_boundaries(enemy)
        game_over = collide_entities(bullets, enemies, player)

        collide_entity_with_boundaries(player)  # Goes after all moves/turns that can collide

        # move existing bullets
        for bullet in bullets:
            bullet.make_turn()
        players_satellite.make_turn(player.center, pg.mouse.get_pos())

        # created new bullet
        if shot_cool_down == RELOAD_SPEED:
            shot(bullets, players_satellite)
            shot_cool_down = 0
        else:
            shot_cool_down += 1


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
