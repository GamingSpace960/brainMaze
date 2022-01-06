import numpy as np
import pygame as pg
import World.py

class Blob():
    def __init__(self,count,map):
        pg.draw.circle(map,(10,10,250),(400,400),2)


        
map = World.World()
bob = Blob(1,map)