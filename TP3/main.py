#resource: https://www.youtube.com/watch?v=i6xMBig-pP4
#https://www.cs.cmu.edu/~112/schedule.html
#https://www.pygame.org/docs/ref/music.html


import module_manager
module_manager.review()
import pygame
from pygame.locals import *
import os
import random
mapWidth=600
mapHeight=600
tileSize=40
screenWidth=800
screenHeight=600
#image from https://www.google.com/search?q=bomberman+wallpaper&tbm=isch&ved=2ahUKEwjm2Z-QyY3pAhUBOK0KHcq2BqUQ2-cCegQIABAA&oq=bomberman+wallpaper&gs_lcp=CgNpbWcQAzICCAAyBAgAEEMyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIAFC4I1iVM2CINGgAcAB4AIAB9AKIAc0KkgEDMy00mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=SGqpXuaVO4HwtAXK7ZqoCg&bih=763&biw=1440&client=safari#imgrc=O0vvVeb9XEpvqM
barImg=pygame.image.load('bar.png')
barImg=pygame.transform.scale(barImg,(800,600))
tileImg=pygame.image.load('tile.png')
tileImg=pygame.transform.scale(tileImg,(tileSize,tileSize))
ebImg=pygame.image.load('eb.png')
ebImg=pygame.transform.scale(ebImg,(tileSize,tileSize))
def makeLand(screen):
    for row in range(15):
        for col in range(15):
            screen.blit(tileImg,(listToCoor(row,col)))


#images of these two sprites from https://www.spriters-resource.com/mobile/bombermanforandroid/sheet/88874/

walkDownImgsEnm=['enmD1.png','enmD2.png','enmD3.png']
walkDownEnm=[]
for img in walkDownImgsEnm:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkDownEnm.append(img)
walkUpImgsEnm=['enmU1.png','enmU2.png','enmU3.png']
walkUpEnm=[]
for img in walkUpImgsEnm:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkUpEnm.append(img)

walkRightImgsEnm=['enmR1.png','enmR2.png','enmR3.png']
walkRightEnm=[]
for img in walkRightImgsEnm:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkRightEnm.append(img)

walkLeftEnm=[]
for img in walkRightImgsEnm:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    img=pygame.transform.flip(img, True, False)
    walkLeftEnm.append(img)


#player sprite images
walkDownImgs=['1.png','2.png','3.png']
walkDown=[]
for img in walkDownImgs:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkDown.append(img)

walkUpImgs=['u1.png','u2.png','u3.png']
walkUp=[]
for img in walkUpImgs:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkUp.append(img)
walkLeftImgs=['l1.png','l2.png','l3.png']
walkLeft=[]
for img in walkLeftImgs:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkLeft.append(img)
walkRightImgs=['r1.png','r2.png','r3.png']
walkRight=[]
for img in walkRightImgs:
    img=pygame.image.load(img)
    img=pygame.transform.scale(img,(tileSize,tileSize))
    walkRight.append(img)
startImg=pygame.image.load('start.png')
startImg = pygame.transform.scale(startImg, (screenWidth, screenHeight))
# from http://getwallpapers.com/wallpaper/full/1/c/8/1079104-bomberman-wallpaper-1920x1080-for-samsung-galaxy.jpg

#image from https://ya-webdesign.com/imgdownload.html
magicImg=pygame.image.load('magic.png')
magicImg = pygame.transform.scale(magicImg, (tileSize, tileSize))

startButton=pygame.image.load('button1.png')

# image from https://www.spriters-resource.com/pc_computer/ragnarokonline/sheet/126506/      
bombImgs=[]
bombImgsList=['bomb2.png','bomb3.png','bomb4.png','bomb5.png']
for bombImg in bombImgsList:
    bombImgs.append(pygame.image.load(bombImg))
# image from https://www.cleanpng.com/png-sprite-gamemaker-studio-animation-2d-computer-grap-4805318/download-png.html    
fireImgs=[]
fireImgsList=['fire1.png','fire2.png','fire3.png','fire4.png','fire5.png']
for fireImg in fireImgsList:
    fireImgs.append(pygame.image.load(fireImg))




#create a maze that makes sures at the beginning, there is a cleared path that 
#goes form the top left corner to the bottom right corner. And then put exploisive
#blocks on this path.

# learning material: 
# https://en.wikipedia.org/wiki/Maze_solving_algorithm
# http://www.migapro.com/depth-first-search/

