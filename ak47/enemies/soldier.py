#!/usr/bin/python
import sys
import pygame
import random
from pygame.locals import *
sys.path.append("..")
from enemy import *

class Soldier(Enemy):
    def __init__(self, scale, scr, clk, fx):
	Enemy.__init__(self, scale, scr, clk, fx)
	self.frames = [pygame.image.load('gfx/soldier1.png').convert_alpha(), 
	pygame.image.load('gfx/soldier2.png').convert_alpha(),
	pygame.image.load('gfx/soldier3.png').convert_alpha(), 
	pygame.image.load('gfx/soldier2.png').convert_alpha(),
	pygame.image.load('gfx/soldier4.png').convert_alpha(),
	pygame.image.load('gfx/soldier5.png').convert_alpha()] 
	self.helix = pygame.Rect(0, 0, self.frames[0].get_width(), self.frames[0].get_height())
	for frame in self.frames:
		frame = self.scaleBitmap(frame, self.gfxscale)
	self.hitPoints = 1
	self.points = 50
	self.resetPos()
	self.framenum = 0
	self.frameTime = 0
	self.shootingStarted = 0
	self.timeOfDeath = 0

    def resetPos(self):
	if(random.random() > 0.5):
		self.xspeed = float(random.randint(10,15))
		self.helix.left=-self.frames[0].get_width()*self.gfxscale * 5
		self.heli = self.frames[0]
	else:
		self.xspeed = float(random.randint(-15,-10))
		self.helix.left=self.screen.get_width() + self.frames[0].get_width()*self.gfxscale * 5
		self.heli = pygame.transform.flip(self.frames[0], True, False)
	self.yspeed = float(random.randint(-3,3))

	self.firingPos = random.randint(self.screen.get_width()/3,self.screen.get_width()/3+self.screen.get_width()/3) 
	self.helix.top = random.randint(self.screen.get_height()/2,self.screen.get_height()/2+self.screen.get_height()/3) * self.gfxscale
	self.xpos = float(self.helix.left)
	self.ypos = float(self.helix.top)

    def tick(self):
	Enemy.tick(self)
	if self.xspeed != 0:
		self.lastMovementX = self.xspeed
	if self.yspeed != 0:
		self.lastMovementY = self.yspeed

	self.xpos += (self.xspeed * float(self.clock.get_time())) / 100.0
	self.ypos += (self.yspeed * float(self.clock.get_time())) / 100.0
	self.helix.left = self.xpos
	self.helix.top = self.ypos
	if(self.helix.top < self.screen.get_height()/2):
		self.yspeed = abs(self.yspeed)
	if(self.helix.bottom > self.screen.get_height()):
		self.yspeed = -abs(self.yspeed)

	if (self.xspeed > 0 and self.helix.left > self.screen.get_width()) or (self.xspeed < 0 and self.helix.left + self.heli.get_width() < 0):
		self.resetPos()
	frame = self.frames[self.framenum]

	currtime = pygame.time.get_ticks()

	if self.shootingStarted > 0: 
		frame = self.frames[4]
		if self.shootingStarted < currtime - 400 and self.timeOfDeath == 0 and self.gunFired==False:
			self.fireGun()
		if self.shootingStarted < currtime - 500 and self.timeOfDeath == 0:
			self.shootingStarted = 0
			self.xspeed = float(random.randint(10,15))
			self.yspeed = float(random.randint(-3,3))

	if self.timeOfDeath > 0:
		frame = self.frames[5]
		if self.timeOfDeath < currtime - 2000:
			self.dead = True

	if self.lastMovementX > 0:
		frame = pygame.transform.flip(frame, True, False)

	self.screen.blit(frame, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None)

	if self.shootingStarted == 0 and random.randint(0,100)==42 and self.timeOfDeath == 0:
		self.shootingStarted = pygame.time.get_ticks()
		self.xspeed = 0
		self.yspeed = 0
		self.gunFired=False

	if self.frameTime < currtime -100:
		self.framenum += 1
		if self.framenum > 3:
			self.framenum = 0
		self.frameTime = currtime

    def shotFired(self, coords):
	Enemy.shotFired(self, coords)
	if self.helix.collidepoint(coords):
		self.hitPoints = self.hitPoints - 1
		if self.hitPoints == 0:
			self.heliDestroyed()

    def heliDestroyed(self):
	self.timeOfDeath = pygame.time.get_ticks()
	self.xspeed = 0
	self.yspeed = 0
	self.effects.playScream()

    def fireGun(self):
	self.effects.addExplosion(self.helix.center, 0.03)
	self.effects.playEnemyGun()
	self.gunFired=True
	if random.randint(0,10) < 3:
		self.damageInflicted = 5

    def getZ(self):
	return self.helix.bottom

