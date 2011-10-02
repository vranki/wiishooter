"""
Copyright 2011 Michael Bachmann

This program is distributed under the terms of the GNU
General Public License
"""

import pygame, random
pygame.init()

from DuckLib import *

screen     = pygame.display.set_mode((640,480), pygame.FULLSCREEN)
screen_dim = screen.get_rect()
pygame.display.set_caption("Duck Rehunt: Reckoning")


def gamePlay():

    pygame.mixer.init()
    pygame.mixer.Sound("Music.ogg").play(-1)

    background     = pygame.Surface(screen.get_size())
    background.blit(pygame.image.load("Background.gif"), (0,0))
    screen.blit(background, (0,0))
 
    foreground     = setPiece(pygame.image.load("Foreground.gif"), (0,301), 1 )
    #hud            = setPiece(pygame.image.load("Hud.gif"), (22, 400), 3 )
    setSprites     = pygame.sprite.LayeredUpdates( foreground )#, hud)

    dSprites.add(Dog())

    crosshair = pygame.sprite.Group(Crosshair())
                          
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
    
    while keepGoing:

        clock.tick(50)
        pygame.mouse.set_visible(False)
        timeLeft -= 0.02
        timeboard = myFont.render("Time left: " + str(int(timeLeft)), 1, (255,255,255))
        if timeLeft <= 0:
            keepGoing = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    keepGoing = False
                    killGame = True

            elif event.type == pygame.KEYDOWN:
                keepGoing = False
                killGame = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gunshot.play()
                flash.add(Flash())
                pointCollide = [sprite for sprite in dSprites.sprites() if sprite.rect.collidepoint(pygame.mouse.get_pos())]
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
                    scoreboard = myFont.render("Score: " + str(score), 1, (255,255,255))

        if abs(timeLeft - 10.0) < 0.001:
            dSprites.add(Dog())

        if abs(timeLeft - 5.0) < 0.001:
            dSprites.add(Dog())

        if abs(timeLeft - 20.0) < 0.001:
            dSprites.add(Dog())
    
        #Garbage collection        
        pause+= 1
        if pause >= delay:

            dSprites.remove([sprite for sprite in dSprites.sprites() if sprite.rect.centery >= 500])

        dSprites.clear(screen, background)
        crosshair.clear(screen, background)
        flash.clear(screen, background)

        dSprites.update()
        crosshair.update()
        flash.update()
        
        dSprites.draw(screen)
        setSprites.draw(screen)
        
        screen.blit(scoreboard, (440,410))
        screen.blit(timeboard, (240,410))
        flash.draw(screen)
        crosshair.draw(screen)
        pygame.display.flip()
    dSprites.empty()
    return killGame, score


def welcomeScreen():
    #pygame.mixer.init()
    #pygame.mixer.Sound("Intro.ogg").play(-1)
    background     = pygame.Surface(screen.get_size())
    background.blit(pygame.image.load("Background2.gif"), (0,0))
    screen.blit(background, (0,0))
    crosshair = pygame.sprite.Group(Crosshair())
    myFont1 = pygame.font.Font(None, 22)
    titleFont1 = pygame.font.Font(None, 40)
    #myFont2 = pygame.font.Font(None, 30)
    #titleFont2 = pygame.font.Font(None, 40)
    
    title = titleFont1.render("DuckReHunt", 1, (0,0,0))
    lines = []
    lines.append(myFont1.render("Duck hunt clone orginally developed by Michael Bachmann", 1, (0,0,0)))
    lines.append(myFont1.render("and is heavily modified by Hackerspace 5w, Tampere (5w.fi)", 1, (0,0,0)))
    lines.append(myFont1.render("", 1, (0,0,0)))
    lines.append(myFont1.render("In game you have 30 seconds time to shoot as many ducks as possible", 1, (0,0,0)))
    lines.append(myFont1.render("There is no reloads or ammo limits, so don't hesitate to shoot!", 1, (0,0,0)))
    lines.append(myFont1.render("Please, stand in square marked on the floor for best game experience", 1, (0,0,0)))
    lines.append(myFont1.render("For shooting you must use iron (/plastic ;) sights of the gun,", 1, (0,0,0)))
    lines.append(myFont1.render("there is no virtual sight in actual game!", 1, (0,0,0)))

    butText = titleFont1.render("Start", 1, (0,0,0))

    keepGoing = True
    killGame = False
    clock = pygame.time.Clock()

    while keepGoing:

        clock.tick(50)
        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                killGame = True
            elif event.type == pygame.KEYDOWN:
                keepGoing = False
                killGame = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gunshot.play()
                flash.add(Flash())
                mpos = pygame.mouse.get_pos()

                if mpos[0] < 600 and mpos[0] > 500 and mpos[1] > 380 and mpos[1] < 430:
                    keepGoing = False

        crosshair.clear(screen, background)
        flash.clear(screen, background)

        crosshair.update()
        flash.update()

        screen.blit(background, (0,0))
        
        screen.blit(title, (230,40))
        lpos = 110
        for line in lines:
            screen.blit(line, (45,lpos))
            lpos += 30

        pygame.draw.rect(screen, (200,200,200), (500,380,100,50), 0)
        pygame.draw.rect(screen, (0,0,0), (500,380,100,50), 1)
        screen.blit(butText, (515,392))

        flash.draw(screen)
        crosshair.draw(screen)

        pygame.display.flip()

    return killGame


