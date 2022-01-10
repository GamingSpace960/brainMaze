from math import sqrt
import numpy as np
import pygame as pg
class Follower():
    def __init__(self,leaders,world):
        self.leadership=np.random.randint(1,50+1)
        self.speed = np.random.randint(1,5)
        self.color = (200,200,200)
        self.world = world
        self.leader = None
        self.reset()
        leaders = [[leader,sqrt((leader.me.x-self.me.x)**2 + (leader.me.y-self.me.y)**2)] for leader in leaders]
        leaders.sort(key=self.closestLeader)
        for leader in leaders:
            if leader[0].leadership > self.leadership:
                self.leader = leader[0]
                break
        if self.leader == None:
            self.leader = leaders[0][0]


    def closestLeader(self,leader):
        return leader[1]

    def draw(self,world):
        pg.draw.rect(world.win,self.color,self.me)

    def action(self,world=None):
        if self.dead:
            if world != None:
                self.draw(world)
            return
        if abs(self.leader.me.x-self.me.x) >= abs(self.leader.me.y-self.me.y):
            if self.leader.me.x-self.me.x > 0:
                self.me.x += 2*self.speed
            elif self.leader.me.x-self.me.x < 0:
                self.me.x -= 2*self.speed
        else:
            if self.leader.me.y-self.me.y > 0:
                self.me.y += 2*self.speed
            else:
                self.me.y -= 2*self.speed
        if self.me.collidelist(self.world.walls) != -1:
            self.dead = 1
        elif self.me.colliderect(self.world.goal):
            self.won = 1
            self.dead = 1
            self.leader.tempScore+=30_000
            
        if world != None:
            self.draw(world)


    def reset(self):
        x = np.random.randint(370/2,450/2+.5)*2
        y = np.random.randint(310/2,370/2+.5)*2
        self.me = pg.draw.rect(self.world.win,self.color,(x,y,2,2))
        self.dead = False
        self.won = False
        self.time = 0




