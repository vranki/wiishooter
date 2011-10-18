#!/usr/bin/python
import sys
import pygame
from operator import itemgetter
from enemy import *
sys.path.append("enemies")
from helicopter import *
from panzer import *
from soldier import *
from barrel import *
from pygame.locals import *
from effects import *

class GameLogic:
    def __init__(self):
	self.bg = pygame.image.load('gfx/background.png').convert_alpha()
	self.reloadImage = pygame.image.load('gfx/reload.png').convert_alpha()
	self.gfxscale = 1.0
	self.lastEnemyAddedTime = pygame.time.get_ticks()
	self.enemyAddInterval = 3000
	self.font = pygame.font.Font(None, 25)
	self.gameEnded = True

    def scaleBitmap(self, sf, scale):
	return pygame.transform.smoothscale(sf, (int(sf.get_width() * scale), int(sf.get_height() * scale)))

    def init(self, scr, clk):
	self.screen = scr
	self.clock = clk
	self.gfxscale = float(self.screen.get_width()) / 1360.0
	self.bg = self.scaleBitmap(self.bg, self.gfxscale)
	self.effects = Effects(self.gfxscale, self.screen, self.clock)
    	self.initNewGame()

    def tick(self):
	curtime = pygame.time.get_ticks()
	self.screen.blit(self.bg, (0,0))

	if self.gameEnded:
		return self.gameEnded, self.score

	zs = []
	for enemy in self.enemies:
		zs.append([enemy.getZ(), enemy])

	sortedEnemies = sorted(zs, key=itemgetter(0), reverse=False)
	for enemyPair in sortedEnemies:
		enemy = enemyPair[1]
		enemy.tick()
		di = enemy.getDamageInflicted()
		if di > 0:
			self.health -= di
			self.updateHealth()
			if self.health <= 0:
				self.playerDied()
		if enemy.isDead():
			self.score += enemy.getPoints()
			self.updateScore()
			self.enemies.remove(enemy)

	self.effects.tick()
	if curtime - self.lastEnemyAddedTime > self.enemyAddInterval:
		self.addRandomEnemy()

	if self.health==0:
		self.enemies = []
		self.gameEnded = True

	if self.health > 0 and self.ammo == 0:
		self.screen.blit(self.reloadImage, (self.screen.get_width()/2 - self.reloadImage.get_width()/2,self.screen.get_height()/2 - self.reloadImage.get_height()/2))
	self.screen.blit(self.healthText, [10,10])
	self.screen.blit(self.scoreText, [10,40])

        return self.gameEnded, self.score


    def updateHealth(self):
	if self.health != 0:
		self.healthText = self.font.render("Health " + str(self.health),True,(0,0,0))
	else:
		self.healthText = self.font.render("MERTVYI",True,(0,0,0))

    def updateScore(self):
	self.scoreText = self.font.render("Score " + str(self.score),True,(0,0,0))

# coords must be physical, unscaled pixels
    def shotFired(self, coords):
	if self.health == 0:
		return
	if self.ammo <= 0:
		return
	scaledCoords = list(coords)
	scaledCoords[0] /= self.gfxscale
	scaledCoords[1] /= self.gfxscale
	self.effects.addExplosion(scaledCoords, 0.1, 100)
	self.effects.playGun()
	for enemy in self.enemies:
		enemy.shotFired(scaledCoords)
	self.ammo -= 1
	if self.ammo == 0:
		print "Reload!!"

    def addRandomEnemy(self):
	enemyType = random.randint(0,100)
#	enemyType = 2
	if enemyType < 10:
		enemy = Panzer(self.gfxscale, self.screen, self.clock, self.effects)
	elif enemyType < 20:
		enemy = Helicopter(self.gfxscale, self.screen, self.clock, self.effects)
	else:
		enemy = Soldier(self.gfxscale, self.screen, self.clock, self.effects)

	self.enemies.append(enemy)
	if self.enemyAddInterval > 1000:
		self.enemyAddInterval = self.enemyAddInterval - 500
	self.lastEnemyAddedTime = pygame.time.get_ticks()
	
    def close(self):
	pass

    def initNewGame(self):
	self.gameEnded = False
	self.health = 100
	self.score = 0
	self.ammo = 30
	self.updateHealth()
	self.updateScore()
	self.enemies = []
	for i in range(0,5): 
		self.addRandomEnemy()
		self.enemies.append(Barrel(self.gfxscale, self.screen, self.clock, self.effects))
	self.screen.fill([0,0,0])
	self.deathTime = 0

    def playerDied(self):
	if self.health < 0:
		self.health = 0
	if self.deathTime == 0:
		self.deathTime = pygame.time.get_ticks()
	self.enemies = []
	self.updateHealth()

    def reloading(self, r):
	if r:
		if self.ammo < 30:
			self.effects.playReload()
		self.ammo = 30

    def gunCanFire(self):
	return self.ammo > 0 and self.health > 0

