import pygame
import game.static
from . import bullet

class Player(pygame.sprite.Group):

	width = 32
	height = 32
	def __init__(self, x, y):

		super(Player,self).__init__()

		self.group = pygame.sprite.Group()
		
		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([self.width, 8])

		base.rect = base.image.get_rect()

		base.rect.x = x
		base.rect.y = y + 24

		self.base = base

		self.group.add(self.base)

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([6, 22])

		base.rect = base.image.get_rect()

		base.rect.x = x + 14
		base.rect.y = y + 2

		self.tronco = base

		self.group.add(self.tronco)

		self.imagem = pygame.sprite.Sprite()

		self.imagem.image = pygame.image.load('images/mainship_t.png')

		self.imagem.rect = self.imagem.image.get_rect()

		self.imagem.rect.x = x
		self.imagem.rect.y = y

		self.pos = [False,False,False,False]

		self.add(self.imagem)

		self.bullets = bullet.Bullet()

	def update(self):

		differX = 0
		differY = 0

		if self.pos[0]:
			if self.imagem.rect.x-3 < 0:
				differX = 0
			else:
				differX = -3
		elif self.pos[1]:
			if self.imagem.rect.x+3 > (game.static.width - 32):
				differX = 0
			else:
				differX = 3

		if self.pos[2]:
			if self.imagem.rect.y-3 < 0:
				differY = 0
			else:
				differY = -3
		elif self.pos[3]:
			if self.imagem.rect.y+3 > (game.static.height - 50 - 32):
				differY = 0
			else:
				differY = 3

		for sprite in self:
			sprite.rect.x = sprite.rect.x + differX
			sprite.rect.y = sprite.rect.y + differY

		for sprite in self.group:
			sprite.rect.x = sprite.rect.x + differX
			sprite.rect.y = sprite.rect.y + differY

		self.group.update()
		self.bullets.update()

	def shot(self):
		self.bullets.shot(self.imagem.rect.x, self.imagem.rect.y)