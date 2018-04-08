import pygame
from pygame.locals import *
import math
import copy
import random

pygame.init()
window_size = (800, 600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(window_size)
print (pygame.ver)

class Point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class Turn:
    def __init__(self,tx,ty,tz):
        self.tx=tx
        self.ty=ty
        self.tz=tz
    def get(self):
        return self.tx,self.ty,self.tz

class Box:
    def __init__(self,co,size,point):
        self.tten=[]
        self.tten.append((-1,-1,1))
        self.tten.append((1,-1,1))
        self.tten.append((1,-1,-1))
        self.tten.append((-1,-1,-1))
        self.tten.append((-1,1,1))
        self.tten.append((1,1,1))
        self.tten.append((1,1,-1))
        self.tten.append((-1,1,-1))
        self.poly=[]
        self.poly.append([0,1,2,3])
        self.poly.append([4,5,6,7])
        self.poly.append([1,2,6,5])
        self.poly.append([0,3,7,4])
        self.poly.append([0,1,5,4])
        self.poly.append([3,2,6,7])
        self.xy8=[]
        self.wk8=[]
        self.co=co
        self.centerZ=0
        self.resize(size,size,size)
        self.point = point
        self.viewpoint =Point(0,0,0)
        self.viewturn =Turn(0,0,0)
    def __lt__(self, other):
        return self.centerZ > other.centerZ
    def resize(self,sx,sy,sz):
        for i in range(8):
            x,y,z=self.tten[i]
            self.tten[i]=(x*sx,y*sy,z*sz)
    def beforedraw(self):
        self.toWk()
        self.shift(self.point)
        self.shift(self.viewpoint)
        self.turn()
        self.setZ()
    def draw(self,screen):
        if self.viewCut():return
        self.conv3d2d()
        for i in range(6):
            xy4=[]
            for j in range(4):
                xy4.append( self.xy8[self.poly[i][j]] )
            pygame.draw.polygon(screen, self.co, xy4)
    def conv3d2d(self):
        del self.xy8[:]
        for i in range(len(self.wk8)):
            x,y,z=self.wk8[i]
            self.xy8.append(self.conv(x,y,z))
    def conv(self,x,y,z):
        d=200
        rx=x*d/(d+z)+400
        ry=y*d/(d+z)+300
        return (rx,ry)
    def toWk(self):
        self.wk8=copy.deepcopy(self.tten)
    def backWk(self):
        self.tten=copy.deepcopy(self.wk8)
    def shift(self,point):
        for i in range(len(self.wk8)):
            x,y,z=self.wk8[i]
            self.wk8[i]=(x+point.x,y+point.y,z+point.z)
    def pointSet(self,x,y,z):
        self.point = Point(x,y,z)
    def turn(self):
        tx,ty,tz=self.viewturn.get()
        rd=3.1415/180
        if tx!=0:
            ct=math.cos(tx*rd)
            st=math.sin(tx*rd)
            self.turnX(ct,st)
        if ty!=0:
            ct=math.cos(ty*rd)
            st=math.sin(ty*rd)
            self.turnY(ct,st)
        if tz!=0:
            ct=math.cos(tz*rd)
            st=math.sin(tz*rd)
            self.turnZ(ct,st)
    def turnY(self,ct,st):
        for i in range(len(self.wk8)):
            x,y,z=self.wk8[i]
            rx=x*ct-z*st
            rz=x*st+z*ct
            self.wk8[i]=(rx,y,rz)
    def turnZ(self,ct,st):
        for i in range(len(self.wk8)):
            x,y,z=self.wk8[i]
            rx=x*ct-y*st
            ry=x*st+y*ct
            self.wk8[i]=(rx,ry,z)
    def turnX(self,ct,st):
        for i in range(len(self.wk8)):
            x,y,z=self.wk8[i]
            ry=y*ct-z*st
            rz=y*st+z*ct
            self.wk8[i]=(x,ry,rz)
    def viewCut(self):
        x,y,z=self.wk8[0]
        x,y,z1=self.wk8[6]
        return (z+z1)<200
    def setZ(self):
        x,y,z=self.wk8[0]
        x1,y1,z1=self.wk8[6]
        cz=int((z+z1)/2)
        cy=int((y+y1)/2)
        cx=int((x+x1)/2)
        r1=cz**2+cy**2
        self.centerZ=r1+cx**2

def mazeMake(sx,sy,sz):
    del mz[:]
    for z in range(sz):
        my=[]
        for y in range(sy):
            x = [1 for i in range(sx)]
            my.append(x)
        mz.append(my)

    mz[0][0][0]=0
    mz[0][0][1]=0
    mz[1][0][0]=0
    mz[1][0][1]=0

    mz[sz-1][0][sz-1]=0
    mz[sz-1][0][sz-2]=0
    mz[sz-2][0][sz-1]=0

    dx=[-2,2,0,0]
    dz=[0,0,-2,2]
    for i in range(3000):
        rx=random.randint(0,int((sx-1)/2)-1)
        rz=random.randint(0,int((sz-1)/2)-1)
        rx=rx*2+1
        rz=rz*2+1
        if mz[rz][0][rx]==1:continue
        for j in range(20):
            h=random.randint(0,3)
            nx=rx+dx[h]
            nz=rz+dz[h]
            if nx>0 and nx<sx and nz>0 and nz<sz:
                if mz[nz][0][nx]==1:
                    mz[nz][0][nx]=0
                    mz[int((nz+rz)/2)][0][int((nx+rx)/2)]=0
                    rx=nx
                    rz=nz

    for z in range(sz):
        for y in range(sy):
            for x in range(sx):
                if mz[z][y][x]==1:
                    co=(random.randint(80,230),random.randint(80,230),random.randint(80,230))
                    if y>0:co=(100,30,20)
                    b.append( Box(co,200,Point(x*400-400*int(sx/2),y*400,z*400+800)) )

def turnMarge(bx,by,bz,dx,dy,dz):
    rx=bx+dx
    ry=by+dy
    rz=bz+dz
    return rx,ry,rz

def forward(cx,cy,cz,tx,ty,tz,leng):
    ry=cy
    rd=3.1415/180
    ct=math.cos(ty*rd)
    st=math.sin(ty*rd)
    rx=cx-(-leng*st)
    rz=cz+(leng*ct)
    return rx,ry,rz

def wallhit(tx,ty,tz):
    global sizeX,sizeZ
    sx=int((-tx+400*int(sizeX/2))/400)
    sz=int((-tz-800)/400)
    #print(str(int(sx))+" "+str(int(sz))+":"+str(int(tx))+" "+str(int(tz)))
    if sx>=0 and sx<sizeX and sz>=0 and sz<sizeZ:
        if mz[sz][0][sx]==1:return True
    return False

b=[]
mz=[]
sizeX=25
sizeZ=25
def main():
    global sizeX,sizeZ
    cx=0
    cy=50
    cz=0
    tx=0
    ty=0
    tz=0
    sizeX
    sizeZ
    mazeMake(sizeX,2,sizeZ)
    bg_color = (0, 0, 0)
    end_game = False
    tn=0
    while not end_game:
        tn+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                tx,ty,tz=turnMarge(tx,ty,tz,0,-5,0)
            if event.key == K_RIGHT:
                tx,ty,tz=turnMarge(tx,ty,tz,0,5,0)
            if event.key == K_UP:
                rx,ry,rz=forward(cx,cy,cz,tx,ty,tz,-50)
                if wallhit(rx,ry,rz)==False:
                    cx,cy,cz=rx,ry,rz
            if event.key == K_DOWN:
                rx,ry,rz=forward(cx,cy,cz,tx,ty,tz,50)
                if wallhit(rx,ry,rz)==False:
                    cx,cy,cz=rx,ry,rz
        screen.fill(bg_color)

        for i in range(len(b)):
            b[i].viewpoint=Point(cx,cy,cz)
            b[i].viewturn=Turn(tx,ty,tz)
            b[i].beforedraw()
        b.sort()
        for i in range(len(b)):
            b[i].draw(screen)

        pygame.display.flip()
        #clock.tick(5)
    pygame.quit()
    quit()

main()