rows=15
cols=15
class Map(object):
    def __init__(self):
        self.make=[[None for row in range(rows)] for col in range(cols)]
        self.initialLocation=[(1,1),(0,0),(1,0),(0,1),(14,14),(14,13),(13,13),(13,14)]

    def generate(self):
        path=getMaze(self.make)
        for row in range(rows):
            for col in range(cols):
                if (row,col)in path or (row,col) in self.initialLocation:
                    self.make[row][col]='e' 
                else: 
                    self.make[row][col]='b'
        for i in range(len(path)//2):
            location=random.choice(path)
            if location not in self.initialLocation:
                self.make[location[0]][location[1]]='eb'
maze=Map()
def getMaze(maze):
    start=(0,0)
    stack=[start]
    while len(stack)>0:
        block=stack.pop()
        nextBlock=getNext(block,maze)
        if nextBlock!=False  :
            stack.append(block)
            stack.append(nextBlock)
          #  print('stack',stack)
            if nextBlock[0]==cols-1 and nextBlock[1]==rows-1:
                return stack
 
def getNext(block,maze):
    directions=['u','d','r','l']
    random.shuffle(directions)
    for direction in directions:
        x,y=getNextHelper(block,direction)
        if x >= cols or x<0 or y>=rows or y<0:
            continue
        if maze[x][y]:
            continue
        maze[x][y]='1'
        return (x,y)
    return False 

def getNextHelper(block,direction):
    x=block[0]
    y=block[1]
    if direction=='u':
        y-=1
    elif direction=='d':
        y+=1
    elif direction=='l':
        x-=1
    elif direction=='r':
        x+=1
    return x,y



def listToCoor(row,col):
    x=col*tileSize
    y=row*tileSize  
    return (x,y)
(startX,startY)=(listToCoor(14,14))

def coorToList(x,y):
    col=x//tileSize
    row=y//tileSize
    
    return (row,col)


class explosiveBlock(pygame.sprite.Sprite):

    def __init__(self,x,y):
        self.x=x
        self.y=y
        (self.row,self.col)=coorToList(self.x,self.y)
        pygame.sprite.Sprite.__init__(self)
        self.image=ebImg
        self.hit=False 
      
    def draw(x,y):
        screen.blit(self.image,(x,y))
    def reset(self):
        #print('resetting')
        if self.hit==True:
           # print('hit')
            maze.make[self.row][self.col]='e'
      



class Magic(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=magicImg
        self.hit=False 
        self.x=x
        self.y=y
        self.rect= self.image.get_rect()
       # self.rect.center=(400,400)

magic=Magic(listToCoor(13,13)[0],listToCoor(13,13)[1])
magic_group=pygame.sprite.Group()
magic_group.add(magic)
bombGroup=pygame.sprite.Group()


class Bomb(pygame.sprite.Sprite):
    def __init__(self,x,y,player):
        pygame.sprite.Sprite.__init__(self)
        self.player=player
        self.x=x
        self.y=y
        self.index=0
        self.life=10
        self.fireindex=0
     
        self.locationList=[]
        for i in range(player.fireRange):
            self.locationList.append((self.x-i*tileSize,self.y))
            self.locationList.append((self.x+i*tileSize,self.y))
            self.locationList.append((self.x,self.y+i*tileSize))
            self.locationList.append((self.x,self.y-i*tileSize))
      
        #print(self.locationList)
    def update(self):
        self.index+=1
       
        self.life-=1
        if self.index>=4:
            self.index=0
    def updateFire(self):
        self.fireindex+=1
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load('1.png')
        self.rect=self.image.get_rect()
        self.alive=True 
        self.fireRange=2  #0 1 
        self.x=startX
        self.y=startY
        (self.row, self.col)=coorToList(self.x,self.y)
        self.stepCount=0
        self.direction=2
        self.index=0
        self.nextX=self.x
        self.nextY= self.y

    def canMove(self,nextX,nextY):
        (nextRow,nextCol)=coorToList(nextX,nextY)
        if nextX>=600 or nextY>=600:
            return False 
        return maze.make[nextRow][nextCol]=='e'   
    def move(self):
        key=pygame.key.get_pressed()
        dis=tileSize 
        if key[pygame.K_SPACE]:
            bomb=Bomb(self.x,self.y,player1)
            bombGroup.add(bomb)
        if key[pygame.K_DOWN]:   
            (self.nextX,self.nextY)=(self.x,self.y+dis) 
            if self.canMove(self.nextX,self.nextY):
                self.y+=dis
            self.direction=2
        elif key[pygame.K_UP]:
            (self.nextX,self.nextY)=(self.x,self.y-dis) 
            if self.canMove(self.nextX,self.nextY):
                self.y-=dis
            self.direction=1
        elif key[pygame.K_RIGHT]:
            (self.nextX,self.nextY)=(self.x+dis,self.y) 
            if self.canMove(self.nextX,self.nextY):
                self.x+=dis
            self.direction=4
        elif key[pygame.K_LEFT]:
            (self.nextX,self.nextY)=(self.x-dis,self.y) 
            if self.canMove(self.nextX,self.nextY):
                self.x-=dis
            self.direction=3 
        self.rect.topleft = self.x, self.y

    def update(self):
        self.index+=1
        if self.index>=3:
            self.index=0
 
    def draw(self,surface):
                if self.direction==1:
                  
                    surface.blit(walkUp[self.index],(self.x,self.y))
                elif self.direction==2:
                    surface.blit(walkDown[self.index],(self.x,self.y))
                elif self.direction==4:
                    surface.blit(walkRight[self.index],(self.x,self.y))
                elif self.direction==3:
                    surface.blit(walkLeft[self.index],(self.x,self.y))
                else:
                    surface.blit(walkDown[0],(self.x,self.y))
    

player1=Player()
player_group=pygame.sprite.Group()
player_group.add(player1)

dis=tileSize 


(startX2,startY2)=(40,40)
class Enemy(Player):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.alive=True
            self.x=startX2
            self.y=startY2
            self.fireRange=2
            self.image=walkDownEnm[0]
            self.rect=self.image.get_rect()
            self.alive=True 
            self.left=False
            self.right=False
            self.up=False
            self.down=False 
            self.direction=2
            self.stepCount=0
            self.index=0
            self.waitCount=0
            self.d=None
            (self.row,self.col)=coorToList(self.x,self.y)
            self.next=[]
            self.check=True
            self.waiting=False 
    def randomMove(self):
        num=random.randint(1,5)
        self.move(num)

        
    def playerIsNear(self,player):
            playerLocation=(player.x,player.y)
            rangeList=[]
            for dis in range(-tileSize*3,tileSize*3):
                rangeList.append((self.x+dis,self.y))
                rangeList.append((self.x,self.y+dis))
            if playerLocation in rangeList:
                return True 
            return False 

    def startWaiting(self):
        self.waitCount+=1
        
    def move(self,num):
        if num==2:
            
            (self.nextX,self.nextY)=(self.x,self.y+dis) 
            if self.canMove(self.nextX,self.nextY):
                self.y+=dis
            self.direction=2
        elif num==1:
            (self.nextX,self.nextY)=(self.x,self.y-dis) 
            if self.canMove(self.nextX,self.nextY):
                self.y-=dis
            self.direction=1
        elif num==4:
            (self.nextX,self.nextY)=(self.x+dis,self.y) 
            if self.canMove(self.nextX,self.nextY):
                self.x+=dis
            self.direction=4
        elif num==3:
            (self.nextX,self.nextY)=(self.x-dis,self.y) 
            if self.canMove(self.nextX,self.nextY):
                self.x-=dis
            self.direction=3 
        self.rect.topleft = self.x, self.y
       
    def update(self):
        self.index+=1
        if self.index>=3:
            self.index=0
    def wait(self):
        if self.waiting==True:
            self.waitCount+=1
        else: self.waitiCount=0

    def draw(self,surface):
        if self.direction==1:
            surface.blit(walkUpEnm[self.index],(self.x,self.y))
        elif self.direction==2:
            surface.blit(walkDownEnm[self.index],(self.x,self.y))
        elif self.direction==4:
            surface.blit(walkRightEnm[self.index],(self.x,self.y))
        elif self.direction==3:
            surface.blit(walkLeftEnm[self.index],(self.x,self.y))
        else:
            surface.blit(walkDownEnm[0],(self.x,self.y))

    def dropBomb(self):
            bomb=Bomb(self.x,self.y,self)
            bombGroup.add(bomb)
            self.waitCount+=1
    
enemy=Enemy()

       
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        #image from https://www.spriters-resource.com/mobile/bombermanforandroid/sheet/70111/
        self.image=pygame.image.load('block.png')
        self.image = pygame.transform.scale(self.image, (tileSize,tileSize))
        self.rect=self.image.get_rect()
        
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))

