__import__

import pygame
import game.static
import score
import gameover
import lifes

class HUD(pygame.sprite.Group):

	x = 0
	y = 0

	def __init__(self):

		super(HUD,self).__init__()

		self.x = 0
		self.y = game.static.height - 50

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([game.static.width, 50])
		base.image.fill((51,51,51))

		base.rect = base.image.get_rect()

		base.rect.x = self.x
		base.rect.y = self.y

		self.add(base)