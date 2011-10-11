#!/usr/bin/python
import sys
import pygame
import random
from pygame.locals import *
sys.path.append("..")
from enemy import *

class Helicopter(Enemy):
    def __init__(self, scale, scr, clk, fx):
	Enemy.__init__(self, scale, scr, clk, fx)
	self.heli_orig = pygame.image.load('gfx/helicopter.png').convert_alpha()
	self.helix = pygame.Rect(0, 0, self.heli_orig.get_width(), self.heli_orig.get_height())
	self.heli_orig = self.scaleBitmap(self.heli_orig, self.gfxscale)
	self.hitPoints = 10
	self.points = 500
	self.resetPos()

    def resetPos(self):
	if(random.random() > 0.5):
		self.xspeed = random.randint(10,100)
		self.helix.left=-self.heli_orig.get_width()*self.gfxscale * 5
		self.heli = self.heli_orig
	else:
		self.xspeed = random.randint(-100,-10)
		self.helix.left=self.screen.get_width() + self.heli_orig.get_width()*self.gfxscale * 5
		self.heli = pygame.transform.flip(self.heli_orig, True, False)

	self.helix.top = random.randint(0,self.screen.get_height()/2) * self.gfxscale

    def tick(self):
	Enemy.tick(self)
	self.helix.left += (self.xspeed * float(self.clock.get_time())) / 100.0
	if (self.xspeed > 0 and self.helix.left > self.screen.get_width()) or (self.xspeed < 0 and self.helix.left + self.heli.get_width() < 0):
		self.resetPos()
	self.screen.blit(self.heli, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None)

    def shotFired(self, coords):
	Enemy.shotFired(self, coords)
	if self.helix.collidepoint(coords):
		self.hitPoints = self.hitPoints - 1
		if self.hitPoints == 0:
			self.heliDestroyed()

    def heliDestroyed(self):
	self.effects.addExplosion(self.helix.center, 1)
	self.dead = True
	self.helix.left=-self.heli.get_width()*self.gfxscale * 5
	self.effects.playExplosion()

    def getZ(self):
	return self.helix.bottom


