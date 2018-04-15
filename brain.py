import pygame
import random
import os

pygame.init()
window_size = (1600, 1000)
screen = pygame.display.set_mode(window_size)
bgmap = pygame.Surface((16000,16000))

parhFileNames = []
searchPath = ["/home/"]#検索したいpathを設定

def fileSearch():
    esw=0
    while len(searchPath)>0 and esw==0:
        try:
            ld = os.listdir(searchPath[0])
        except:
            del searchPath[0]
            continue
        for i in range(len(ld)):
            fileName=searchPath[0] + ld[i]
            if os.path.isdir(fileName):
                searchPath.append(fileName+"/")
            elif (fileName+" ").count(".jpg ")>0:
                parhFileNames.append(fileName)
                if len(parhFileNames)%1000==0:
                    print(len(parhFileNames))
                if len(parhFileNames)>50000:esw=1
        del searchPath[0]

def bgSet(n):
    global bgt,bg
    j=0
    bgt=[]
    bg=[]
    for i in range(n):
        r=random.randint(0,len(parhFileNames)-1)
        try:
            bgt.append(pygame.image.load(parhFileNames[r]))
        except:
            print("error file="+parhFileNames[r])
            continue
        bg.append(pygame.transform.smoothscale(bgt[j],(400,400)))
        j+=1
    for i in range(ｎ):
        r=random.randint(0,len(bg)-1)
        x=random.randint(0,40)
        y=random.randint(0,40)
        bgmap.blit(bg[r], (x*400, y*400), (0,0, 400, 400))

def main():
    end_game = False
    while not end_game:
        bgSet(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:end_game = True
        screen.fill((0,0,0))
        screen.blit(bgmap,(0,0),(random.randint(0,14400),random.randint(0,15000),1600,1000))
        pygame.display.flip()
        pygame.time.delay(100)
    pygame.quit()
    quit()

fileSearch()
main()
