# Flappy Bird, wrote on April 24th, 2024

import pygame as pg
import random as r

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480


speed = WINDOW_WIDTH/250
pipeDist = WINDOW_WIDTH/5
gravity = 0.4

gameOverTime = 100

pg.init()
clock = pg.time.Clock()

fps = 30

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 

def fpsCoeff():
    currentFps = clock.get_fps()
    if currentFps == 0:
        return 1
    else:
        return fps / currentFps

class PipePair(object):
    w = WINDOW_WIDTH /16
    h = WINDOW_HEIGHT*0.7

    gap = WINDOW_HEIGHT*0.3
    margin = 10

    pic = pg.image.load("./res/pipe.bmp")
    pic = pg.transform.scale(pic, (w,h))
    pic_180 = pg.transform.rotate(pic,180)
    vX = speed

    def __init__(self):
        self.x = WINDOW_WIDTH
        self.y = r.randint(int(PipePair.margin), int(WINDOW_HEIGHT-PipePair.gap-Environment.groundH-PipePair.margin))
        self.scored = False

    def move(self): # return if scored
        ox = self.x
        self.x-= PipePair.vX*fpsCoeff()
        if ox > Bird.x and self.x < Bird.x and self.scored == False:
            self.scored = True
            return True
        return False

    def show(self):
        screen.blit(PipePair.pic_180,(self.x,self.y-self.h))
        screen.blit(PipePair.pic,(self.x,self.y + PipePair.gap))
        

class Bird(object):
    w = WINDOW_WIDTH/25
    h = w/1.3
    x = WINDOW_WIDTH*0.3

    pic = pg.transform.scale(pg.image.load("./res/Bird.bmp"), (w,h))
    pic2 = pg.transform.scale(pg.image.load("./res/Bird2.bmp"), (w,h))

    def __init__(self):
        self.y=WINDOW_HEIGHT/2
        self.vY = 0
        self.wingsUp = 1 

    def move(self):
        self.y += self.vY*fpsCoeff()
        self.vY += gravity # add gravity
        
        self.wingsUp += 1
        self.wingsUp %= 10

    def flap(self):
        self.vY = -5

    def show(self):
        angle = -self.vY*2

        if self.wingsUp < 5:
            screen.blit(pg.transform.rotate(Bird.pic,angle),(Bird.x,self.y))
        else:
            screen.blit(pg.transform.rotate(Bird.pic2,angle),(Bird.x,self.y))

class Environment:
    backPic = pg.transform.scale(pg.image.load("./res/Background.bmp"), (WINDOW_WIDTH,WINDOW_HEIGHT))
    backPicW = backPic.get_width()

    groundPic = pg.transform.scale(pg.image.load("./res/Ground.bmp"), (WINDOW_WIDTH/3,WINDOW_WIDTH/9))
    groundPicH = groundPic.get_height()
    groundPicW = groundPic.get_width()
    groundH = WINDOW_HEIGHT/10

    def __init__(self):
        self.groundX = 0
        self.backX = 0
        self.pipePairs = []

        self.started = False

    def update(self, ui, started):
        # move ground
        self.groundX -= speed*fpsCoeff()
        if self.groundX <= -Environment.groundPicW:
            self.groundX = 0

        # move background
        self.backX -= speed/2 *fpsCoeff()
        if self.backX <= -Environment.backPicW:
            self.backX = 0

        # move pipe pairs
        for pipePair in self.pipePairs:
            if pipePair.move():
                ui.changeScore(1)

        # manage pipe pairs
        if started:
            if len(self.pipePairs) == 0 or WINDOW_WIDTH - (self.pipePairs[-1].x + PipePair.w) > pipeDist:
                self.pipePairs.append(PipePair())
        
        if len(self.pipePairs) > 0: 
            if self.pipePairs[0].x + PipePair.w < 0:
                del self.pipePairs[0]
    
    def collide(self,bird):
        if bird.y + Bird.h > WINDOW_HEIGHT-Environment.groundH:
            return True
        
        for pipePair in self.pipePairs:
            if pipePair.x < bird.x < pipePair.x + PipePair.w or pipePair.x < bird.x + Bird.w < pipePair.x + PipePair.w:
                if bird.y + Bird.h > pipePair.y + PipePair.gap or bird.y < pipePair.y:
                    return True
        return False

    def show(self, ui, started):
        # show background pieces
        for x in range(int(self.backX),WINDOW_WIDTH,WINDOW_WIDTH):
            screen.blit(self.backPic,(x,-Environment.groundH+4))

        ui.show(started)

        # show pipes
        for pipePair in self.pipePairs:
            pipePair.show()

        # show ground pieces
        for x in range(int(self.groundX),WINDOW_WIDTH,Environment.groundPicW):
            screen.blit(Environment.groundPic,(x,WINDOW_HEIGHT-Environment.groundH))

