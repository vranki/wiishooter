#!/usr/bin/python
import sys
import pygame
from pygame.locals import *
sys.path.append("..")
from enemy import *

class Helicopter(Enemy):
    def __init__(self, scale, scr, clk, fx):
	Enemy.__init__(self, scale, scr, clk, fx)
	self.heli = pygame.image.load('gfx/helicopter.png').convert_alpha()
	self.helix = pygame.Rect(0, 0, self.heli.get_width(), self.heli.get_height())
	self.heli = self.scaleBitmap(self.heli, self.gfxscale)
	self.helix.left=-self.heli.get_width()*self.gfxscale * 5

    def tick(self):
	Enemy.tick(self)
    	# Set the screen background
	self.helix.left += float(self.clock.get_time()) / 5
	if self.helix.left > 1360:
		self.helix.left = 0.0
	self.screen.blit(self.heli, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None)

    def shotFired(self, coords):
	Enemy.shotFired(self, coords)
	if self.helix.collidepoint(coords):
		self.heliDestroyed()

    def heliDestroyed(self):
	print str(self.helix)
	self.effects.addExplosion(self.helix.center, 1)
	self.helix.left=-self.heli.get_width()*self.gfxscale * 5

