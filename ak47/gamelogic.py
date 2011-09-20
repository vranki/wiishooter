#!/usr/bin/python
import sys
import pygame
from pygame.locals import *

class GameLogic:
    def __init__(self):
	self.bg = pygame.image.load('gfx/background.png').convert()
	self.heli = pygame.image.load('gfx/helicopter.png').convert()
	self.helix = pygame.Rect(0, 0, self.heli.get_width(), self.heli.get_height())
	self.gfxscale = 1.0

    def scaleBitmap(self, sf, scale):
	return pygame.transform.smoothscale(sf, (int(sf.get_width() * scale), int(sf.get_height() * scale)))

    def init(self, scr, clk):
	self.screen = scr
	self.clock = clk
	self.gfxscale = float(self.screen.get_width()) / 1360.0
	self.bg = self.scaleBitmap(self.bg, self.gfxscale)
	self.heli = self.scaleBitmap(self.heli, self.gfxscale)
	self.helix.left=-self.heli.get_width()*self.gfxscale * 5

    def tick(self):
    	# Set the screen background
	self.helix.left += float(self.clock.get_time()) / 5
	if self.helix.left > 1360:
		self.helix.left = 0.0
	self.screen.blit(self.bg, (0,0))
	self.screen.blit(self.heli, ( self.helix.left*self.gfxscale,self.helix.top*self.gfxscale), None, BLEND_RGBA_MULT)

    def shotFired(self, coords):
	scaledCoords = list(coords)
	scaledCoords[0] /= self.gfxscale
	scaledCoords[1] /= self.gfxscale
	if self.helix.collidepoint(scaledCoords):
		self.heliDestroyed()

    def heliDestroyed(self):
	self.helix.left=-self.heli.get_width()*self.gfxscale * 5

    def close(self):
	pass

