import pygame
from gamelib import rgb
from sprites.base_space_ship import BaseSpaceShip
from gamelib.controller import Keyboard
from gamelib.controller import broadcast_pressed_key
from gamelib.player import Player

from sprites import players
from sprites import enemies
from sprites import miscs

#from sprites.bullet import Bullet

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Test')

background = pygame.Surface(screen.get_size())
background = background.convert()

background.fill(rgb.BLACK)

clock = pygame.time.Clock()

FPS = 60

BaseSpaceShip(enemies, coords = (200, 50), colour = rgb.RED)
BaseSpaceShip(enemies, coords = (500, 50), colour = rgb.RED)

Keyboard(
	Player(0, BaseSpaceShip(players, (275, 500)))
)

def Play():

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			return False

	miscs.update()
	broadcast_pressed_key()

	screen.fill(rgb.BLACK)

	players.draw(screen)
	enemies.draw(screen)
	miscs.draw(screen)

	pygame.display.flip()

	clock.tick(FPS)

	if len(enemies) == 0:
		print("venceu")
		pygame.quit()
		return False

	return True

while Play():
	pass
