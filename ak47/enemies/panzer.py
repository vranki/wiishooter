#!/usr/bin/python
import sys
import pygame
import random
from pygame.locals import *
sys.path.append("..")
from enemy import *

class Panzer(Enemy):
    def __init__(self, scale, scr, clk, fx):
	Enemy.__init__(self, scale, scr, clk, fx)
	self.heli_orig = pygame.image.load('gfx/panzer.png').convert_alpha()
	self.helix = pygame.Rect(0, 0, self.heli_orig.get_width(), self.heli_orig.get_height())
	self.heli_orig = self.scaleBitmap(self.heli_orig, self.gfxscale)
	self.hitPoints = 15
	self.points = 500
	self.resetPos()

    def resetPos(self):
	if(random.random() > 0.5):
		self.xspeed = float(random.randint(3,10))
		self.helix.left=-self.heli_orig.get_width()*self.gfxscale * 5
		self.heli = self.heli_orig
	else:
		self.xspeed = float(random.randint(-10,-3))
		self.helix.left=self.screen.get_width() + self.heli_orig.get_width()*self.gfxscale * 5
		self.heli = pygame.transform.flip(self.heli_orig, True, False)

	self.firingPos = random.randint(self.screen.get_width()/3,self.screen.get_width()/3+self.screen.get_width()/3) 
	self.helix.top = random.randint(self.screen.get_height()/2,self.screen.get_height()/2+self.screen.get_height()/3) * self.gfxscale
	self.xpos = float(self.helix.left)

    def tick(self):
	Enemy.tick(self)
	self.xpos += (self.xspeed * float(self.clock.get_time())) / 100.0
	self.helix.left = self.xpos
	if (self.xspeed > 0 and self.helix.left > self.screen.get_width()) or (self.xspeed < 0 and self.helix.left + self.heli.get_width() < 0):
		self.resetPos()
	self.screen.blit(self.heli, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None)
	if self.firingPos is not None and abs(self.helix.left - self.firingPos) < 10:
		self.fireGun()
		self.firingPos = None

    def shotFired(self, coords):
	Enemy.shotFired(self, coords)
	if self.helix.collidepoint(coords):
		self.hitPoints = self.hitPoints - 1
		if self.hitPoints == 0:
			self.heliDestroyed()

    def heliDestroyed(self):
	self.effects.addExplosion(self.helix.center, 1)
	self.effects.playExplosion()
	self.dead = True
	self.helix.left=-self.heli.get_width()*self.gfxscale * 5

    def fireGun(self):
	self.effects.addExplosion([self.helix.center[0] - 20*self.gfxscale,self.helix.center[1] - 80*self.gfxscale] , 0.3)		
	self.effects.playExplosion()
	self.damageInflicted = 30

