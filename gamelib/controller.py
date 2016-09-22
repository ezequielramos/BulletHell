import pygame

_controllers = set()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SHOOT = 4

class _Default():
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

#This sould inherit the Joystick class
class Joystick(_Default):

	def __init__(self, entity):		
		if pygame.joystick.get_count() == 0:
			raise Exception('Mas q cu!')
		_Default.__init__(self, entity)

		self.joystick = pygame.joystick.Joystick(0)
		self.joystick.init()

	def stroke(self, key):
		axis_x = self.joystick.get_axis(0)
		axis_y = self.joystick.get_axis(1)
		triggers = self.joystick.get_axis(2)#WTF?!?!
		triggers = max(0,(triggers + 1))# 1~== nothing left trigger < 1 > right trigger
		# # 1 can be both as well, no idea how to solve this
		#print(triggers)
		if triggers < 0.4:
			self.entity.react(SHOOT)

		if axis_x > 0.2:
			self.entity.react(RIGHT)
		elif axis_x < -0.2:
			self.entity.react(LEFT)

		if axis_y > 0.2:
			self.entity.react(DOWN)
		elif axis_y < -0.2:
			self.entity.react(UP)

		pass

def broadcast_pressed_key():
	key = pygame.key.get_pressed()
	for controller in _controllers:
		controller.stroke(key)

pygame.joystick.init()
