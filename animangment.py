import pygame

pg = pygame

def import_images(start, end):
    animation = []
    for i in range(start, end):
        if 0 < i <= 18:
            animation.append(pg.image.load("running_player" + str(i) + ".png"))
    return animation


def draw_animation(screen, animation, index, cool_down):
    cool_down += 1
    if index in range(len(animation)):
        screen.blit(animation[index], [0, 0])

    if cool_down == 4:
        index += 1
        cool_down = 0
    if index == 10:
        index = 0
    return index, cool_down