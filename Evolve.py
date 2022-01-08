import numpy as np
import pygame as pg
import World
from time import sleep,time


# chnageable
# speed, leadership, brainsizex, brainsizey

class Evolve():
    def __init__(self,bots,mutationRate):
        self.bots = bots
        self.population = len(bots)
        self.fitSize = 10
        self.mutationRate = mutationRate
        self.points = 360
        self.sortFitness()
        self.birth()
        self.mutate()
       

    def getFitness(self,bot):
        return bot.avgScore

    def sortFitness(self):
        self.bots.sort(key=self.getFitness)
        

    def birth(self):
        self.commonMind()
        i = 0
        self.saveNum = len(self.bots)
        while len(self.bots) < self.population:
            self.bots.append(self.bots[i].copy())

    def commonMind(self):
        megaMind = sum([bot.qtable for bot in self.bots])/self.population
        self.bots = self.bots[:self.fitSize]
        for i in range(self.fitSize):
            self.bots[i].color = (200,10,255)
            self.bots.append(self.bots[i].copy())
            self.bots[-1].qtable = megaMind
            for j in range(self.fitSize):
                if i != j:
                    self.bots.append(self.bots[i].copy())
                    self.bots[-1].qtable = (self.bots[i].qtable + self.bots[j].qtable) /2

    def mutate(self):
        for i, bot in enumerate(self.bots[self.saveNum:]):
            if np.random.random() < self.mutationRate:
                self.bots[i+self.saveNum].leadership += (np.random.randint(-2,2))
            if np.random.random() < self.mutationRate:
                num = (np.random.randint(-10,10))
                self.bots[i+self.saveNum].mindSizeX += num
                    
            if np.random.random() < self.mutationRate:
                num = (np.random.randint(-10,10))
                self.bots[i+self.saveNum].mindSizeY += num
            #self.mindFix(i)
            points = self.points
            points -= self.bots[i+self.saveNum].leadership + self.bots[i+self.saveNum].mindSizeX + self.bots[i+self.saveNum].mindSizeY
            if self.points > 3:
                self.bots[i+self.saveNum].speed = 4
            elif self.points < 1:
                self.bots[i+self.saveNum].speed = 0
            else:
                self.bots[i+self.saveNum].speed = points


    def mindFix(self,i):
        if len(bots[i+self.saveNum].qtable) > bots[i+self.saveNum].mindSizeX:
            bots[i+self.saveNum].qtable = bots[i+self.saveNum].qtable[:bots[i+self.saveNum].mindSizeX]
        if len(bots[i+self.saveNum].qtable[0]) > bots[i+self.saveNum].mindSizeY:
            for axis in range(bots[i+self.saveNum].mindSizeX):
                bots[i+self.saveNum].qtable[axis] = bots[i+self.saveNum].qtable[axis][:bots[i+self.saveNum].mindSizeY]

        if len(bots[i+self.saveNum].qtable) < bots[i+self.saveNum].mindSizeX:
            bots[i+self.saveNum].qtable = np.concatenate([bots[i+self.saveNum].qtable,np.random.rand(bots[i+self.saveNum].mindSizeX,len(bots[i+self.saveNum].qtable[0]),4)])
        if len(bots[i+self.saveNum].qtable[0]) < bots[i+self.saveNum].mindSizeY:
            bots[i+self.saveNum].qtable = np.concatenate([bots[i+self.fitSize].qtable,np.random.rand(bots[i+self.fitSize].mindSizeX,bots[i+self.fitSize].mindSizeY,4)],1)


        

        


