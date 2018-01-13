import pygame

pygame.mixer.init() 

class Bullet(pygame.sprite.Group):
	width = 3
	height = 6
	damage = 1

	def __init__(self, mainPath):

		self.bulletsound = pygame.mixer.Sound(mainPath + "sounds/Laser_Shoot.wav")
		self.bulletImage = pygame.image.load(mainPath + 'images/simple_laser_shot_t.png')

		super(Bullet,self).__init__()

	def update(self):

		for sprite in self:

			sprite.rect.y = sprite.rect.y-10

			if sprite.rect.y < 6:
				self.remove(sprite)
				del sprite

	def shot(self, x, y):

		self.bulletsound.play()

		base = pygame.sprite.Sprite()

		base.image = self.bulletImage

		base.rect = base.image.get_rect()

		base.rect.x = x + 15
		base.rect.y = y

		self.add(base)