class UI:
    planeYc = WINDOW_HEIGHT * 0.25 # y center position

    planeW = WINDOW_WIDTH/4
    planeH = planeW*0.17

    planeY = planeYc - planeH/2
    planePic = pg.transform.scale(pg.image.load("./res/BannerPlane.bmp"), (planeW,planeH))

    fontColor = (255,0,0)
    fontSize = WINDOW_HEIGHT/20
    font = pg.font.Font("freesansbold.ttf", int(fontSize))

    goLabel = font.render("Game Over" , True, fontColor) # GAME OVER LABEL
    goX = WINDOW_WIDTH/2-goLabel.get_width()/2
    goY = WINDOW_HEIGHT/2-goLabel.get_height()/2

    tapPicW = WINDOW_WIDTH/5
    tapPicH = WINDOW_HEIGHT/4
    tapPic = pg.transform.scale(pg.image.load("./res/TapToStart.bmp"), (tapPicW,tapPicH))


    def __init__(self):
        self.planeX = 0
        self.scoreLabelX = -2*UI.planeW/3-10 # scoreLabelX
        self.score = 0
        self.changeScore(0)
        
    def update(self):
        if ui.planeX < WINDOW_WIDTH/2-(UI.planeW/3)+UI.planeW:
            self.planeX += speed*fpsCoeff()

        if self.scoreLabelX < WINDOW_WIDTH/2-self.scoreLabel.get_width()/2:
            self.scoreLabelX += speed*fpsCoeff()

    def changeScore(self,value):
        self.score += value
        self.scoreLabel = UI.font.render(str(self.score), True, UI.fontColor)
        self.scoreLabelY = UI.planeYc - self.scoreLabel.get_height()/2

    def show(self, started):
        if started == False:
            screen.blit(UI.tapPic, (WINDOW_WIDTH*0.6, WINDOW_HEIGHT*0.5))

        screen.blit(UI.planePic,  (self.planeX-UI.planeW, UI.planeY))
        screen.blit(self.scoreLabel,(self.scoreLabelX,self.scoreLabelY))


# WORKING LOOP
work = True
while work:
    # RESET
    bird = Bird()
    environment = Environment()
    ui = UI()
    started = False

    # MAIN GAME RUN LOOP
    gameRun = True
    while gameRun == True:
        # INTERACTION
        for event in pg.event.get():
            if event.type == pg.QUIT:
                work = False
                gameRun = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_d:
                    started = True
                    bird.flap()
                elif event.key == pg.K_ESCAPE:
                    work = False
                    gameRun = False

        # GAME PHYSICS
        if started:
            bird.move()

        environment.update(ui, started)
        gameRun = gameRun and not environment.collide(bird)

        ui.update()

        # SHOW
        environment.show(ui, started) # includes rendering UI
        bird.show()

        pg.display.flip()

        clock.tick(fps)

    # GAME OVER LOOP
    t = gameOverTime * int(work)
    while t > 0:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                t = -1
                work = False
                gameRun = False
        screen.fill((0,0,0))
        screen.blit(UI.goLabel,(UI.goX,UI.goY))
        pg.display.flip()
        clock.tick(fps)
        t -= 1

pg.quit()