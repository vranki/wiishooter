#!/usr/bin/python
import sys
import pygame
import ak47
from pygame.locals import *

def drawCalibrationStuff(screen, calibrationPhase):
        if(calibrationPhase > 3):
                return
 
        font = pygame.font.Font(None, 25)
        if(calibrationPhase==0):
                text = font.render("Shoot top left",True,(0,0,0))
                targetPos = [0,0]
        if(calibrationPhase==1):
                text = font.render("Shoot bottom left",True,(0,0,0))
                targetPos = [0,screen.get_height()]
        if(calibrationPhase==2):
                text = font.render("Shoot top right",True,(0,0,0))

                targetPos = [screen.get_width(), 0]
        if(calibrationPhase==3):
                text = font.render("Shoot bottom right",True,(0,0,0))
                targetPos = [screen.get_width(), screen.get_height()]

        screen.blit(text, [250,250])
        drawCrosshairs(screen, (128,0,0), targetPos)

 
def drawCrosshairs(screen, color, pos):
        pygame.draw.line(screen,color,[pos[0] - 30, pos[1]],[pos[0]+30, pos[1]],1)
        pygame.draw.line(screen,color,[pos[0], pos[1] - 30],[pos[0], pos[1] + 30],1)
        pygame.draw.circle(screen, color, pos, 20, 1)
        pygame.draw.circle(screen, color, pos, 5, 1)
 
def main():
        pygame.init()
        pygame.mixer.init()
 
        #gunSound = pygame.mixer.Sound('gun.wav')
        #Connect to address given on command-line, if present
        print 'Put ak47 in discoverable mode now (press connection button)...'
	gun = ak47.Ak47()
        print 'OK'
 
        # Set the height and width of the screen
        size=[1024,768]
        screen=pygame.display.set_mode(size)
 
        pygame.display.set_caption("PYSSYTESTI")
 
        # Used to manage how fast the screen updates
        clock=pygame.time.Clock()
 
        gun_pos = [500,500]
	calib_index = 0
	old_trigger = False       

        exit = False
        while not exit:
                for event in pygame.event.get(): # User did something
                        if event.type == pygame.QUIT: # If user clicked close
                                exit=True # Flag that we are done so we exit this loop
			if event.type == pygame.KEYDOWN:
				exit=True

		gun_pos, trigger = gun.get_pos()
		gun_pos[0] *= gun_pos[0]
		gun_pos[1] *= gun_pos[1]


                 # Set the screen background
        	screen.fill((255,255,255))
 
        	drawCrosshairs(screen, (0,0,0), gun_pos)

		if trigger and not old_trigger:
			calib_index += 1
			
		old_trigger = trigger

        	drawCalibrationStuff(screen, calib_index)
 
        	# Limit to 60 frames per second
        	clock.tick(60)
 
        	# Go ahead and update the screen with what we've drawn.
        	pygame.display.flip()
 
        pygame.quit ()
        gun.close()
 
main()
