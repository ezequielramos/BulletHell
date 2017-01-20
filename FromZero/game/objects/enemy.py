import pygame

enemyImage = pygame.image.load('images/mainship_t_o.png')

class Enemy(pygame.sprite.Group):

	width = 32
	height = 32
	heath = 5

	def __init__(self, x, y):

		super(Enemy,self).__init__()

		self.x = x
		self.y = y
		self.group = pygame.sprite.Group()
		self.hitimage = pygame.image.load('images/hitted_t.png')

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([self.width, 8])

		base.rect = base.image.get_rect()

		base.rect.x = x
		base.rect.y = y
		base.collidible = True

		self.group.add(base)

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([6, 22])

		base.rect = base.image.get_rect()

		base.rect.x = x + 14
		base.rect.y = y + 8
		base.collidible = True

		self.group.add(base)

		imagem = pygame.sprite.Sprite()

		imagem.image = enemyImage
		imagem.rect = imagem.image.get_rect()

		imagem.rect.x = x
		imagem.rect.y = y

		imagem.collidible = False

		self.add(imagem)

	def hit(self, damage):
		self.heath = self.heath - damage

		for sprite in self:
			sprite.image = self.hitimage

	def update(self):

		for sprite in self:
			sprite.rect.x = sprite.rect.x + 1
			sprite.image = enemyImage

		for sprite in self.group:
			sprite.rect.x = sprite.rect.x + 1

		self.x = self.x + 1

		self.group.update()