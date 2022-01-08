import numpy as np
import pygame as pg
import World
import BlobSolo
import Evolve
from time import sleep,time



world = World.World()
st = time()
bots = [BlobSolo.LeadBlob(world) for _ in range(1_000)]
print((time()-st))


epsilon = .5
epsilonDecay = .001
step = 0
game = 0
while True:
    game+=1
    while step < 1200 and False in [bot.dead for bot in bots]:
        if step == 1119:
            for i,bot in enumerate(bots):
                bots[i].dead = True
        if game%50 == 0:
                world.draw()
                for bot in bots:
                    bot.Action(epsilon,world)
                world.update()
        else:
            for bot in bots:
                bot.Action(epsilon)
        step+= 1
    

    for bot in bots:
        bot.reset()
    print(game,epsilon,max([bot.avgScore for bot in bots]),step)  
    if game%10 == 0:
        [bot.colorReset() for bot in bots]
        bots = Evolve.Evolve(bots,.1).bots
        [bot.scoreReset() for bot in bots]
    epsilon -= epsilon*epsilonDecay
    if epsilon < .0001:
        epsilon = .5
    step = 0