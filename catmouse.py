import sys
import random
import pygame

# Constants
SCREEN_SIZE = (600, 400)
BACKGROUND_PICT = "grass.png"		# For now, background pict must be same dimenstions as screenSize (600x400 pixels)
CAT_PICT = "cat.png"				# 80x58 pixels
MOUSE_PICT = "mouse.png"			# 50x49 pixels
catSpeed = 7						# Pixels to move for each keypress
waitTime = 10						# Time delay in ms for each loop

class CatMouseGame(object):
	def __init__(self):
		pass

class Cat(pygame.sprite.Sprite):
	"""Cat class"""
	def __init__(self):
		"""Creates a cat given an (x,y) tuple with specified starting position."""
		pygame.sprite.Sprite.__init__(self)		# Call the parent class (Sprite) constructor

		self.image = pygame.image.load(CAT_PICT).convert_alpha()

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values # of rect.x and rect.y
		self.rect = self.image.get_rect()

	def update(self, newPos):
		self.rect.x = newPos[0]
		self.rect.y = newPos[1]

class Mouse(pygame.sprite.Sprite):
	"""Mouse class"""
	def __init__(self, startPos=(0, 0)):
		"""Creates a mouse given an (x,y) tuple with specified starting position."""
		pygame.sprite.Sprite.__init__(self)		# Call the parent class (Sprite) constructor

		self.image = pygame.image.load(MOUSE_PICT).convert_alpha()

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values # of rect.x and rect.y
		self.rect = self.image.get_rect()

		self.xpos = startPos[0]				# Initial position
		self.ypos = startPos[1]				# Initial position
		self.xmove = random.randrange(0,5)	# x amount to move each update
		self.ymove = random.randrange(0,5)	# y amount to move each update

	def move(self):
		self.xpos += self.xmove
		self.ypos += self.ymove

	def update(self, newPos):
		self.rect.x = newPos[0]
		self.rect.y = newPos[1]


mouse = []

def MakeMice():
	global mouse
	mouse = []
	for i in range(0,5):
		mouse.append(Mouse())
		mousex = random.randrange(1, SCREEN_SIZE[0] - mouse[i].rect.size[0])
		mousey = random.randrange(1, SCREEN_SIZE[1] - mouse[i].rect.size[1])
		mouse[i].xpos, mouse[i].ypos = mousex, mousey
		mouse[i].update((mousex, mousey))
		allgroup.add(mouse[i])

def RemoveMiceFromGroup():
	global mouse
	for i in range(0,5):
		allgroup.remove(mouse[i])


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE)
	background = pygame.image.load(BACKGROUND_PICT).convert_alpha()

	# Place both cat and mouse at random start location
	cat = Cat()
	catx = random.randrange(1, SCREEN_SIZE[0] - cat.rect.size[0])
	caty = random.randrange(1, SCREEN_SIZE[1] - cat.rect.size[1])
	cat.update((catx, caty))

	# Create group (allgroup) for sprites to belong to
	allgroup = pygame.sprite.Group()

	MakeMice()

	allgroup.add(cat)		# Make cat appear on top

	# Main loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.blit(background, (0, 0))	# Display background image (same size as screen)
		allgroup.clear(screen, background)
		allgroup.draw(screen)
		pygame.display.flip()

		# Move the cat based on key presses
		keyState = pygame.key.get_pressed()

		if keyState[pygame.K_UP] and (caty > 0):
			caty -= catSpeed
		if keyState[pygame.K_DOWN] and (caty < (SCREEN_SIZE[1] - cat.rect.size[1])):
			caty += catSpeed
		if keyState[pygame.K_LEFT] and (catx > 0):
			catx -= catSpeed
		if keyState[pygame.K_RIGHT] and (catx < (SCREEN_SIZE[0] - cat.rect.size[0])):
			catx += catSpeed

		if keyState[pygame.K_m]:	#debug
			RemoveMiceFromGroup()	#debug
			MakeMice()				#debug

		cat.update((catx, caty))	# Update position of cat sprite

		# Update all mice
		for i in range(0,5):
			mouse[i].move()
			mouse[i].update((mouse[i].xpos, mouse[i].ypos))

		pygame.time.wait(waitTime)
