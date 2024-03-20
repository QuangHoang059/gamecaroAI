import pygame as pg
from gamecaro import Game1x1
from gamecaroAI import GameAI
from start import Option

pg.init()
pg.display.set_caption("Game Caro")
pg_icon = pg.image.load(".\img\cat-cupid-love-icon.png")
pg.display.set_icon(pg_icon)
fps = 60
fpsClock = pg.time.Clock()
width, height = 800, 700
screen = pg.display.set_mode((width, height), flags=pg.HIDDEN)
runing = True
event = None
star = Option()
star.Star()
if star.chedo != 0:
    screen = pg.display.set_mode((width, height), flags=pg.SHOWN)
    if star.chedo == 2:
        gamecaro = Game1x1(screen)
    else:
        gamecaro = GameAI(screen)
while runing:
    ismousedown = False
    fpsClock.tick(fps)
    screen.fill((253, 245, 230))

    for even in pg.event.get():
        event = even
        if even.type == pg.QUIT:
            runing = False
        if even.type == pg.MOUSEBUTTONDOWN:
            ismousedown = True
    gamecaro.update(event)
    pg.display.update()
