###############################################################################################
# Name: Flappy Bird
# Date: 24.05.19 - newest: 13.8.20
#
# Programming note: ...X / ...Y : Position X / Y
#					...W / ...H : Width / Height
# 					...C        : Color
###############################################################################################


screenW = 800
screenH = 480
fullscreen = False
fullscreenRes = False
resPath = "./res/"

flySpeed = screenW/400
playerX = int(screenW*0.3)
fps = 60

flapForce = -8
gravityForce = 0.3

gateH = int(screenH*0.4)


backgroundC = (50,50,200)
borderThickness = int(screenH/10)
fontC = (255,0,0)
fontSize = int(screenH/20)
groundC = (0,255,0)
groundSize = int(screenW/3)
ceilingC = (50,50,50)

gapBetweenPipes = int(screenW/3)
pipeW = int(screenW /16)
pipeH = int(screenH*0.7)

playerSize = int(screenW/25)
playerC = (255,0,0)

deathCrossSize = int(screenH/12)
auaW = int(screenH/18)
auaH = int(auaW*0.7)

planePicW = int(screenW/4)
planePicH = int(planePicW*0.17)

deathTime = 100

playerStartMoveMode = 1 #1 = sin-wave, 2 = jumping

class Gate(object):
	def __init__(self,yc):
		global gateH
		self.x1=screenW
		self.x2=screenW+pipeW

		self.y1=yc-gateH/2
		if self.y1 < 10:
			self.y1 = -9000
		self.y2=yc+gateH/2

		self.w = pipeW
		self.h = gateH

		self.scored = False
	def move(self):
		self.x1-= speed*clock.get_fps()/60
		self.x2-= speed*clock.get_fps()/60
	def show(self):
		if not self.y1 < 10:
			screen.blit(pipe_upsidedown_pic,(self.x1,self.y1-pipeH))
		screen.blit(pipepic,(self.x1,self.y2))

class Player(object):
	def __init__(self,xc,yc,w,h):
		global borderThickness,playerW,playerH
		self.w = w
		self.h = h
		self.x1=xc-w/2
		self.x2=xc+w/2
		self.y2=screenH/2+self.h/2
		self.y1 = screenH/2-self.h/2
		self.gravityStrength = 0
		self.wingsUp = 1
		self.dead = False
		self.deathTime = 0
		self.deadX = 0
		self.deadY = 0

	def move(self):
		self.y1 += int(self.gravityStrength*clock.get_fps()/60)
		self.y2 += int(self.gravityStrength*clock.get_fps()/60)

		if self.dead == True:
			if self.y2 > screenH-borderThickness:
				self.y2 = screenH-borderThickness
				self.y1 = screenH-borderThickness - self.h

		self.wingsUp += 1
		if self.wingsUp == 10:
			self.wingsUp = 0

	def show(self):
		global playerC,birdPic

		if player.dead:
			screen.blit(deadCrossPic,(self.deadX,self.deadY))
			if player.y2 < (screenH - borderThickness-1):
				screen.blit(pg.transform.rotate(birdPic,-90),(self.x1,self.y1))
				screen.blit(auaPic,(self.x2+4,self.y1-4))
			else:
				screen.blit(ripPic,(self.x1+self.w/2-(ripW/2)-player.w*2, self.y1+self.h/2-(ripH/2)))
				screen.blit(skelettPic,(self.x1, self.y1+self.h/2+(ripH/2)+10))
				screen.blit(auaPic,(self.x1+self.w+4,self.y1+self.h/2+(ripH/2)-4))


		else:
			if self.wingsUp < 5:
				pic = pg.transform.rotate(birdPic,-self.gravityStrength*2)
				screen.blit(pic,(int(self.x1),int(self.y1)))
			if self.wingsUp >= 5:
				pic = pg.transform.rotate(birdPicW,-self.gravityStrength*2)
				screen.blit(pic,(int(self.x1),int(self.y1)))

###############
# Program start


import pygame as pg
import random as r
from time import sleep
import math
pg.mixer.pre_init(44100, -16, 1, 512)
pg.mixer.init()
pg.init()


#please don't change:
work = True
clock = pg.time.Clock()
clock.tick(60)

screeninfo = pg.display.Info() #needed for displaying the right screen resolution

