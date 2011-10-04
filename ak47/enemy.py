#!/usr/bin/python
import pygame
from pygame.locals import *

class Enemy:
    def __init__(self, scale, scr, clk, fx):
	self.gfxscale = scale
	self.screen = scr
	self.clock = clk
	self.effects = fx
	self.dead = False
	self.hitPoints = 1
	self.damageInflicted = 0

    def scaleBitmap(self, sf, scale):
	return pygame.transform.smoothscale(sf, (int(sf.get_width() * scale), int(sf.get_height() * scale)))

    def tick(self):
	pass

    def shotFired(self, coords):
	pass

    def isDead(self):
	return self.dead

    def getDamageInflicted(self):
	di = self.damageInflicted
	self.damageInflicted = 0
	return di