screen=pygame.display.set_mode((screenWidth,screenHeight))
pygame.init()
clock=pygame.time.Clock()


#the start menu of the game


def mainMenu():
    #music by Nxon. From https://www.youtube.com/watch?v=0aysffpX9c0&list=PLtdWdFWSYZKVrphexN_zLzWSkLqiy8SRS
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(-1)
  
    while True:
        screen.blit(startImg,(0,0))
        screen.blit(startButton,(600,500))
        startButtonRect=startButton.get_rect()
        startButtonRect.topleft=(600,500)
        startButtonWidth,startButtonHeight=startButton.get_size()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                os._exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:        
                mousePosx,mousePosy=event.pos
                #if hit the button start, start playing the game
                if mousePosx in range(startButtonRect.x,startButtonRect.x+startButtonWidth) and mousePosy in range(startButtonRect.y,startButtonRect.y+startButtonHeight):
                        game.play(game.level)
        pygame.display.update()  

class Game(object):
    def __init__(self):
        self.level=0
        self.won=0
        self.lost=0
    def play(self,level):
        playGame(level)
game=Game()
msg = "You have won " + str(game.won) + " times"
msg2 = "You have lost " + str(game.lost) + " times"
font = pygame.font.SysFont('Comic Sans MS', 23)
text = font.render(msg, True, (0, 0, 0))
#textWinTimes = myfont.render(game.won, False, (0, 0, 0))
text2=font.render(msg2, True, (0, 0, 0))

