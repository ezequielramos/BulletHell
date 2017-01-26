import pygame

backgroundImage = pygame.image.load('images/background.jpg')

class Background(pygame.sprite.Group):
	width = 1920
	height = 1080

	def __init__(self):

		super(Background,self).__init__()

		base = pygame.sprite.Sprite()
		base.image = backgroundImage

		base.rect = base.image.get_rect()

		base.rect.x = 0
		base.rect.y = 0

		self.add(base)

		base = pygame.sprite.Sprite()
		base.image = backgroundImage

		base.rect = base.image.get_rect()

		base.rect.x = 0
		base.rect.y = -1080

		self.add(base)

	def update(self):

		for sprite in self:
			sprite.rect.y = sprite.rect.y+1

			if sprite.rect.y == 1080:
				sprite.rect.y = -1080