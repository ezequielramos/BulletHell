import pygame
import game
import math

enemyImage = pygame.image.load('images/mainship_t_o.png')
hitimage = pygame.image.load('images/hitted_t.png')

class Enemy(pygame.sprite.Group):

	width = 32
	height = 32
	heath = 5

	def __init__(self, x, y):

		super(Enemy,self).__init__()

		self.x = x
		self.y = y
		self.group = pygame.sprite.Group()
		self.direction = 1

		self.rota = []
		self.umquarto = 0
		self.gira = True
		self.velocidade = 1

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([self.width, 8])

		base.rect = base.image.get_rect()

		base.rect.x = x
		base.rect.y = y

		self.group.add(base)

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([6, 22])

		base.rect = base.image.get_rect()

		base.rect.x = x + 14
		base.rect.y = y + 8

		self.group.add(base)

		imagem = pygame.sprite.Sprite()

		imagem.image = enemyImage
		imagem.rect = imagem.image.get_rect()

		imagem.rect.x = x
		imagem.rect.y = y

		self.add(imagem)

	def hit(self, damage):
		self.heath = self.heath - damage

		for sprite in self:
			sprite.image = hitimage

	def update(self):

		if len(self.rota) > 0:

			self.movRota()

		else:

			if self.gira:

				for sprite in self:

					centroy = sprite.image.get_rect().centery
					centrox = sprite.image.get_rect().centerx

					if (centrox + self.x) == (game.static.width / 2):
						self.calculaRota(centrox, centroy)
						self.movRota()

					else:
						self.movPadrao()

			else:
				self.movPadrao()

		self.group.update()

	def movPadrao(self):

		if self.x > game.static.width:
			self.direction = -1
			self.gira = True
		elif self.x < -32:
			self.direction = 1
			self.gira = True

		for sprite in self:
			sprite.rect.x += (self.direction * self.velocidade)
			sprite.image = enemyImage
			self.x = sprite.rect.x
			self.y = sprite.rect.y			

		for sprite in self.group:
			sprite.rect.x += (self.direction * self.velocidade)

	def movRota(self):

		if self.direction == 1:
			if len(self.rota) > (self.umquarto):
				position = self.rota.pop((self.umquarto))
			else:
				position = self.rota.pop(0)
		else:
			if self.umquarto >= 0:
				position = self.rota.pop((self.umquarto))
				self.umquarto -= 1
			else:
				position = self.rota.pop()

		for sprite in self:

			diffX = position[0] - sprite.rect.x
			diffY = position[1] - sprite.rect.y

			self.x = sprite.rect.x
			self.y = sprite.rect.y

			sprite.rect.x += diffX
			sprite.rect.y += diffY
			sprite.image = enemyImage

		for sprite in self.group:
			sprite.rect.x += diffX
			sprite.rect.y += diffY

	def calculaRota(self, centrox, centroy):

		centroyTela = (game.static.height - 50) / 2

		self.gira = False

		r = centroyTela - (self.y + centroy)

		circ = 2 * math.pi * r

		circ = int(circ / self.velocidade)

		self.umquarto = circ / 4

		if centrox < centroyTela:
			self.umquarto *= 3

		qtd = (2 * math.pi) / circ
		atual = qtd

		for i in range(0,circ):
			self.rota.append([(math.cos(atual) * r) - centrox + (game.static.width / 2), (math.sin(atual) * r) - centroy + centroyTela])
			atual += qtd