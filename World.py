import pygame as pg

class World(object):
    def __init__(self):
        pg.init()
        win = pg.display.set_mode(size = (500,500))
        while True:
            pg.display.flip()
        

map = World()