if fullscreen:
	if fullscreenRes:
		screen = pg.display.set_mode((screeninfo.current_w,screeninfo.current_h),pg.FULLSCREEN) # | pg.DOUBLEBUF | pg.HWSURFACE)
	else:
		screen = pg.display.set_mode((screenW,screenH),pg.FULLSCREEN) # | pg.DOUBLEBUF | pg.HWSURFACE)
else:
	if fullscreenRes:
		pg.display.set_mode((screeninfo.current_w,screeninfo.current_h))
	else:
		screen = pg.display.set_mode((screenW, screenH)) 

flipflopSpace = True
font = pg.font.Font('freesansbold.ttf', fontSize)

pipepic = pg.image.load(resPath+'pipe.bmp')
pipepic = pg.transform.scale(pipepic, (pipeW,pipeH))
pipe_upsidedown_pic = pg.transform.rotate(pipepic,180)


playerW = playerSize
playerH = int(playerSize/1.3)

ripW = playerW + 2
ripH = playerH + 24

birdPic = pg.transform.scale(pg.image.load(resPath+'Bird.bmp'), (playerW,playerH))
#birdPicUp = pg.transform.rotate(birdPic,20)
#birdPicDown = pg.transform.rotate(birdPic,-20)

birdPicW = pg.transform.scale(pg.image.load(resPath+'Bird2.bmp'), (playerW,playerH))
#birdPicUpW = pg.transform.rotate(birdPic,20)
#birdPicDownW = pg.transform.rotate(birdPic,-20)


player = Player(playerX, screenW-borderThickness-playerW ,playerW,playerH)

backgroundPic = pg.transform.scale(pg.image.load(resPath+'Background.bmp'), (screenW,screenH))

planePic = pg.transform.scale(pg.image.load(resPath+'BannerPlane.bmp'), (planePicW,planePicH))


groundPic = pg.transform.scale(pg.image.load(resPath+'Ground.bmp'), (groundSize,int(groundSize*0.3)))
groundPicH = groundPic.get_height()
groundPicW = groundPic.get_width()

gameOverLabel = font.render("Game Over" , True, fontC)
gameOverLabelX = screenW/2-gameOverLabel.get_width()/2
gameOverLabelY = screenH/2-gameOverLabel.get_height()/2

ripPic = pg.image.load(resPath+'RIP.bmp')
ripPic = pg.transform.scale(ripPic, (ripW,ripH))
deadCrossPic = pg.transform.scale(pg.image.load(resPath+'DeadCross.bmp'), (deathCrossSize,deathCrossSize))
auaPic = pg.transform.scale(pg.image.load(resPath+'Aua.bmp'), (auaW,auaH))
skelettPic = pg.transform.scale(pg.image.load(resPath+'BirdSkelett.bmp'), (playerW,playerH))
tapPicW = int(screenW/5)
tapPicH = int(screenH/4)
tapPic = pg.transform.scale(pg.image.load(resPath+'TapToStart.bmp'), (tapPicW,tapPicH))



flap = pg.mixer.Sound(resPath+'Wing.ogg')
#die = pg.mixer.Sound('DieSound.wav')
hit = pg.mixer.Sound(resPath+'Hit.ogg')
point = pg.mixer.Sound(resPath+'Point.ogg')

pg.mixer.music.load(resPath+"Music.ogg")
pg.mixer.music.play(-1)

mKeyD = True
newColumnY = 380

