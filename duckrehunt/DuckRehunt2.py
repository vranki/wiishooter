"""
Copyright 2011 Michael Bachmann

This program is distributed under the terms of the GNU
General Public License
"""

import pygame, random
pygame.init()

from DuckLib import *
import ak47_2
import time
import menusystem


def gamePlay():
    screen     = pygame.display.set_mode((640,480), pygame.FULLSCREEN)
    screen_dim = screen.get_rect()
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Duck Rehunt: Reckoning")
    myAK = ak47_2.Ak47()
    myAK.load_calibration("full_screen_calib.txt")
    pygame.mixer.init()
    pygame.mixer.Sound("Music.ogg").play(-1)
    
    background     = pygame.Surface(screen.get_size())
    background.blit(pygame.image.load("Background.gif"), (0,0))
    screen.blit(background, (0,0))
 
    foreground     = setPiece(pygame.image.load("Foreground.gif"), (0,301), 1 )
    setSprites     = pygame.sprite.LayeredUpdates( foreground )

    ################
    crosshair = pygame.sprite.Group(Crosshair(myAK))
                          
    keepGoing = True
    pause     = 0
    delay     = 60
    shotScore = 0
    score = 0

    timeLeft = 30
    
    global ducks

    myFont = pygame.font.Font(None, 40)
    
    scoreboard = myFont.render("Score: " + str(score), 1, (255,255,255))
    timeboard = myFont.render("Time left: " + str(int(timeLeft)), 1, (255,255,255))

    clock = pygame.time.Clock()

    killGame = False
    trigTime = time.time()

    game_state = "menu"
    menu_system = menusystem.menu()
    
    while keepGoing:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    keepGoing = False

            elif event.type == pygame.KEYDOWN:
                keepGoing = False

        gun_pos, trigger = myAK.get_pos()
        if trigger and time.time() - trigTime > 0.12:
                trigTime = time.time()
                myAK.fire(True)
                score -= 1
                gunshot.play()
                flash.add(Flash(myAK))
                pointCollide = [sprite for sprite in dSprites.sprites() if sprite.rect.collidepoint(gun_pos)]
                if pointCollide != []:
                    for sprite in pointCollide:
                        if not sprite.dog and not sprite.isDead:
                            sprite.isDead = True
                            sprite.pause = 0
                            if sprite.enemy:
                                shotScore -= 50
                            else:
                                shotScore += 5
                            sprite.setAnim()
                    shotScore *= len(pointCollide)
                    score += shotScore
                    shotScore = 0

        if time.time() - trigTime > 0.05:
            myAK.fire(False)
    
        #Garbage collection        
        pause+= 1
        if pause >= delay:
            dSprites.remove([sprite for sprite in dSprites.sprites() if sprite.rect.centery >= 500])

        dSprites.clear(screen, background)
        ###############
	if game_state != "play":
        	crosshair.clear(screen, background)
        flash.clear(screen, background)

        dSprites.update()
        ###############
	if game_state != "play":
        	crosshair.update()
        flash.update()
        
        dSprites.draw(screen)
        setSprites.draw(screen)


        if game_state == "init":
            score = 0
            timeLeft = 30
            screen.blit(background, (0,0))
            dSprites.add(Dog())
            game_state = "play"

        
        if timeLeft <= 0 and game_state == "play":
            dSprites.empty()
            menu_system.new_score(score)
            game_state = "menu"


        if game_state == "play":

            timeLeft -= 0.02
            timeboard = myFont.render("Time left: " + str(int(timeLeft)), 1, (255,255,255))
            scoreboard = myFont.render("Score: " + str(score), 1, (255,255,255))
        
            screen.blit(scoreboard, (440,410))
            screen.blit(timeboard, (240,410))

            if abs(timeLeft - 10.0) < 0.001:
                dSprites.add(Dog())

            if abs(timeLeft - 5.0) < 0.001:
                dSprites.add(Dog())

            if abs(timeLeft - 20.0) < 0.001:
                dSprites.add(Dog())

        if game_state == "menu":
            menu_state = menu_system.update(screen, [gun_pos[0], gun_pos[1], trigger])
            if menu_state == "new_game":
                game_state = "init"
        
        flash.draw(screen)
        ###############
	if game_state != "play":
        	crosshair.draw(screen)

        clock.tick(50)
        pygame.display.flip()
        
    dSprites.empty()


if __name__ == "__main__":    
    gamePlay()
    pygame.quit()
