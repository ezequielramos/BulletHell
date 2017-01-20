import pygame
import game.static

class Score(pygame.sprite.Group):

	x = 0
	y = 0

	def __init__(self):

		super(Score,self).__init__()

		self.x = 0
		self.y = game.static.height - 50

		self.font = pygame.font.Font('data/coders_crux/coders_crux.ttf', 32)
		surface = self.font.render("Score: " + str(game.static.score).zfill(7), 1, (255, 255, 153) )

		self.Score = pygame.sprite.Sprite()
		self.Score.image = surface
		self.Score.rect = surface.get_rect()
		self.Score.rect.x = self.x + 15
		self.Score.rect.y = game.static.height - 30

		self.add(self.Score)

	def update(self):

		surface = self.font.render("Score: " + str(game.static.score).zfill(7), 1, (255, 255, 153) )
		self.Score.image = surface
		self.Score.rect = surface.get_rect()
		self.Score.rect.x = self.x + 15
		self.Score.rect.y = game.static.height - 30