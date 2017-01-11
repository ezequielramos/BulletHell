import pygame
from gamelib import rgb
from gamelib.screen import screen
from sprites.base_space_ship import BaseSpaceShip

from gamelib.controller import Keyboard
from gamelib.controller import Joystick
from gamelib.controller import broadcast_event
from gamelib.controller import SHOOT
from gamelib.controller import UP

from sprites import miscs
from entities.player import Player
from entities.basic_enemy import BasicEnemy
from entities import players
from entities import ai

import random

FPS = 60

pygame.display.set_caption('Test')
clock = pygame.time.Clock()

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
	if len(pygame.event.get(pygame.QUIT)) > 0:
		pygame.quit()		
		return False

	miscs.update()
	broadcast_event()

	screen.fill(rgb.BLACK)

	for player in players:
		player.draw(screen)
	for bot in ai:
		bot.draw(screen)

	miscs.draw(screen)
	pygame.display.flip()
	clock.tick(FPS)

	'''if len(ai) == 0:
		print("venceu")
		pygame.quit()
		return False
	el'''
	if len(players) == 0:
		print("seu perdedor")
		pygame.quit()
		return False
	else:
		return True

shit_ai = 25
discard_pile = set()
last_move = UP

stage = 1

while Play():

	if len(ai) == 0:

		for i in range(0,stage):
			BasicEnemy(BaseSpaceShip(coords = (random.randint(1, 8) * 100, 50), colour = rgb.RED))
		
		stage += 1

	#BasicEnemy(BaseSpaceShip(coords = (200, 50), colour = rgb.RED))
	#BasicEnemy(BaseSpaceShip(coords = (500, 50), colour = rgb.RED))

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
