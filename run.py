import pygame
from gamelib import rgb
from gamelib.screen import screen
from sprites.base_space_ship import BaseSpaceShip

from gamelib.controller import Keyboard
from gamelib.controller import Joystick
from gamelib.controller import broadcast_pressed_key
from gamelib.controller import SHOOT
from gamelib.controller import UP

from sprites import miscs
from entities.player import Player
from entities.basic_enemy import BasicEnemy
from entities import players
from entities import ai

FPS = 60

pygame.display.set_caption('Test')
clock = pygame.time.Clock()

BasicEnemy(BaseSpaceShip(coords = (200, 50), colour = rgb.RED))
BasicEnemy(BaseSpaceShip(coords = (500, 50), colour = rgb.RED))

Keyboard(
	Player(BaseSpaceShip(coords = (275, 500)))
)

try:
	jk_player = Player(BaseSpaceShip(coords = (375, 500), colour = rgb.GREEN))
	Joystick(jk_player)
except Exception:
	jk_player.spaceship.kill()
	jk_player.react(UP)
	pass

def Play():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			return False

	miscs.update()
	broadcast_pressed_key()

	screen.fill(rgb.BLACK)

	for player in players:
		player.draw(screen)
	for bot in ai:
		bot.draw(screen)

	miscs.draw(screen)
	pygame.display.flip()
	clock.tick(FPS)

	if len(ai) == 0:
		print("venceu")
		pygame.quit()
		return False
	elif len(players) == 0:
		print("seu perdedor")
		pygame.quit()
		return False
	else:
		return True

shit_ai = 25
discard_pile = set()
last_move = UP
while Play():
	shit_ai -= 1
	if shit_ai <= 0:
		if last_move == SHOOT:
			last_move = UP

		for bot in ai:
			if bot.dead is False:
				bot.react(last_move)
				bot.react(SHOOT)
			else:
				discard_pile.add(bot)

		last_move += 1
		for bot in discard_pile:
			ai.discard(bot)
		shit_ai = 25
	pass
