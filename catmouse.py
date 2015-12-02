import sys
import random
import pygame

pygame.init()

# Constants
screenSize = (600, 400)
backgroundPict = "grass.png"	# 600x400 pixels
catPict = "cat.png"				# 80x58 pixels
mousePict = "mouse.png"			# 50x49 pixels

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

	def update(self, newPos):
		self.rect.x = newPos[0]
		self.rect.y = newPos[1]


screen = pygame.display.set_mode(screenSize)
background = pygame.image.load("grass.png").convert_alpha()

#mouse = pygame.image.load("mouse.png").convert_alpha()
#cat = pygame.image.load("cat.png").convert_alpha()

# Place the cat in a random location at the start of the game
#catx = random.randrange
cat = Cat()
catx = random.randrange(1, screenSize[0] - cat.rect.size[0])
caty = random.randrange(1, screenSize[1] - cat.rect.size[1])
cat.update((catx, caty))

mouse = Mouse()
mousex = random.randrange(1, screenSize[0] - mouse.rect.size[0])
mousey = random.randrange(1, screenSize[1] - mouse.rect.size[1])
mouse.update((mousex, mousey))

# Create group (allgroup) for sprites to belong to
allgroup = pygame.sprite.Group()
allgroup.add(cat)
allgroup.add(mouse)

# Main loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.blit(background, (0, 0))	# Display background image (same size as screen)
	allgroup.clear(screen, background)
	#allgroup.update((1,1))
	allgroup.draw(screen)
	pygame.display.flip()          # flip the screen 30 times a second

	catx += 1
	caty += 1
	cat.update((catx, caty))
	mousex += 2
	mousey += 2
	mouse.update((mousex, mousey))
	pygame.time.wait(10)
