from numpy import random, argmax
from time import sleep,time

class LeadBlob():
    def __init__(self,leadership=random.randint(1,50+1),mindSizeX = random.randint(1,239+1),mindSizeY = random.randint(1,179+1),speed = random.randint(1,6),qtable = []):
        #bounds (370,310)-(440,370)
        # max spots = (440,370)/2 = (220,185)
        # range is 5 -> 220 so -(-5) = +5 is needed for a 0 therefore max mind size is 215/180

        # map size = (10,10,480,360) = pixels = (10,10,490,370)
        # spawn size = (370,310,80,60) = pixels = (370,310,450,370)
        # bots only read top left of themselves so for bot minus 2 for high x & y
        # pixels is value read
        # map size = (10,10,478,358) = pixels = (10,10,488,368)
        # spawn size = (370,310,78,58) = pixels = (370,310,448,368)
        #mind size range = (5,5,244,184)
        #max mind size = (239,179)
        self.games = 0
        self.avgScore = 0
        self.score = 0
        self.time = 0
        self.colorReset()
        self.reset()
        self.leadership = leadership
        self.mindSizeX = mindSizeX
        self.mindSizeY = mindSizeY
        self.speed = speed
        self.lr = .1
        if len(qtable) == 0:
            self.qTable()
        else:
            self.qtable = qtable
        

    def qTable(self):
        self.qtable = random.rand(239,179,4)

    def colisionDetect(self,l1,list2):

        # x = l1[0] = smallest x value
        # X = l1[2] = biggest x value
        # y = l1[1] = smallest y value
        # Y = l1[3] = biggest y value
        # a = l2[0] = smallest x value
        # A = l2[2] = biggest x value
        # b = l2[1] = smallest y value
        # B = l2[3] = biggest y value
        if l1 in [l1 if ((l1[0] >= l2[0] and l1[0] <= l2[2]) or ((l1[2] >= l2[0] and l1[2] <= l2[2]))) and ((l1[1] >= l2[1] and l1[1] <= l2[3]) or ((l1[3] >= l2[1] and l1[3] <= l2[3]))) else -1 for l2 in list2]:
            pass
        else:
            return -1

    def Action(self,epsilon,world):
        if self.dead or self.won:
            return
        elif 244-(self.me[0]/2) < 0 or 184-(self.me[1]/2) < 0:
            print(244-(self.me[0]/2),184-(self.me[1]/2),self.me[0],self.me[1],self.speed)
        elif random.random() > epsilon and len(self.qtable) > 244-(self.me[0]/2) and len(self.qtable[int(244-(self.me[0]/2))-1]) > 184-(self.me[1]/2):
            self.action = argmax(self.qtable[int(244-(self.me[0]/2))-1][int(184-(self.me[1]/2))-1])
        else:
            self.action = random.randint(4)

        x = int(244-(self.me[0]/2))
        y = int(184-(self.me[1]/2))
        
        if self.action == 0:
            self.me[0] -= 2*self.speed
            self.me[2] -= 2*self.speed
        elif self.action == 1:
            self.me[0] += 2*self.speed
            self.me[2] += 2*self.speed
        elif self.action == 2:
            self.me[1] -= 2*self.speed
            self.me[3] -= 2*self.speed
        else:
            self.me[1] += 2*self.speed
            self.me[3] += 2*self.speed
        score = 0
        if self.colisionDetect(self.me,world[1:]) != -1 or (self.me[0],self.me[1]) in self.beenList:
            self.dead = True
            score -= 20_000
        elif self.colisionDetect(self.me,world[:1]) != -1:
            score += 40_000-(2*self.speed*self.time)
            self.won = True
            self.dead = True
        
        self.beenList.append((self.me[0],self.me[1]))
        score += 1*self.speed
        self.score += score
        self.time+=1
        
        if not self.dead and self.mindSizeX >= 244-(self.me[0]/2) and self.mindSizeY >= 184-(self.me[1]/2) and self.mindSizeX >= x and self.mindSizeY >= y:
            self.qtable[x-1][y-1][self.action] += self.lr* ((1-.99)*score + .99*max(self.qtable[int(244-(self.me[0]/2))-1][int(184-(self.me[1]/2))-1]) - self.qtable[x-1][y-1][self.action])
        elif self.mindSizeX >= x and self.mindSizeY >= y:
            self.qtable[x-1][y-1][self.action] += self.lr*( score - self.qtable[x-1][y-1][self.action])


    def reset(self):
        
        
        #print(self.avgScore,self.games,self.score)
        self.games+=1
        self.avgScore = (self.avgScore*(self.games-1) + self.score)/self.games
        #print(self.avgScore,self.games,self.score,2)
        #x = np.random.randint(370/2,448/2+.5)*2
        #y = np.random.randint(310/2,368/2+.5)*2
        x = (448+370)/2
        y = (368+310)/2
        self.me = [x,y,x+1,y+1]
        self.beenList = []
        self.dead = False
        self.won = False
        self.score = 0
        self.timebackup = self.time
        self.time = 0
        if self.games > 100:
            self.games = 0
            self.avgScore = 0

    def colorReset(self):
        self.color = (100,100,200)

    def copy(self):
        return LeadBlob(leadership=self.leadership,mindSizeX = self.mindSizeX,mindSizeY = self.mindSizeY,speed = self.speed, qtable = self.qtable)

