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
#epsilonDecay = .01
step = 0
game = 0
st = time()
while True:
    game+=1
    while step < 1200 and False in [bot.dead for bot in bots]:
        if step == 1119:
            for i,bot in enumerate(bots):
                bots[i].dead = True
        if game%100 == 0:
                world.draw()
                pg.draw.rect(world.win ,(200,200,200),(370,310,80,60))
                pg.draw.rect(world.win ,(200,200,10),((bestBrainX-244)*-2,(bestBrainY-184)*-2,490-(bestBrainX-244)*-2,10))
                pg.draw.rect(world.win ,(200,200,10),((bestBrainX-244)*-2,(bestBrainY-184)*-2,10,370-(bestBrainY-184)*-2))
                for bot in bots:
                    bot.Action(epsilon,world)
                world.update()
        else:
            for bot in bots:
                bot.Action(epsilon)
        step+= 1
    
    bestScore = -99999999999
    for bot in bots:
        tempTime = bot.time
        bot.reset()
        if bot.avgScore > bestScore:
            bestScore = bot.avgScore
            bestTime = tempTime
            bestBrainX = bot.mindSizeX
            bestBrainY = bot.mindSizeY
            bestleadership = bot.leadership
            bestSpeed = bot.speed

    print(game,step,epsilon,bestTime,bestBrainX,bestBrainY,bestleadership,bestSpeed,bestScore)  
    if game%10 == 0:
        [bot.colorReset() for bot in bots]
        bots = Evolve.Evolve(bots,.1).bots
        [bot.scoreReset() for bot in bots]
    epsilon = 10/game
    #epsilon -= epsilon*epsilonDecay
    #if epsilon < .0001:
    #    epsilon = .5
    step = 0