import sys
import random
import pygame

# Constants
screenSize = (600, 400)
bkgrndPict = "grass.png"		# For now, background pict must be same dimenstions as screenSize (600x400 pixels)
catPict = "cat.png"				# 80x58 pixels
mousePict = "mouse.png"			# 50x49 pixels
catSpeed = 7					# Pixels to move for each keypress
waitTime = 10					# Time delay in ms for each loop
spawnTime = 2000				# Time in ms between each mouse spawn TODO randomize this
mouseMoveGain = 5				# Gain factor which affects how fast the mice move

class Cat(pygame.sprite.Sprite):
	"""Cat class"""
	def __init__(self):
		"""Creates a cat given an (x,y) tuple with specified starting position."""
		pygame.sprite.Sprite.__init__(self)		# Call the parent class (Sprite) constructor

		self.image = pygame.image.load(catPict).convert_alpha()

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values # of rect.x and rect.y
		self.rect = self.image.get_rect()

	def update(self, newPos):
		self.rect.x = newPos[0]
		self.rect.y = newPos[1]

class Mouse(pygame.sprite.Sprite):
	"""Mouse class"""
	def __init__(self):
		"""Creates a mouse given an (x,y) tuple with specified starting position."""
		pygame.sprite.Sprite.__init__(self)		# Call the parent class (Sprite) constructor

		self.image = pygame.image.load(mousePict).convert_alpha()

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values # of rect.x and rect.y
		self.rect = self.image.get_rect()


		#TODO here's how I want to do this start position and movement direction business
		# Select a random number between 0 and 3. Each one represents a side of the screen.
		# If 0, set x = -self.rect.size[0] and y to a random number from 0 to screenSize[1]
		# If 1, set y = -self.rect.size[1] and x to a random number from 0 to screenSize[0]
		#   etc....
		# Then determine if we're in the top or bottom half of the rectangle based on y
		# Assign a random point on the other side as the endpoint
		# Calculate the slope of the line between the two points and set xmove & ymove to the
		# nearest integers to this slope
		# VOILA!!

		startPoint = self.makeEdgePoint(screenSize)
		self.rect.x = startPoint[0]
		self.rect.y = startPoint[1]

		tmpPoint = self.makeEdgePoint((screenSize[0], screenSize[1]/2))
		endx = tmpPoint[0]

		# Now figure out if we are starting on the top or bottom half of the screen
		#   end point should be on opposite half
		if self.rect.y < (screenSize[1] / 2):		# Starting in top half
			endy = tmpPoint[1] + (screenSize[1] / 2)
		else:
			endy = tmpPoint[1]

		# Now calculate slope between (self.rect.x,self.rect.y) and (endx,endy)
		slope = float(endy - self.rect.y) / float(endx - self.rect.x)

		# Save off sign of slope and then get absolute value
		tmp = 1

		if slope < 0:
			tmp *= -1

		slope = abs(slope)
		
		if slope < 1:
			self.xmove = mouseMoveGain
			self.ymove = int(round(slope, 0))
		elif slope > mouseMoveGain:
			self.xmove = 0
			self.ymove = mouseMoveGain
		else:
			self.xmove = int(round(slope * mouseMoveGain, 0))
			self.ymove = mouseMoveGain

		#TODO take care of negative slope (re-assign xmove/ymove appropriately)

		# Create movement direction for sprite (they only move in one direction)
		#self.xmove = random.randrange(0, 5)	# x amount to move each update
		#self.ymove = random.randrange(0, 5)	# y amount to move each update

	def makeEdgePoint(self, size):
		"""Given a rectangle of specified dimensions, find a random x,y point on an edge."""
		side = random.randrange(0, 3)

		if side == 0:		# Top edge
			x = random.randrange(0, size[0])
			y = 0
		elif side == 1:		# Right edge
			x = screenSize[0]
			y = random.randrange(0, size[1])
		elif side == 2:		# Bottom edge
			x = random.randrange(0, size[0])
			y = screenSize[1]
		else:				# Left edge
			x = 0
			y = random.randrange(0, size[1])

		return (x, y)

	def update(self, newPos):
		self.rect.x += self.xmove
		self.rect.y += self.ymove

class CatMouseGame(object):
	"""Main class for the game"""
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(screenSize)
		self.background = pygame.image.load(bkgrndPict).convert_alpha()
		self.mouseSpawnTimer = 0

	def start(self):
		"""Initialize & start the game."""
		# Place cat at random start location
		self.cat = Cat()
		self.catx = random.randrange(1, screenSize[0] - self.cat.rect.size[0])
		self.caty = random.randrange(1, screenSize[1] - self.cat.rect.size[1])
		self.cat.update((self.catx, self.caty))

		# Create group (allgroup) for sprites to belong to
		self.allgroup = pygame.sprite.Group()
		self.allgroup.add(self.cat)

		#mouse = Mouse()
		#mousex = random.randrange(1, screenSize[0] - mouse.rect.size[0])
		#mousey = random.randrange(1, screenSize[1] - mouse.rect.size[1])
		#mouse.update((mousex, mousey))
		#allgroup.add(mouse)
		self.mainLoop()

	def manageMice(self):
		"""Handle creating/destroying mice sprites & their movement."""
		# Spawn a new mouse if spawn time has elapsed
		if (pygame.time.get_ticks() - self.mouseSpawnTimer) > spawnTime:
			mouse = Mouse()
			self.mice.append(mouse)
			self.mouseSpawnTimer = pygame.time.get_ticks()	# Reset spawn timer to current time

		# Move each mouse
		for mouse in self.mice:
			mouse.update()

	def mainLoop(self):
		"""Main loop for gameplay."""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			self.manageMice()		# Take care of the mice

			self.screen.blit(self.background, (0, 0))	# Display background image (same size as screen)
			self.allgroup.clear(self.screen, self.background)
			self.allgroup.draw(self.screen)
			pygame.display.flip()

			# Move the cat based on key presses
			keyState = pygame.key.get_pressed()

			if keyState[pygame.K_UP] and (self.caty > 0):
				self.caty -= catSpeed
			if keyState[pygame.K_DOWN] and (self.caty < (screenSize[1] - self.cat.rect.size[1])):
				self.caty += catSpeed
			if keyState[pygame.K_LEFT] and (self.catx > 0):
				self.catx -= catSpeed
			if keyState[pygame.K_RIGHT] and (self.catx < (screenSize[0] - self.cat.rect.size[0])):
				self.catx += catSpeed

			# for development - quick exit
			if keyState[pygame.K_q]:
				sys.exit()

			# Update position of cat sprite
			self.cat.update((self.catx, self.caty))

			# Test code to move cat and mouse diagonally down & to the right @different speeds
			#mousex += 2
			#mousey += 2
			#mouse.update((mousex, mousey))
			pygame.time.wait(waitTime)	# To regulate gameplay speed

if __name__ == "__main__":
	game = CatMouseGame()
	game.start()

