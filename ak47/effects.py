#!/usr/bin/python
import sys
import pygame
from enemy import *
from pygame.locals import *

class Effects(Enemy):
    def __init__(self, scale, scr, clk):
	Enemy.__init__(self, scale, scr, clk, self)
	self.explosion = pygame.image.load('gfx/explosion.png').convert_alpha()
	self.explosion = self.scaleBitmap(self.explosion, self.gfxscale)
	self.objects = []

    def tick(self):
	Enemy.tick(self)
	curtime = pygame.time.get_ticks()
	for obj in self.objects:
		self.screen.blit(obj[1], [obj[0][0] * self.gfxscale, obj[0][1] * self.gfxscale], None)
		age = curtime - obj[2]
		if age > 0:
			self.objects.remove(obj)
		
    def addExplosion(self, pos, scale, time=1000):
	bmp = pygame.transform.rotozoom(self.explosion, 0, scale)
	pos = list(pos)
	pos[0] = pos[0] - bmp.get_width() / 2
	pos[1] = pos[1] - bmp.get_height() / 2

	self.objects.append([pos, bmp, pygame.time.get_ticks() + time])

