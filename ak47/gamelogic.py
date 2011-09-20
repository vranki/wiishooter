#!/usr/bin/python
import sys
import pygame
from pygame.locals import *

class GameLogic:
    def __init__(self):
	self.bg = pygame.image.load('gfx/background.png').convert()
	self.heli = pygame.image.load('gfx/helicopter.png').convert()
	self.helix = 0.0	

    def scaleBitmap(self, sf, scale):
	return pygame.transform.smoothscale(sf, (int(sf.get_width() * scale), int(sf.get_height() * scale)))

    def init(self, scr, clk):
	self.screen = scr
	self.clock = clk
	gfxscale = float(self.screen.get_width()) / 1360.0
	self.bg = self.scaleBitmap(self.bg, gfxscale)
	self.heli = self.scaleBitmap(self.heli, gfxscale)

    def tick(self):
    	# Set the screen background
	self.helix += float(self.clock.get_time()) / 5
	if self.helix > self.screen.get_width():
		self.helix = 0.0
	self.screen.blit(self.bg, (0,0))
	self.screen.blit(self.heli, ( self.helix,self.screen.get_height()/20), None, BLEND_RGBA_MULT)

    def close(self):
	pass

