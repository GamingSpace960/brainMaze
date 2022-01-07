import numpy as np
import pygame as pg
import World
from time import sleep,time


# chnageable
# speed, leadership, brainsizex, brainsizey

class Evolve():
    def __init__(self,bots,mutationRate):
        self.bots = bots
        self.sortFitness()
        self.topNum = 10

    def getFitnes(bot):
        return bot.score

    def sortFitness(self):
        self.bots.sort(key=self.getFitness)