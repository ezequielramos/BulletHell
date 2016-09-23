import pygame

_controllers = set()

# Other joystick events are:
#pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN
_joystickEvts = [pygame.JOYAXISMOTION]
_keyboardEvts = [pygame.KEYDOWN, pygame.KEYUP]


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
#This also should be renamed to XboxJoystick
class Joystick(_Default):

	joy_id = 0
	L_AXIS_X = 0
	L_AXIS_Y = 1
	TRIGGER = 2 

	def __init__(self, entity):		
		if pygame.joystick.get_count() == 0:
			raise Exception('Mas q cu!')
		_Default.__init__(self, entity)

		self.joystick = pygame.joystick.Joystick(self.joy_id)
		self.joystick.init()

	evts_mem = set()

	def stroke(self, evt):
		#Por enquanto so vou gravar os movimentos do axis num tuple (id, value) pq foda-se
		if evt.joy == self.joy_id:
			for stored_evt in self.evts_mem:
				if stored_evt[0] == evt.axis:
					self.evts_mem.discard(stored_evt)
					break
			self.evts_mem.add((evt.axis, evt.value))

	def act(self):
		xunxo_break_shooting = None
		for evt in self.evts_mem:
			etype = evt[0]
			val = evt[1]
			if etype == self.L_AXIS_X:
				self.deal_with_l_axis_x(val)
			elif etype == self.L_AXIS_Y:
				self.deal_with_l_axis_y(val)
			elif etype == self.TRIGGER:
				if self.deal_with_triggers(val):
					xunxo_break_shooting = evt

		if xunxo_break_shooting:
			self.evts_mem.discard(xunxo_break_shooting)

	def deal_with_l_axis_x(self, val):
		if val > 0.2:
			self.entity.react(RIGHT)
		elif val < -0.2:
			self.entity.react(LEFT)

	def deal_with_l_axis_y(self, val):
		if val > 0.2:
			self.entity.react(DOWN)
		elif val < -0.2:
			self.entity.react(UP)
	
	def deal_with_triggers(self, val):
		wtf = max(0,(val + 1))# +-1 == nothing or both | left trigger < 1 > right trigger		
		if round(wtf, 2) <= 0.00:#Right trigger
			self.entity.react(SHOOT)
			return True
		return False

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
