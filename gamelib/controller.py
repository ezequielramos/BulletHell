import pygame

_controllers = set()

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
SHOOT = 4

class _Default():
	#actions_dict = dict()

	def __init__(self, entity):
		self.entity = entity
		_controllers.add(self)

	def stroke(self, stroked_keyset):		
		for action in self.actions_dict:						
			keys = self.actions_dict[action]
			for key in keys:
				if stroked_keyset[key]:
					self.entity.react(action)

class Keyboard(_Default):
	actions_dict = {
		UP: [pygame.K_UP, pygame.K_w],
		DOWN: [pygame.K_DOWN, pygame.K_s],
		RIGHT: [pygame.K_RIGHT, pygame.K_d],
		LEFT: [pygame.K_LEFT, pygame.K_a],
		SHOOT: [pygame.K_SPACE]
	}

class Joystick(_Default):
	keys = []

def broadcast_pressed_key():
	key = pygame.key.get_pressed()
	for controller in _controllers:
		controller.stroke(key)