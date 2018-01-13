import pygame

class GameOver(pygame.sprite.Group):

	def __init__(self,x,y, mainPath):

		super(GameOver,self).__init__()

		self.font = pygame.font.Font(mainPath + 'data/coders_crux/coders_crux.ttf', 64)
		surface = self.font.render("GAME OVER", 1, (255, 255, 153) )

		self.Score = pygame.sprite.Sprite()
		self.Score.image = surface
		self.Score.rect = surface.get_rect()
		self.Score.rect.x = x - surface.get_rect().centerx
		self.Score.rect.y = y - surface.get_rect().centery

		self.add(self.Score)