import numpy as np
import pygame as pg
import World
import Blob
from time import sleep,time


world = World.World()
st = time()
bobs = [LeadBlob(world) for _ in range(1_000)]
print((time()-st))

qtable = np.random.rand(245,185,4)
epsilon = .7
epsilonDecay = .01
step = 0
game = 0
while True:
    while step < 1100 and False in [bob.dead for bob in bobs]:
        for bob in bobs:
            bob.Action(epsilon)
        if game%10 ==0:
            world.draw()
            [pg.draw.rect(world.win,(100,100,200),bob.me) for bob in bobs]
            world.update()
        step+= 1

    print(epsilon,max([bob.score for bob in bobs]))  
    for bob in bobs:
            bob.restart()
    epsilon -= epsilon*epsilonDecay
    if epsilon < .001:
        epsilon = .6
    step = 0
    
    game+=1
    done = False