def highScores(myScore):
    pygame.mixer.init()
    background     = pygame.Surface(screen.get_size())
    background.blit(pygame.image.load("Background2.gif"), (0,0))
    screen.blit(background, (0,0))
    crosshair = pygame.sprite.Group(Crosshair())
    myFont1 = pygame.font.Font(None, 22)
    titleFont1 = pygame.font.Font(None, 40)
    #myFont2 = pygame.font.Font(None, 30)
    #titleFont2 = pygame.font.Font(None, 40)
    
    title = titleFont1.render("High scores", 1, (0,0,0))
    lines = []
    f = open("highscores.txt", "r")

    print f

    lines.append(myFont1.render("Your score was: " + str(myScore), 1, (0,0,0)))
    lines.append(myFont1.render("", 1, (0,0,0)))
    lines.append(myFont1.render("TOP 3", 1, (0,0,0)))

    scores = []

    top3Flag = False

    for line in f:
        line = line.strip()
        if int(line) < myScore:
            scores.append(myScore)
            top3Flag = True
        scores.append(int(line))

    print scores

    f.close()
    f = open("highscores.txt", "w+")

    for i in range(0,3):
        print scores[i]
        f.write(str(scores[i]) + "\n")
        lines.append(myFont1.render(str(scores[i]), 1, (0,0,0)))

    f.close()

    if top3Flag:
        lines.append(myFont1.render("", 1, (0,0,0)))
        lines.append(myFont1.render("", 1, (0,0,0)))
        lines.append(myFont1.render("Congratz, you made to TOP 3!!", 1, (0,0,0)))

    butText = titleFont1.render("mkay", 1, (0,0,0))

    keepGoing = True
    killGame = False
    clock = pygame.time.Clock()

    while keepGoing:

        clock.tick(50)
        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                killGame = True
            elif event.type == pygame.KEYDOWN:
                keepGoing = False
                killGame = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gunshot.play()
                flash.add(Flash())
                mpos = pygame.mouse.get_pos()

                if mpos[0] < 400 and mpos[0] > 300 and mpos[1] > 380 and mpos[1] < 430:
                    keepGoing = False

        crosshair.clear(screen, background)
        flash.clear(screen, background)

        crosshair.update()
        flash.update()

        screen.blit(background, (0,0))
        
        screen.blit(title, (250,40))
        lpos = 110
        for line in lines:
            screen.blit(line, (195,lpos))
            lpos += 30

        pygame.draw.rect(screen, (200,200,200), (300,380,100,50), 0)
        pygame.draw.rect(screen, (0,0,0), (300,380,100,50), 1)
        screen.blit(butText, (315,392))

        flash.draw(screen)
        crosshair.draw(screen)

        pygame.display.flip()

    f.close()

    return killGame


if __name__ == "__main__":
    while True:
        killGame = welcomeScreen()
        if killGame:
            break
        killGame, score = gamePlay()
        if killGame:
            break
        #score = 68
        killGame = highScores(score)
        if killGame:
            break

pygame.quit()
