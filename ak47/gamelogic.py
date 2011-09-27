#!/usr/bin/python
import sys
import pygame
from enemy import *
sys.path.append("enemies")
from helicopter import *
from pygame.locals import *
from effects import *

class GameLogic:
    def __init__(self):
	self.bg = pygame.image.load('gfx/background.png').convert_alpha()
	self.gfxscale = 1.0
	self.enemies = []
	self.lastEnemyAddedTime = pygame.time.get_ticks()
	self.enemyAddInterval = 10000

    def scaleBitmap(self, sf, scale):
	return pygame.transform.smoothscale(sf, (int(sf.get_width() * scale), int(sf.get_height() * scale)))

    def init(self, scr, clk):
	self.screen = scr
	self.clock = clk
	self.gfxscale = float(self.screen.get_width()) / 1360.0
	self.bg = self.scaleBitmap(self.bg, self.gfxscale)
	self.effects = Effects(self.gfxscale, self.screen, self.clock)
	self.addRandomEnemy()

    def tick(self):
	curtime = pygame.time.get_ticks()
	self.screen.blit(self.bg, (0,0))
	for enemy in self.enemies:
		enemy.tick()
		if enemy.isDead():
			self.enemies.remove(enemy)
	self.effects.tick()
	if curtime - self.lastEnemyAddedTime > self.enemyAddInterval:
		self.addRandomEnemy()

    def shotFired(self, coords):
	scaledCoords = list(coords)
	scaledCoords[0] /= self.gfxscale
	scaledCoords[1] /= self.gfxscale
	self.effects.addExplosion(scaledCoords, 0.1, 100)
	for enemy in self.enemies:
		enemy.shotFired(scaledCoords)

    def addRandomEnemy(self):
	heli = Helicopter(self.gfxscale, self.screen, self.clock, self.effects)
	self.enemies.append(heli)
	if self.enemyAddInterval > 1000:
		self.enemyAddInterval = self.enemyAddInterval - 500
	self.lastEnemyAddedTime = pygame.time.get_ticks()
	
    def close(self):
	pass

