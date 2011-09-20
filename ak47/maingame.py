#!/usr/bin/python
import sys
import pygame
import gamelogic
import ak47
from pygame.locals import *
 
def main():
        pygame.init()
        pygame.mixer.init()
 	gun = None
        #gunSound = pygame.mixer.Sound('gun.wav')
        print 'Put ak47 in discoverable mode now (press connection button)...'
#	gun = ak47.Ak47()
        print 'OK'
 
        # Set the height and width of the screen
        size=[1024,768]
        screen=pygame.display.set_mode(size)
 
        pygame.display.set_caption("WiiShooter")
 
        # Used to manage how fast the screen updates
        clock=pygame.time.Clock()

	game = gamelogic.GameLogic()
        exit = False
        while not exit:
                for event in pygame.event.get(): # User did something
                        if event.type == pygame.QUIT: # If user clicked close
                                exit=True # Flag that we are done so we exit this loop
			if event.type == pygame.KEYDOWN:
				exit=True
		if gun is not None:
			gun_pos, trigger = gun.get_pos()
			gun_pos[0] *= gun_pos[0]
			gun_pos[1] *= gun_pos[1]

                 # Set the screen background
        	screen.fill((255,255,255))
 
        	# Limit to 60 frames per second
        	clock.tick(60)
 
        	# Go ahead and update the screen with what we've drawn.
        	pygame.display.flip()
 
        pygame.quit ()
	if gun is not None:
	        gun.close()
 
main()
