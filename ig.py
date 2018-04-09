import pygame
from pygame.locals import *
import random

pygame.init()
window_size = (800, 600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(window_size)
img_char = pygame.image.load('bg.png')

class Unit:
    def __init__(self,x,y,n,t,v,s):
        self.x=x
        self.y=y
        self.n=n
        self.t=t
        self.v=v
        self.s=s
        self.dx=0
    def draw(self,screen):
        if self.v==0:return
        scale=self.s
        temp = pygame.transform.rotozoom(spimg[self.n], 0, scale)
        screen.blit(temp, (self.x,self.y))
    def hit(self,other):
        return abs(self.x-other.x)<60 and abs(self.y-other.y)<60

def spset():
    for y in range(10):
        for x in range(10):
            temp = pygame.Surface((16, 16), pygame.SRCALPHA)
            temp.blit(img_char, (0, 0), (x * 16, y * 16, 16, 16))
            spimg.append(temp)

def randset():
    for i in range(100):
        u.append(Unit(rnd(800),rnd(540),21,1,10,4 ))
        u[i].dx=2
    for i in range(5):
        m.append(Unit(rnd(800),600,22,1,0,4 ))

def rnd(n):
    return random.randrange(0, n)

spimg = []
u=[]
m=[]
jk=[]

def main():
    jk.append(Unit(400,550,20,1,10,4 ))
    mw=0
    spset()
    randset()
    pygame.key.set_repeat (1, 1)
    #pygame.mixer.music.load('field03.mp3')
    #pygame.mixer.music.play(-1)
    end_game = False
    while not end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:end_game = True
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if jk[0].x>0:jk[0].x -= 5
                if event.key == K_RIGHT:
                    if jk[0].x<800-16:jk[0].x += 5
                if event.key == K_SPACE and mw==0:
                    for i in range(len(m)):
                        if m[i].v==0:
                            m[i].v=1
                            m[i].x=jk[0].x
                            m[i].y=jk[0].y-64
                            mw=20
                            break
        screen.fill((0,0,0))
        for i in range(len(u)):
            for j in range(len(m)):
                if m[j].v>0:
                    if u[i].hit(m[j]):
                        u[i].v=0
            u[i].x+=u[i].dx
            if u[i].x>740:
                u[i].y+=32
                u[i].dx=-2
            if u[i].x<0:
                u[i].y+=32
                u[i].dx=2
            if u[i].y>600:u[i].y=-32
            u[i].draw(screen)
        for i in range(len(m)):
            m[i].draw(screen)
            m[i].y-=3
            if m[i].y<-100:m[i].v=0
        jk[0].draw(screen)
        if mw>0:mw-=1
        pygame.display.flip()
    pygame.quit()
    quit()

main()
