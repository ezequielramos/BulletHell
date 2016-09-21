from gamelib.controller import UP
from gamelib.controller import DOWN
from gamelib.controller import LEFT
from gamelib.controller import RIGHT
from gamelib.controller import SHOOT

class Player():

	def __init__(self, id, spaceship):
		self.spaceship = spaceship

	def react(self, action):
		if(action == DOWN): self.spaceship.move(1)
		elif(action == RIGHT): self.spaceship.move(0)
		elif(action == UP): self.spaceship.move(1, False)
		elif(action == LEFT): self.spaceship.move(0, False)
		elif(action == SHOOT): self.spaceship.shoot(180)

players = set()