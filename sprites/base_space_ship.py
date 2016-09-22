from pygame.sprite import Sprite
from pygame import Surface
from gamelib.rgb import WHITE
from gamelib import screen
from sprites.bullet import Bullet

class BaseSpaceShip(Sprite):

	width = 50
	height = 50
	my_joystick = None
	step_size = 5

	def __init__(self,  group_ref = None, coords = (0, 0), colour = WHITE):
		Sprite.__init__(self)
		if group_ref is not None:
			group_ref.add(self)

		self.image = Surface([self.width, self.height])
		self.image.fill(colour)

		self.rect = self.image.get_rect()

		self.rect.x = coords[0]
		self.rect.y = coords[1]

	def move(self, axys, forward=True, steps=1):
		self.rect[axys] += ((self.step_size * steps) * (1 if forward else -1))

		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x + self.width > screen.WIDTH:
			self.rect.x = screen.WIDTH - self.width

		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y + self.height > screen.HEIGHT:
			self.rect.y = screen.HEIGHT - self.height

	def shoot(self, move_x, move_y):
		Bullet(self, move_x, move_y)
