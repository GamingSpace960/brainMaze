import numpy as np
import pygame as pg
import World
import BlobSolo
import Evolve
import Follower
from time import sleep,time



world = World.World()
st = time()
bots = [BlobSolo.LeadBlob(world) for _ in range(1_000)]
followers = [Follower.Follower(bots,world) for _ in range(1_000)]
print((time()-st))


epsilon = .5
epsilonDecay = .001
step = 0
game = 0
font = pg.font.Font('freesansbold.ttf', 20)
while True:
    game+=1
    Generation = font.render( f"Generation: {int(game/10)}" ,1,(200,200,200))
    GenerationRect = Generation.get_rect()
    GenerationRect.x,GenerationRect.y = 50,300
    mindSizeX = font.render( f"mindSizeX: {bots[0].mindSizeX}" ,1,(200,200,200))
    mindSizeXRect = mindSizeX.get_rect()
    mindSizeXRect.x,mindSizeXRect.y = 50,340
    mindSizeY = font.render( f"mindSizeY: {bots[0].mindSizeY}" ,1,(200,200,200))
    mindSizeYRect = mindSizeY.get_rect()
    mindSizeYRect.x,mindSizeYRect.y = 50,380
    leadership = font.render( f"leadership: {bots[0].leadership}" ,1,(200,200,200))
    leadershipRect = leadership.get_rect()
    leadershipRect.x,leadershipRect.y = 50,420
    speed = font.render( f"speed: {bots[0].speed}" ,1,(200,200,200))
    speedRect = speed.get_rect()
    speedRect.x,speedRect.y = 50,460
    while 0 in [bot.dead for bot in bots]:
        if step == 999:
            for i,bot in enumerate(bots):
                bots[i].dead = True
        if game%50 == 0:
                world.draw()
                world.win.blit(Generation, GenerationRect)
                world.win.blit(mindSizeX, mindSizeXRect)
                world.win.blit(mindSizeY, mindSizeYRect)
                world.win.blit(leadership, leadershipRect)
                world.win.blit(speed, speedRect)
                for bot in bots:
                    bot.Action(epsilon,world)
                [follower.action(world) for follower in followers]
                world.update()
        else:
            for bot in bots:
                bot.Action(epsilon)
            [follower.action() for follower in followers]
        step+= 1
        

    [bot.lastUpdate() for bot in bots]
    

    for bot in bots:
        bot.reset()
    print(game,epsilon,max([bot.avgScore for bot in bots]),step)  
    if game%10 == 0:
        [bot.colorReset() for bot in bots]
        bots = Evolve.Evolve(bots,.01).bots
        [bot.scoreReset() for bot in bots]
        followers = [Follower.Follower(bots,world) for _ in range(1_000)]
    epsilon -= epsilon*epsilonDecay
    if epsilon < .0001:
        epsilon = .5
    step = 0