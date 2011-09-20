#!/usr/bin/python
import sys
import pygame
from pygame.locals import *

class GameLogic:
    def __init__(self):
	self.bg = pygame.image.load('gfx/background.png').convert()
	self.heli = pygame.image.load('gfx/helicopter.png').convert()
	self.helix = 0.0	

    def init(self, scr, clk):
	self.screen = scr
	self.clock = clk

    def tick(self):
    	# Set the screen background
	self.helix += float(self.clock.get_time()) / 5
	if self.helix > self.screen.get_width():
		self.helix = 0.0
	self.screen.blit(self.bg, (0,0))
	self.screen.blit(self.heli, ( self.helix,50), None, BLEND_RGBA_MULT)

    def close(self):
	pass

