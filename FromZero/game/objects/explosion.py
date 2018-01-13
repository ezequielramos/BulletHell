import pygame

pygame.mixer.init() 

class Explosions(pygame.sprite.Group):

	width = 32
	height = 32

	def __init__(self, mainPath):

		self.explosionSound = pygame.mixer.Sound(mainPath + "sounds/Explosion.wav")
		self.explosionImage = pygame.image.load(mainPath + 'images/explosion_t.png')


		super(Explosions,self).__init__()

	def addExplosion(self, x, y):

		self.explosionSound.play()

		base = pygame.sprite.Sprite()
		base.fps = 0

		base.image = self.explosionImage

		base.rect = base.image.get_rect()

		base.rect.x = x
		base.rect.y = y

		self.add(base)

	def update(self):

		for sprite in self:
			sprite.fps += 1
			if sprite.fps > 30:
				self.remove(sprite)
				del sprite