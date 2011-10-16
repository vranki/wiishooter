#!/usr/bin/python
import sys
import pygame
import time
import gamelogic
import ak47
from pygame.locals import *
import menusystem
 
def main():
        pygame.init()
        pygame.mixer.init()
 	gun = None
        print 'Put ak47 in discoverable mode now (press connection button)...'
    	myAK = ak47.Ak47()
    	myAK.load_calibration("full_screen_calib.txt")
        print 'OK'
 
        # Set the height and width of the screen
        size=[1000,700]
	# for native size
       	# size=[0,0]
        screen=pygame.display.set_mode(size, FULLSCREEN)
 
        pygame.display.set_caption("WiiShooter")
 
        # Used to manage how fast the screen updates
        clock=pygame.time.Clock()

	game = gamelogic.GameLogic()
	game.init(screen, clock)

	textArea = menusystem.textarea(size)
	highScores = menusystem.highscores()
	highScores.reload_scores(False)
	appendScore = menusystem.appendscore()
	welcomeScreen = menusystem.welcome()

	gameState = 'welcome'

	trigTime = time.time()
        exit = False
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
                	myAK.fire(True)
			game.shotFired(gun_pos)

        	if time.time() - trigTime > 0.05:
            		myAK.fire(False)
 
        	# Limit to 60 frames per second
        	clock.tick(60)

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

        	# Go ahead and update the screen with what we've drawn.
         	pygame.display.update()

        pygame.quit ()
	if gun is not None:
	        gun.close()
 
main()
