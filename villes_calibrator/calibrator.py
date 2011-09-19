#!/usr/bin/python
import cwiid
import sys
import pygame
import pickle
import random
import math

def main():
	led = 0
	rpt_mode = 0
	pygame.init()
	pygame.mixer.init()
	global gunSound
	global calibrationPhase
	global calibrationValues
	global exitMainLoop
	global targetPos
	global targetNumber
	global calibratedPosition
	targetNumber = 0
	targetPos=[0,0]
	exitMainLoop = False

	calibrationPhase = 0
	calibrationValues = []
	try:
		f = open('calibration.cal', 'r')
		calibrationValues = pickle.load(f)
		calibrationPhase = 5
		f.close()
		print 'Loaded calibration: ' + str(calibrationValues)
	except IOError:
		print "Can't open calibration file"
	except EOFError:
		print "Empty calibration file"

	gunSound = pygame.mixer.Sound('gun.wav')
	#Connect to address given on command-line, if present
	print 'Put Wiimote in discoverable mode now (press 1+2)...'
	global wiimote
	global pointerPos
	if len(sys.argv) > 1:
		wiimote = cwiid.Wiimote(sys.argv[1])
	else:
		wiimote = cwiid.Wiimote()
	print 'OK'
	led ^= cwiid.LED1_ON
	wiimote.led = led

	wiimote.mesg_callback = callback
	rpt_mode ^= cwiid.RPT_IR
	wiimote.rpt_mode = rpt_mode
	rpt_mode ^= cwiid.RPT_BTN
	wiimote.rpt_mode = rpt_mode

	wiimote.enable(cwiid.FLAG_MESG_IFC);

	# Set the height and width of the screen
	size=[700,700]
	screen=pygame.display.set_mode(size)

	pygame.display.set_caption("PYSSYTESTI")
 
	# Used to manage how fast the screen updates
	clock=pygame.time.Clock()

	pointerPos = [500,500]
	while not exitMainLoop:
		for event in pygame.event.get(): # User did something
		        if event.type == pygame.QUIT: # If user clicked close
            			exitMainLoop=True # Flag that we are done so we exit this loop
 		mainloop(screen, pointerPos, clock)
	print 'Quitting..'
	pygame.quit ()
	wiimote.close()

def setupNewTarget(screen):
	global targetNumber
	global targetPos
	targetPos[0] = random.randint(0,screen.get_width())
	targetPos[1] = random.randint(0,screen.get_height())
	targetNumber += 1
	print 'target at ' + str(targetPos)

def drawTarget(screen):
	global targetPos
	pos = targetPos
	pygame.draw.circle(screen, (0,0,0), pos, 50, 0)
	pygame.draw.circle(screen, (255,255,255), pos, 40, 0)
	pygame.draw.circle(screen, (0,0,0), pos, 30, 0)
	pygame.draw.circle(screen, (255,255,255), pos, 20, 0)
	pygame.draw.circle(screen, (0,0,0), pos, 10, 0)
	pygame.draw.circle(screen, (255,255,255), pos, 5, 0)

def mainloop(screen, pointerPos, clock):
	global calibrationPhase
	global targetNumber
	global calibratedPosition
	if(calibrationPhase == 5 and targetNumber == 0):
		setupNewTarget(screen)

	# Set the screen background
	screen.fill((255,255,255))

	drawTarget(screen)

	calibratedPosition = calibratePosition(pointerPos, screen)

	drawCrosshairs(screen, (0,0,0), calibratedPosition)
	drawCalibrationStuff(screen)
		

	# Limit to 60 frames per second
	clock.tick(60)
 
	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

def calibratePosition(pointerPos, screen):
	if(calibrationPhase <= 4):
		return pointerPos
	global calibrationValues
	pos = pointerPos
	pos[0] = pos[0] - calibrationValues[0][0]
	rng = calibrationValues[3][0]-calibrationValues[0][0]
	pos[0] = float(pos[0]) / float(rng)
	pos[0] = int(pos[0] * float(screen.get_width()))

	pos[1] = pos[1] - calibrationValues[0][1]
	rng = calibrationValues[3][1]-calibrationValues[0][1]
	pos[1] = float(pos[1]) / float(rng)
	pos[1] = int(pos[1] * float(screen.get_height()))

	if(pos[0] < 0):
		pos[0] = 0;
	if(pos[0] > screen.get_width()):
		pos[0] = screen.get_width();

	if(pos[1] < 0):
		pos[1] = 0;
	if(pos[1] > screen.get_height()):
		pos[1] = screen.get_height();
	return pos

def drawCalibrationStuff(screen):
	global calibrationPhase
	if(calibrationPhase > 4):
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
	if(calibrationPhase==4):
		text = font.render("Shoot center",True,(0,0,0))
		targetPos = [screen.get_width()/2, screen.get_height()/2]
#	assert(calibrationPhase < 5)
	screen.blit(text, [250,250])
	drawCrosshairs(screen, (128,0,0), targetPos)

def drawCrosshairs(screen, color, pos):
	pygame.draw.line(screen,color,[pos[0] - 30, pos[1]],[pos[0]+30, pos[1]],1)
	pygame.draw.line(screen,color,[pos[0], pos[1] - 30],[pos[0], pos[1] + 30],1)
	pygame.draw.circle(screen, color, pos, 20, 1)
	pygame.draw.circle(screen, color, pos, 5, 1)

def checkTargetHit():
	global calibratedPosition
#	if(math.sqrt( ( calibratedPosition[0]-targetPos[0] )**2 + ( calibratedPosition[1]-targetPos[1] )**2 ) < 50):
#		setupNewTarget()

def gunFired():
	global gunSound
	gunSound.play()
	global calibrationPhase
	global pointerPos
	global targetPos
	if(calibrationPhase > 4):
		checkTargetHit()
		return
	global calibrationValues
	calibrationValues.append(pointerPos)
	calibrationPhase = calibrationPhase + 1
	print str(calibrationValues)
	if(calibrationPhase==5):
		f = open('calibration.cal', 'w')
		pickle.dump(calibrationValues, f)
		f.close()

def callback(mesg_list, time):
	global exitMainLoop
	for mesg in mesg_list:
		if mesg[0] == cwiid.MESG_BTN:
			print 'Button Report: ' + str(mesg[1])
			if(mesg[1]==4):
				gunFired()
			if(mesg[1]==128):
				exitMainLoop = True

		elif mesg[0] == cwiid.MESG_IR:
			valid_src = False
			
			for src in mesg[1]:
				if src:
					valid_src = True
					global pointerPos
					pointerPos = list(src['pos'])
					pointerPos[0] = 1024 - pointerPos[0]

		elif mesg[0] ==  cwiid.MESG_ERROR:
			print "Error message received"
			exitMainLoop = True
		else:
			print 'Unknown Report'

main()