def getHit(eb,location):
    if eb.x==location[0] and eb.y==location[1]:
        eb.hit=True 
        return True
    return False 

def playGame(level):
    game.level+=1
    player1.alive=True
    player1.x=startX
    player1.y=startY
    enemy.x=startX2
    enemy.y=startY2 
    maze.make=[[None for row in range(rows)] for col in range(cols)]
    maze.generate()
    ebLocations=[]
    eb_group=pygame.sprite.Group()
    for row in range(len(maze.make)):
        for col in range(len(maze.make[0])):
            (x,y)=listToCoor(row,col)
            if maze.make[row][col]=='eb':
                ebLocations.append((x,y)) 
                eb=explosiveBlock(x,y)
                if eb.hit==False:
                    eb_group.add(eb)  
    blockLocationList=[]

    for row in range(len(maze.make)):
        for col in range(len(maze.make[0])):
            tilex=(col)*tileSize
            tiley=(row)*tileSize  
            if maze.make[row][col] =='b':
                blockLocationList.append((tilex,tiley))
    block_group=pygame.sprite.Group()
    for blockLocation in blockLocationList:
        x=blockLocation[0]
        y=blockLocation[1]
        block=Block(x,y)
        block_group.add(block)
    while True:
        clock.tick(600)
      #  screen.blit(bgImg,(0,0))
        screen.blit(barImg,(0,0))
        screen.blit(text,(625,500))
        screen.blit(text2,(625,520))
        makeLand(screen)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                os._exit(0)
        player1.move()
        player1.update()
        if player1.alive:
            player1.draw(screen)
        
        
        #game AI 
        # the first round 
        if level<5:
            enemy.update()
            enemy.draw(screen)
            enemy.randomMove()
      
        elif level>=5:
            enemy.update()
            enemy.draw(screen)
            if enemy.playerIsNear(player1):
                enemy.dropBomb()
            (row,col)=coorToList(enemy.x,enemy.y)
            fireArea=[(row-1,col),(row,col+1),(row+1,col),(row,col-1)]
            n=(row-2,col)
            s=(row+2,col)
            w=(row,col-2)
            e=(row,col+2)
            nw=(row-1,col-1)
            se=(row+1,col+1)
            sw=(row+1,col-1)
            ne=(row-1,col+1)
            escapes=[n,s,w,e,nw,se,sw,ne]
            num=enemy.direction
            dict={1:(-1,0),2:(1,0),3:(0,-1),4:(0,1)}
            if maze.make[row+dict[enemy.direction][0]][col+dict[enemy.direction][1]]=='eb' and enemy.waiting==False:
                #print('found eb')
                #if map[pos[0]][pos[1]]=='eb':
                    #print('this person',row,col)
                if maze.make[n[0]][n[1]]=='e' and maze.make[row-1][col]=='e':
                    print('n',n)
                    enemy.dropBomb()
                    enemy.next.insert(0,1)
                    enemy.next.insert(0,1)
                    enemy.waiting=True
                elif maze.make[s[0]][s[1]]=='e' and maze.make[row+1][col]=='e':
                    print('s')
                    enemy.dropBomb()
                    enemy.next.insert(0,2)
                    enemy.next.insert(0,2)
                    enemy.waiting=True
                elif maze.make[nw[0]][nw[1]]=='e': 
                
                    if maze.make[row-1][col]=='e':
                        print('nw1')
                        enemy.dropBomb()
                        enemy.next.insert(0,3)
                        enemy.next.insert(0,1)
                        enemy.waiting=True
                        
                    elif maze.make[row][col-1]=='e':
                        print('nw2')
                        enemy.dropBomb()
                        enemy.next.insert(0,1)
                        enemy.next.insert(0,3)
                        enemy.waiting=True
                elif maze.make[sw[0]][sw[1]]=='e': 
                    if maze.make[row+1][col]=='e':
                        print('sw1')
                        enemy.dropBomb()
                        enemy.next.insert(0,3)
                        enemy.next.insert(0,2)
                        enemy.waiting=True
                    elif maze.make[row][col-1]=='e':
                        print('sw2')
                        enemy.dropBomb()
                        enemy.next.insert(0,2)
                        enemy.next.insert(0,3)
                        enemy.waiting=True
                elif maze.make[se[0]][se[1]]=='e': 
                    if maze.make[row][col+1]=='e':
                        print('se1')
                        enemy.dropBomb()
                        enemy.next.insert(0,2)
                        enemy.next.insert(0,4)
                        enemy.waiting=True
                    elif maze.make[row+1][col]=='e':
                        print('se2')
                        enemy.dropBomb()
                        enemy.next.insert(0,4)
                        enemy.next.insert(0,2)
                        enemy.waiting=True
                elif maze.make[ne[0]][ne[1]]=='e': 
                    if maze.make[row-1][col]=='e':
                        print('ne1')
                        enemy.dropBomb()
                        enemy.next.insert(0,4)
                        enemy.next.insert(0,1)
                        enemy.waiting=True
                    elif maze.make[row][col+1]=='e':
                        print('ne1')
                        enemy.dropBomb()
                        enemy.next.insert(0,1)
                        enemy.next.insert(0,4)
                        enemy.check=False
                        enemy.waiting=True #12345  until 30 3132 
            if enemy.waiting==True:
                enemy.waitCount+=1
            if enemy.waitCount>16:
                enemy.waitCount=0
                enemy.waiting=False 
            if enemy.waiting==True:   
                for num in enemy.next:
                    enemy.move(num)
                enemy.next=[] 
        
            #print('waitCount',enemy.waitCount)  
            if enemy.waiting==False:
                #print('not waiting')
                enemy.randomMove()
       # elif level>=5: 

        for bomb in bombGroup:
            bomb.update()
            if bomb.life>0: 
                screen.blit(bombImgs[bomb.index],(bomb.x,bomb.y))
            elif bomb.life<0 and bomb.fireindex<=3:
                bomb.updateFire()
                screen.blit(fireImgs[bomb.fireindex],(bomb.x,bomb.y))
                for location in bomb.locationList:
                    #print(bomb.locationList)
                    if getHit(player1,location):
                        player1.alive=False
                        game.lost+=1                        
                        game.play(game.level)

                    elif getHit(enemy,location):
                        enemy.alive=False    
                        game.won+=1                       
                        game.play(game.level)
                    for eb in eb_group:
                        #print(eb.row,eb.col,map[eb.row][eb.col])
                        if getHit(eb,location)==True:
                            eb.reset()
                            eb_group.remove(eb)
                          #  print(map[eb.row][eb.col])
                    screen.blit(fireImgs[bomb.fireindex],location)  
        #print(eb_group)
        for eb in eb_group:
            screen.blit(ebImg,(eb.x,eb.y))
            pygame.display.update()
        for magic in magic_group:
            if getHit(magic,[player1.x,player1.y]):
                player1.fireRange=3
                magic_group.remove(magic)
            screen.blit(magicImg,(magic.x,magic.y))
        for block in block_group:
            block.draw(screen)
        pygame.display.update()
mainMenu()