from pygame.sprite import Sprite
from pygame import Surface
from gamelib.rgb import WHITEBLUE
from math import sin
from math import cos
from sprites import miscs

class Bullet(Sprite):
	width = 5
	height = 5
	speed = 10

	def __init__(self, spriteOrigin, angle):
		Sprite.__init__(self, miscs)
		super(Bullet, self).__init__()

		self.image = Surface([self.width, self.height])
		self.image.fill(WHITEBLUE)

		self.rect = self.image.get_rect()

		self.rect.x = spriteOrigin.rect.x + 20
		self.rect.y = spriteOrigin.rect.y

		self.move_y = (-1 * round(sin(angle))) * 10
		self.move_x = (-1 * round(cos(angle))) * 10

		#print(angle, round(sin(angle)), round(cos(angle)))

	def update(self):
		self.rect.y += self.move_y
		self.rect.x += self.move_x

		#self.rect.y = self.rect.y-10
		#self.image.fill(WHITEBLUE)

		#enemy_collide = pygame.sprite.spritecollideany(self,enemies_group)

		#if enemy_collide:
		#	enemy_collide.kill()
		#	self.kill()

		#if(self.rect.y < 0):
		#	self.kill()