import pygame
import game.static

class Lifes(pygame.sprite.Group):

	x = 0
	y = 0

	def __init__(self, mainPath):

		self.noheath = pygame.image.load(mainPath + 'images/no_heath_t.png')
		self.fullheath = pygame.image.load(mainPath + 'images/full_heath_t.png')


		super(Lifes,self).__init__()

		self.x = 200
		self.y = game.static.height - 30

		self.heart = []

		for x in range(0,5):

			imagem = pygame.sprite.Sprite()

			imagem.image = self.noheath
			imagem.rect = imagem.image.get_rect()

			imagem.rect.x = self.x + (17 * x)
			imagem.rect.y = self.y

			self.heart.append(imagem)

			self.add(imagem)

	def update(self):

		for x in range(0,5):

			if x > game.static.lifes-1:
				self.heart[x].image = self.noheath
			else:
				self.heart[x].image = self.fullheath