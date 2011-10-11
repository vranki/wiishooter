#!/usr/bin/python
import sys
import pygame
import random
from pygame.locals import *
sys.path.append("..")
from enemy import *

class Barrel(Enemy):
    def __init__(self, scale, scr, clk, fx):
	Enemy.__init__(self, scale, scr, clk, fx)
	self.heli_orig = pygame.image.load('gfx/barrel.png').convert_alpha()
	self.helix = pygame.Rect(0, 0, self.heli_orig.get_width(), self.heli_orig.get_height())
	self.heli = self.scaleBitmap(self.heli_orig, self.gfxscale)
	self.hitPoints = 2
	self.points = 1
	self.resetPos()

    def resetPos(self):
	self.helix.left = random.randint(0,self.screen.get_width())
	self.helix.top = random.randint(self.screen.get_height()/2, self.screen.get_height())

    def tick(self):
	Enemy.tick(self)
	self.screen.blit(self.heli, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None)

    def shotFired(self, coords):
	Enemy.shotFired(self, coords)
	if self.helix.collidepoint(coords):
		self.hitPoints = self.hitPoints - 1
		if self.hitPoints == 0:
			self.heliDestroyed()

    def heliDestroyed(self):
	self.effects.addExplosion(self.helix.center, 0.6)
	self.dead = True
	self.effects.playExplosion()

    def getZ(self):
	return self.helix.bottom

