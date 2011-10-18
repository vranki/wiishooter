#!/usr/bin/python
import sys
import pygame
import random
from enemy import *
from pygame.locals import *

class Effects(Enemy):
    def __init__(self, scale, scr, clk):
	Enemy.__init__(self, scale, scr, clk, self)
	self.explosion = pygame.image.load('gfx/explosion.png').convert_alpha()
	self.explosion = self.scaleBitmap(self.explosion, self.gfxscale)
	self.explosion_s = pygame.image.load('gfx/explosion_start.png').convert_alpha()
	self.explosion_s = self.scaleBitmap(self.explosion_s, self.gfxscale)
	self.explosion_e = pygame.image.load('gfx/explosion_end.png').convert_alpha()
	self.explosion_e = self.scaleBitmap(self.explosion_e, self.gfxscale)
	self.pain = pygame.image.load('gfx/pain.png').convert_alpha()
	self.pain = self.scaleBitmap(self.pain, self.gfxscale)
	self.objects = []

	self.gunSound = pygame.mixer.Sound('sounds/gun.wav')
	self.explosionSound = pygame.mixer.Sound('sounds/explosion.wav')
	self.screamSounds = [ pygame.mixer.Sound('sounds/scream.ogg'), pygame.mixer.Sound('sounds/scream2.ogg')]
	self.reloadSound = pygame.mixer.Sound('sounds/reload.wav')
	self.painEndTime = 0

    def tick(self):
	Enemy.tick(self)
	curtime = pygame.time.get_ticks()
	for obj in self.objects:
		age = curtime - obj[2]
		idx = 0
		if age > obj[3] / 3:
			idx = idx + 1
		if age > obj[3] / 3 * 2:
			idx = idx + 1

		bmp = obj[1][idx]
		self.screen.blit(bmp, [obj[0][0] * self.gfxscale, obj[0][1] * self.gfxscale], None)
		if age > obj[3]:
			self.objects.remove(obj)
	if curtime < self.painEndTime:
		self.screen.blit(self.pain, [0,0], None)
		
    def addExplosion(self, pos, scale, time=500):
	bmp = []
	bmp.append(pygame.transform.rotozoom(self.explosion_s, 0, scale))
	bmp.append(pygame.transform.rotozoom(self.explosion, 0, scale))
	bmp.append(pygame.transform.rotozoom(self.explosion_e, 0, scale))
	pos = list(pos)
	pos[0] = pos[0] - bmp[0].get_width() / 2
	pos[1] = pos[1] - bmp[0].get_height() / 2
	self.objects.append([pos, bmp, pygame.time.get_ticks(), time])

    def playGun(self):
	self.gunSound.play()

    def playEnemyGun(self):
	self.gunSound.play()

    def playExplosion(self):
	self.explosionSound.play()

    def playReload(self):
	self.reloadSound.play()

    def playScream(self):
	self.screamSounds[random.randint(0,len(self.screamSounds)-1)].play()

    def showPain(self, time):
	self.painEndTime = pygame.time.get_ticks() + time

