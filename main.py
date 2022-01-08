

if __name__ == '__main__':

    import numpy as np
    import pygame as pg
    import World
    from  BlobSolo import LeadBlob
    import Evolve
    from time import sleep,time
    from multiprocessing import Pool

    world = World.World()
    st = time()
    botWorld = world.wallsList.copy()
    bots = [LeadBlob() for _ in range(1_000)]
    epsilon = .5
    #epsilonDecay = .01
    step = 0
    game = 0
    st = time()
    while 1:
        game+=1
        while False in [bot.dead for bot in bots]:
            if step == 999:
                for i,bot in enumerate(bots):
                    bots[i].dead = True
            elif game%50 == 0:
                    world.draw()
                    pg.draw.rect(world.win ,(200,200,200),(370,310,80,60))
                    pg.draw.rect(world.win ,(200,200,10),((bots[0].mindSizeX-244)*-2,(bots[0].mindSizeY-184)*-2,490-(bots[0].mindSizeX-244)*-2,10))
                    pg.draw.rect(world.win ,(200,200,10),((bots[0].mindSizeX-244)*-2,(bots[0].mindSizeY-184)*-2,10,370-(bots[0].mindSizeY-184)*-2))
                    for bot in bots:
                        bot.Action(epsilon,botWorld)
                        pg.draw.rect(world.win,bot.color,(bot.me[0],bot.me[1],2,2))
                    world.update()
            else:
                st=time()
                [bot.Action(epsilon,botWorld) for bot in bots]
                #print(time()-st,1)
            step+= 1
        
        [bot.reset() for bot in bots]
        if game%10 == 0:
            [bot.colorReset() for bot in bots]
            bots = Evolve.Evolve(bots).bots
        print(game,step,epsilon,bots[0].timebackup,bots[0].mindSizeX,bots[0].mindSizeY,bots[0].speed,bots[0].leadership,bots[0].avgScore)  
        epsilon = .0001
        #epsilon -= epsilon*epsilonDecay
        #if epsilon < .0001:
        #    epsilon = .5
        step = 0