while work:
	columnProtection = gapBetweenPipes
	playerpos = {'x1':playerX,'y1':screenH-playerH-borderThickness}
	gameRun = True
	gates = []
	score = 0
	scoreLabel = font.render(str(score) , True, fontC)
	scoreLabelY = screenH/2-scoreLabel.get_height()/2-screenH/4

	showGameOver = 0
	pg.mouse.set_visible(False)
	groundX = 0
	backgroundX = 0
	player.dead = False
	player.deathTime = 0
	speed = flySpeed
	player.y2=screenH/2+player.h/2-2
	player.y1 = screenH/2-player.h/2-2
	player.gravityStrength = 0
	startRun = True

	planeX = 0
	scoreLabelX = -2*planePicW/3-10
	player.deadX = 0
	player.deadY = 0
	sinX = 0
	while startRun:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				work = False
				gameRun = False

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					if not player.dead:
						player.gravityStrength = -12
						flap.play()
					startRun = False
				if event.key == pg.K_d:
					if not player.dead:
						player.gravityStrength = -12
						flap.play()
					startRun = False
				if event.key == pg.K_ESCAPE:
					work = False
					gameRun = False
					startRun = False

		#if player.y2 < screenH-borderThickness-2:
		#	player.gravityStrength += 1.1
		if playerStartMoveMode == 1:
			sinX += 1*clock.get_fps()/60

			playerY = int(4*math.sin(sinX*0.1))
			player.y2+=playerY
			player.y1+=playerY
		elif playerStartMoveMode == 2:
			player.gravityStrength += 1
			if player.y2 > screenH*0.6:
				player.gravityStrength = -14
		else:
			pass
		player.move()


		groundX -=speed
		if groundX == -50*groundPicW:
			groundX = 0

		backgroundX -= speed/2
		if backgroundX == -20*screenW:
			backgroundX = 0

		#show
		for x in range(int(backgroundX),screenW,screenW):
			screen.blit(backgroundPic,(x,-borderThickness+4))

		for x in range(int(groundX),screenW,groundPicW):
			screen.blit(groundPic,(x,screenH-borderThickness))

		player.show()

		screen.blit(tapPic,(int(screenW/2-tapPicW/2),int(screenH/2)))#-tapPicH/2))

		pg.display.flip()

		clock.tick(fps)

	############################################################################
	while gameRun:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				work = False
				gameRun = False

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE or event.key == pg.K_d: #or event.key == pg.K_a:
					if not player.dead:
						player.gravityStrength = flapForce
						flap.play()
				if event.key == pg.K_ESCAPE:
					work = False
					gameRun = False

		if player.y2 < screenH-borderThickness-2:
			player.gravityStrength += gravityForce

		player.move()
		if player.dead:
			player.deathTime += 1

		groundX -= speed
		if groundX == -5*groundPicW:
			groundX = 0
		backgroundX -= speed/2
		if backgroundX == -20*screenW:
			backgroundX = 0

		if columnProtection <= 0:
			#if newColumnY > 40:
			#	newColumnY -= 40
			#else:
			#	newColumnY = 380
			newColumnY = r.randrange(0+int(gateH/2),screenH-int(gateH/2)-borderThickness)
			gates.append(Gate(newColumnY))
			columnProtection = gapBetweenPipes

		columnProtection -= speed*clock.get_fps()/60


		delGates = []

		for gate in gates:
			gate.move()

			if gate.x2 < player.x1 and gate.scored == False:
				score += 1
				scoreLabel = font.render(str(score) , True, fontC)
				scoreLabelY = screenH/2-scoreLabel.get_height()/2-screenH/4
				point.play()
				gate.scored = True

			# check if player should die
			elif player.deadX == 0:
				if player.y2 > screenH-borderThickness or (
					player.x2-10 > gate.x1 and 
					player.x1+10 < gate.x2 and 
					(player.y2-5 > gate.y2 or player.y1+5 < gate.y1)): # check if player position is valid	
					
					hit.play()
					player.deadX = player.x1+player.w/2 - deathCrossSize/2
					player.deadY = player.y1+player.h/2 - deathCrossSize/2
					showGameOver = deathTime

			if gate.x2 < 0:
				delGates.append(gate)

		for gate in delGates:
			gates.pop(gates.index(gate))
			delGates.pop(delGates.index(gate))

		if player.deathTime > deathTime:
			print("Game Over! Score: {}".format(score))
			gameRun = False
		#show

		screen.fill((0,0,0))

		for x in range(int(backgroundX),screenW,screenW):
			screen.blit(backgroundPic,(x,-borderThickness+4))

		if planeX < screenW/2-(planePicW/3)+planePicW:
			planeX += speed*clock.get_fps()/60
		if scoreLabelX < screenW/2-scoreLabel.get_width()/2 or player.dead:
			scoreLabelX += speed*clock.get_fps()/60

		if player.dead:
			scoreLabelX += 4
			planeX += 4


		screen.blit(planePic,(planeX-planePicW,screenH/2-planePicH/2-screenH/4))
		screen.blit(scoreLabel,(scoreLabelX,scoreLabelY))

		if showGameOver > 0:
			screen.blit(gameOverLabel,(gameOverLabelX,gameOverLabelY))
			showGameOver -= 1
			player.dead = True
			speed = 0

			#gameRun = False
		for gate in gates:
			gate.show()

		for x in range(int(groundX),screenW,groundPicW):
			screen.blit(groundPic,(x,screenH-borderThickness))
		player.show()

		pg.display.flip()

		clock.tick(fps)


print("Program ended")
