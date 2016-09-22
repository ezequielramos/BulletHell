from gamelib.controller import UP
from gamelib.controller import DOWN
from gamelib.controller import LEFT
from gamelib.controller import RIGHT
from gamelib.controller import SHOOT
from pygame.sprite import GroupSingle
from . import players

class Player(GroupSingle):

	def __init__(self, spaceship):
		GroupSingle.__init__(self)
		self.spaceship = spaceship
		self.add(spaceship)
		players.add(self)

	def react(self, action):
		if len(self.spaceship.groups()) > 0:
			if(action == DOWN): self.spaceship.move(1)
			elif(action == RIGHT): self.spaceship.move(0)
			elif(action == UP): self.spaceship.move(1, False)
			elif(action == LEFT): self.spaceship.move(0, False)
			elif(action == SHOOT): self.spaceship.shoot(90)
		else:			
			players.discard(self)
