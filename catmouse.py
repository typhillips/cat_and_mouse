# Cat and Mouse Game
#
# Copyright 2017 Ty Phillips. All Rights Reserved.
# This program is free software. You can redistribute and/or modify it in
# accordance with the terms of the accompanying license agreement.

#!/usr/bin/env python

import sys
import random
import pygame
import ConfigParser
import time

# Constants
cfgFilename = "settings.ini"
screenSize = (600, 400)

class Cat(pygame.sprite.Sprite):
	"""Cat class"""
	def __init__(self, catPict):
		"""Creates a cat given an (x,y) tuple with specified starting position."""
		pygame.sprite.Sprite.__init__(self)		# Call the parent class (Sprite) constructor

		self.image = pygame.image.load(catPict).convert_alpha()

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values # of rect.x and rect.y
		self.rect = self.image.get_rect()

		# For collision detection (half of rect width)
		self.radius = self.rect.width / 2

	def update(self, newPos):
		self.rect.x = newPos[0]
		self.rect.y = newPos[1]

class Mouse(pygame.sprite.Sprite):
	"""Mouse class"""
	def __init__(self, mousePict, mouseMoveGain, screenSize):
		"""Creates a mouse given an (x,y) tuple with specified starting position."""
		pygame.sprite.Sprite.__init__(self)		# Call the parent class (Sprite) constructor

		self.image = pygame.image.load(mousePict).convert_alpha()

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values # of rect.x and rect.y
		self.rect = self.image.get_rect()

		# "Trimmed" screen size is slightly smaller than full screen size so that mice don't get generated
		#   partially off screen
		self.screenSizeTrimmed = (screenSize[0] - self.rect.size[0], screenSize[1] - self.rect.size[1])

		# For collision detection (half of rect width)
		self.radius = self.rect.width / 2

		# Get random point on edge of screen and set starting sprite position to this point
		startPoint = self.makeEdgePoint(self.screenSizeTrimmed)
		self.rect.x = startPoint[0]
		self.rect.y = startPoint[1]

		# Get a second random point (but convert tuple to a list so we can manipulate it)
		endPoint = list(self.makeEdgePoint(self.screenSizeTrimmed))

		#### This next bit of code ensures that start and end points aren't too close together
		# If start point is on left edge, force end point to right side of screen, and
		#   if start point is on right edge, force end point to left side of screen
		if ((startPoint[0] == 0) and (endPoint[0] < (self.screenSizeTrimmed[0] / 2))) or \
		   ((startPoint[0] == self.screenSizeTrimmed[0]) and (endPoint[0] > (self.screenSizeTrimmed[0] / 2))):
			endPoint[0] = self.screenSizeTrimmed[0] - endPoint[0]	# Flip end point horizontally
		# If start point is on top edge, force end point to bottom side of screen, and
		#   if start point is on bottom edge, force end point to top side of screen
		elif ((startPoint[1] == 0) and (endPoint[1] < (self.screenSizeTrimmed[1] / 2))) or \
		     ((startPoint[1] == self.screenSizeTrimmed[1]) and (endPoint[1] > (self.screenSizeTrimmed[1] > 2))):
			endPoint[1] = self.screenSizeTrimmed[1] - endPoint[1]	# Flip end point vertically
		else:
			pass

		# Calculate slope of the line between start and end points
		xdelta = endPoint[0] - startPoint[0]
		ydelta = endPoint[1] - startPoint[1]
		if xdelta != 0:
			slope = abs(float(ydelta) / float(xdelta))
		elif ydelta > 0:
			slope = mouseMoveGain
		elif ydelta < 0:
			slope = -mouseMoveGain
		else:
			pass

		# Figure out the closest integer approximations of xmove,ymove (these represent the amount
		#   to change x and y each iteration through the main loop) based on this slope
		if slope < 1:
			self.xmove = mouseMoveGain
			self.ymove = int(round(slope, 0))
		elif slope > mouseMoveGain:
			self.xmove = 0
			self.ymove = mouseMoveGain
		else:
			self.xmove = int(round(slope * mouseMoveGain, 0))
			self.ymove = mouseMoveGain

		# Re-apply correct sign to x,y terms so we move in the correct direction
		if xdelta < 0:
			self.xmove = -self.xmove
		if ydelta < 0:
			self.ymove = -self.ymove

	def makeEdgePoint(self, size):
		"""Given a rectangle of specified dimensions, find a random x,y point on an edge."""
		side = random.randrange(0, 3)

		if side == 0:		# Top edge
			x = random.randrange(0, size[0])
			y = 0
		elif side == 1:		# Right edge
			x = self.screenSizeTrimmed[0]
			y = random.randrange(0, size[1])
		elif side == 2:		# Bottom edge
			x = random.randrange(0, size[0])
			y = self.screenSizeTrimmed[1]
		else:				# Left edge
			x = 0
			y = random.randrange(0, size[1])

		return (x, y)

	def update(self):
		self.rect.x += self.xmove
		self.rect.y += self.ymove

