import pygame

_controllers = set()

_keyboardEvts = [pygame.KEYDOWN, pygame.KEYUP]
# Other events are:
#pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN
_joystickEvts = [pygame.JOYAXISMOTION]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SHOOT = 4

class _Default():
	def __init__(self, entity):
		self.entity = entity
		_controllers.add(self)

	def receive_evts(self, evts_list):
		for event in evts_list:
			self.stroke(event)

	# This is called when there is an event to be received by the controller.
	def stroke(self, evt):
		pass

	# This is called after stroke so all the events
	# are received and the controller can use them to warn their entity
	def act(self):
		pass

class Keyboard(_Default):
	actions_dict = {
		SHOOT: [pygame.K_SPACE],
		UP: [pygame.K_UP, pygame.K_w],
		DOWN: [pygame.K_DOWN, pygame.K_s],
		RIGHT: [pygame.K_RIGHT, pygame.K_d],
		LEFT: [pygame.K_LEFT, pygame.K_a]		
	}

	keydown_mem = set()

	def stroke(self, evt):
		if evt.type == pygame.KEYDOWN:
			self.keydown_mem.add(evt.key)
		elif evt.type == pygame.KEYUP:
			for keydown in self.keydown_mem:
				if keydown == evt.key:
					self.keydown_mem.discard(keydown)
					break

	def act(self):
		for action in self.actions_dict:
			keys = self.actions_dict[action]
			#Break the shooting shouldn't be here, instead it should be within the entity.
			xunxo_break_shooting = None

			for key in self.keydown_mem:
				if key in keys:
					self.entity.react(action)
					if action == SHOOT:
						xunxo_break_shooting = key

			if xunxo_break_shooting is not None:
				self.keydown_mem.discard(xunxo_break_shooting)


#This sould inherit the Joystick class
class Joystick(_Default):

	def __init__(self, entity):		
		if pygame.joystick.get_count() == 0:
			raise Exception('Mas q cu!')
		_Default.__init__(self, entity)

		self.joystick = pygame.joystick.Joystick(0)
		self.joystick.init()

	def stroke(self, evt):
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

def broadcast_event():	
	if len(_controllers):		
		keyboardEvts = pygame.event.get(_keyboardEvts)
		joystickEvts = pygame.event.get(_joystickEvts)
		
		for controller in _controllers:
			if isinstance(controller, Joystick):				
				controller.receive_evts(joystickEvts)
			else:
				controller.receive_evts(keyboardEvts)
			controller.act()

pygame.joystick.init()
