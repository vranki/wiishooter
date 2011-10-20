#!/usr/bin/python
import sys
import pygame
import random
from pygame.locals import *
sys.path.append("..")
from enemy import *

class Medikit(Enemy):
    def __init__(self, scale, scr, clk, fx):
	Enemy.__init__(self, scale, scr, clk, fx)
	self.heli_orig = pygame.image.load('gfx/medikit.png').convert_alpha()
	self.helix = pygame.Rect(0, 0, self.heli_orig.get_width(), self.heli_orig.get_height())
	self.heli = self.scaleBitmap(self.heli_orig, self.gfxscale)
	self.hitPoints = 1
	self.points = 0
	self.resetPos()

    def resetPos(self):
	self.helix.left = random.randint(0,self.screen.get_width())
	self.helix.top = 0

    def tick(self):
	Enemy.tick(self)
	self.helix.top += (2*float(self.clock.get_time())) / 10.0
	if self.helix.top > self.screen.get_height():
		self.dead = True
	self.screen.blit(self.heli, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None)

    def shotFired(self, coords):
	Enemy.shotFired(self, coords)
	if self.helix.collidepoint(coords):
		self.hitPoints = self.hitPoints - 1
		if self.hitPoints == 0:
			self.heliDestroyed()

    def heliDestroyed(self):
	self.dead = True
	self.damageInflicted = -30

    def getZ(self):
	return self.helix.bottom