class CatMouseGame(object):
	"""Main class for the game"""
	def __init__(self):
		pygame.init()
		self.readConfig()
		self.screen = pygame.display.set_mode(self.screenSize)
		self.background = pygame.image.load(self.bkgrndPict).convert_alpha()
		self.muteIcon = pygame.image.load(self.mutePict).convert_alpha()
		self.mice = []
		self.mouseSpawnTimer = 0
		self.score = 0
		self.mute = False
		self.timeRemaining = self.gameTime

	def readConfig(self):
		""" Read configuration input file. """
		try:
			# Instantiate config parser and process file
			config = ConfigParser.RawConfigParser()
			config.read(cfgFilename)

			# Read [general] section
			tmplist = []
			for dimension in config.get('general', 'screen size').split(','):
				tmplist.append(int(dimension))
				self.screenSize = tuple(tmplist)
			self.catSpeed = config.getint('general', 'cat speed')
			self.waitTime = config.getint('general', 'wait time')
			self.spawnTime = config.getint('general', 'spawn time')
			self.mouseMoveGain = config.getint('general', 'mouse move gain')
			self.fontSize = config.getint('general', 'font size')

			tmplist = []
			for color in config.get('general', 'font color').split(','):
				tmplist.append(int(color))
				self.fontColor = tuple(tmplist)

			self.gameTime = config.getint('general', 'game time')

			# Read [pictures] section
			self.bkgrndPict = config.get('pictures', 'background')
			self.catPict = config.get('pictures', 'cat')
			self.mousePict = config.get('pictures', 'mouse')
			self.mutePict = config.get('pictures', 'mute')

			# Read [sounds] section
			self.collideSound= pygame.mixer.Sound(config.get('sounds', 'collide'))

		# If any kind of exception occurs while parsing the configuration file, just silently ignore
		#   any remaining settings and abort the configuration update
		except:
			pass


	def start(self):
		"""Initialize & start the game."""
		# Place cat at random start location
		self.cat = Cat(self.catPict)
		self.catx = random.randrange(1, self.screenSize[0] - self.cat.rect.size[0])
		self.caty = random.randrange(1, self.screenSize[1] - self.cat.rect.size[1])
		self.cat.update((self.catx, self.caty))

		# Create groups for sprites to belong to
		self.catgroup = pygame.sprite.Group()
		self.catgroup.add(self.cat)
		self.mousegroup = pygame.sprite.Group()

		# Run main game loop
		self.mainLoop()

	def manageMice(self):
		"""Handle creating/destroying mice sprites & their movement."""
		# Spawn a new mouse if spawn time has elapsed
		if ( (pygame.time.get_ticks() - self.mouseSpawnTimer) > self.spawnTime ) and ( self.timeRemaining > 0):
			mouse = Mouse(self.mousePict, self.mouseMoveGain, self.screenSize)
			self.mice.append(mouse)
			self.mousegroup.add(mouse)
			self.mouseSpawnTimer = pygame.time.get_ticks()	# Reset spawn timer to current time

		# Move each mouse
		for mouse in self.mice:
			mouse.update()
			if (mouse.rect.x > self.screenSize[0]) or (mouse.rect.y > self.screenSize[1]):
				mouse.kill()

	def mainLoop(self):
		"""Main loop for gameplay."""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			# Move the cat based on key presses
			keyState = pygame.key.get_pressed()

			if keyState[pygame.K_UP] and (self.caty > 0):
				self.caty -= self.catSpeed
			if keyState[pygame.K_DOWN] and (self.caty < (self.screenSize[1] - self.cat.rect.size[1])):
				self.caty += self.catSpeed
			if keyState[pygame.K_LEFT] and (self.catx > 0):
				self.catx -= self.catSpeed
			if keyState[pygame.K_RIGHT] and (self.catx < (self.screenSize[0] - self.cat.rect.size[0])):
				self.catx += self.catSpeed

			# for development - quick exit
			if keyState[pygame.K_q]:
				sys.exit()

			# Mute sound
			# Check previous state to debouce 'm' key since it's a toggle
			if keyState[pygame.K_m] and not keyStateOld[pygame.K_m]:
				if self.mute == False:
					self.mute = True
				else:
					self.mute = False

			# Save off previous key state
			keyStateOld = keyState

			# Update position of cat sprite if game is still in progress
			if self.timeRemaining > 0:
				self.cat.update((self.catx, self.caty))

			# Take care of the mice
			self.manageMice()

			# See if the cat has collided with anything in the mouse group
			#  (Note: the True flag will remove the mouse from the list)
			collideList = pygame.sprite.spritecollide(self.cat, self.mousegroup, True, pygame.sprite.collide_circle)

			# Add 1 to the score for each mouse caught
			for mouse in collideList:
				self.score +=1
				if self.mute == False:
					self.collideSound.play()			# Play collide sound

			self.screen.blit(self.background, (0, 0))	# Display background image (same size as screen)

			self.mousegroup.clear(self.screen, self.background)		# Draw mice first (so cat will overlap)
			self.mousegroup.draw(self.screen)
			self.catgroup.clear(self.screen, self.background)
			self.catgroup.draw(self.screen)

			# Display score
			font = pygame.font.Font(None, self.fontSize)
			text = font.render("Score: " + str(self.score), 1, self.fontColor)
			textpos = text.get_rect()
			textpos.topleft = (10, 10)
			self.screen.blit(text, textpos)

			# Display elapsed time
			font = pygame.font.Font(None, 24)
			# Lower limit time remaining to 0
			self.timeRemaining = max( self.gameTime - pygame.time.get_ticks(), 0 )
			time_remaining_str = time.strftime('%M:%S', time.gmtime(self.timeRemaining / 1000))	# Convert time in ms to sec and format as MM:SS
			text = font.render(time_remaining_str, 1, (255, 255, 255))
			textpos = text.get_rect()
			textpos.bottomleft = (10, screenSize[1] - 10)
			self.screen.blit(text, textpos)

			# Display mute icon (if sound is muted)
			if self.mute == True:
				mutepos = self.muteIcon.get_rect()
				mutepos.topleft = (self.screenSize[0] - self.muteIcon.get_rect().size[0] - 10, 10)
				self.screen.blit(self.muteIcon, mutepos)

			# Game over display
			if self.timeRemaining <= 0:
				font_go = pygame.font.Font(None, 48)
				text = font_go.render("GAME OVER", 1, self.fontColor)
				textpos = text.get_rect()
				textpos.midleft = ((screenSize[0] - textpos.width) / 2, screenSize[1] / 2)
				self.screen.blit(text, textpos)

			pygame.display.flip()
			pygame.time.wait(self.waitTime)	# To regulate gameplay speed

if __name__ == "__main__":
	game = CatMouseGame()
	game.start()

