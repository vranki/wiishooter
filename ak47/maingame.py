#!/usr/bin/python
import sys
import pygame
import time
import gamelogic
from ak47 import Ak47
from ak47mouse import Ak47Mouse
from ak47wiimote import Ak47Wiimote
from pygame.locals import *
import menusystem
 
def main():
        pygame.init()
        pygame.mixer.init()
 	gun = None
	fullscreen = False
	myAK = None
	# PARAMS: wiimote (use wiimote) fullscreen (guess)
	for param in sys.argv:
		if param == 'wiimote':
		        print 'Put ak47 in discoverable mode now (press connection button)...'
    			myAK = Ak47Wiimote()
    			myAK.load_calibration("full_screen_calib.txt")
        		print 'OK'
 		if param == 'fullscreen':
			fullscreen = True

	size=[0,0]
	if fullscreen:
	        screen=pygame.display.set_mode(size, FULLSCREEN)
	else:
	        # Set the height and width of the screen
        	size=[1360,764]
		# for native size
		screen=pygame.display.set_mode(size)
	if myAK is None:
		myAK = Ak47Mouse() 
        pygame.display.set_caption("WiiShooter")
 
        # Used to manage how fast the screen updates
        clock=pygame.time.Clock()

	game = gamelogic.GameLogic()
	game.init(screen, clock)

	textArea = menusystem.textarea([screen.get_width(), screen.get_height()])
	highScores = menusystem.highscores()
	highScores.reload_scores(False)
	appendScore = menusystem.appendscore()
	welcomeScreen = menusystem.welcome()

	gameState = 'welcome'

	trigTime = time.time()
        exit = False
	reloading = False
	myAK.fire(False)
        while not exit:
                for event in pygame.event.get(): # User did something
                        if event.type == pygame.QUIT: # If user clicked close
                                exit=True # Flag that we are done so we exit this loop
			if event.type == pygame.KEYDOWN:
				exit=True
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pass

		gun_pos, trigger = myAK.get_pos()
		if trigger and time.time() - trigTime > 0.12:
			trigTime = time.time()
#			if game.gunCanFire():
			myAK.fire(True)
			game.shotFired(gun_pos)

		if time.time() - trigTime > 0.05:
	    		myAK.fire(False)

		newReloading = myAK.reload_ak()
		if reloading is not newReloading:
			reloading = newReloading
			game.reloading(reloading)
        	# Limit to 60 frames per second
        	clock.tick(30)

		gameEnded, score = game.tick() 

		cursor = [gun_pos[0], gun_pos[1], trigger]

		if gameState == 'play' and gameEnded:
			gameState = 'appendscore'
			appendScore.upload_highscore(score)

		elif gameState == 'appendscore':
			textArea.update(screen, cursor)
			gameState = appendScore.update(screen, cursor)
			if gameState == 'highscores':
				highScores.reload_scores(True, appendScore.score_pos())

		elif gameState == 'highscores':
			textArea.update(screen, cursor)
			gameState = highScores.update(screen, cursor)
			if gameState == 'play':
				game.initNewGame()

		elif gameState == 'welcome':
			textArea.update(screen, cursor)
			gameState = welcomeScreen.update(screen, cursor)
			if gameState == 'play':
				game.initNewGame()

		if gameState != 'play':
			pygame.draw.circle(screen, (255,0,0), gun_pos, 5, 0) 


        	# Go ahead and update the screen with what we've drawn.
         	pygame.display.update()

        pygame.quit ()
	if gun is not None:
	        gun.close()
 
main()
