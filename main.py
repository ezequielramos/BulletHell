import pygame
import random
import time
import threading

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (0, 0, 255)
whiteblue = (150, 200, 255)
red = (255, 0, 0)
green = (0, 255, 0)

class Player(pygame.sprite.Sprite):

	width = 50
	height = 50
	my_joystick = None

	def __init__(self, x, y, joystick_no):

		super(Player,self).__init__()

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(white)

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

		self.pos = [False,False,False,False]

		joystick_count = pygame.joystick.get_count()
		if joystick_count < joystick_no+1:
			print ("Error, I didn't find enough joysticks. Found ", joystick_count)
		else:
			self.my_joystick = pygame.joystick.Joystick(joystick_no)
			self.my_joystick.init()

	def update(self):

		#controle xbox
		if self.my_joystick != None:
			vert_ayis_pos = self.my_joystick.get_axis(0) #x
			vert_axis_pos = self.my_joystick.get_axis(1) #y
		
			if not(vert_axis_pos > -0.2 and vert_axis_pos < 0.2 and vert_ayis_pos > -0.2 and vert_ayis_pos < 0.2):
				self.rect.x = self.rect.x+vert_ayis_pos*10
				self.rect.y = self.rect.y+vert_axis_pos*10

				if self.rect.y < 0:
					self.rect.y = 0
				if self.rect.y > screen_height - self.height:
					self.rect.y = screen_height - self.height

			if self.my_joystick.get_button(0):
				self.image.fill(green)
			elif self.my_joystick.get_button(1):
				self.image.fill(red)
			elif self.my_joystick.get_button(2):
				self.image.fill(blue)
			elif self.my_joystick.get_button(3):
				self.image.fill(yellow)
			else:
				self.image.fill(white)

		#teclado
		else:

			if self.pos[0]:
				self.rect.x = self.rect.x-5
			elif self.pos[1]:
				self.rect.x = self.rect.x+5

			if self.pos[2]:
				self.rect.y = self.rect.y-5
			elif self.pos[3]:
				self.rect.y = self.rect.y+5

			self.image.fill(white)

class Enemy(pygame.sprite.Sprite):

	width = 50
	height = 50

	def __init__(self, x, y):

		super(Enemy,self).__init__()

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(red)

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

		self.running = True

		self.atirar = (pygame.time.get_ticks() / 1000) * 1000

	#removido de uma thread separada, porem ainda por tempo(1 segundo)... verificar se consigo fazer por Frames(60)
	def dispara(self):

		self.bullet = EnemyBullet(self.rect.x,self.rect.y)

		all_sprites.add(self.bullet)
		movingsprites.add(self.bullet)
		enemiesbullets.add(self.bullet)

	def update(self):
		self.image.fill(red)

		numero = ((pygame.time.get_ticks() - self.atirar) / 1000) * 1000

		if numero >= 1000:
			self.atirar += numero
			print(self.atirar)
			self.dispara()

class Bullet(pygame.sprite.Sprite):
	width = 5
	height = 5
	my_joystick = None

	def __init__(self, x, y):

		super(Bullet,self).__init__()

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(whiteblue)

		self.rect = self.image.get_rect()

		self.rect.x = x + 24
		self.rect.y = y

	def update(self):

		self.rect.y = self.rect.y-10

		self.image.fill(whiteblue)

class EnemyBullet(pygame.sprite.Sprite):

	width = 5
	height = 5
	my_joystick = None

	def __init__(self, x, y):

		super(EnemyBullet,self).__init__()

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(green)

		self.rect = self.image.get_rect()

		self.rect.x = x + 24
		self.rect.y = y + 50

	def update(self):

		self.rect.y = self.rect.y+10

		self.image.fill(green)

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Test')

background = pygame.Surface(screen.get_size())

background = background.convert()

background.fill(black)

all_sprites = pygame.sprite.Group()
movingsprites = pygame.sprite.Group()
enemiesbullets = pygame.sprite.Group()

player1 = Player(375, 500, 0)

all_sprites.add(player1)
movingsprites.add(player1)

clock = pygame.time.Clock()

stage = 1
enemies = []

FPS = 60

def Loop():

	global atiro

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			for enemy in enemies:
				enemy.running = False
			pygame.quit()
			return False

		if (event.type==pygame.KEYDOWN):

			if (event.key==pygame.K_LEFT or event.key==pygame.K_a):
				player1.pos[0] = True
			if (event.key==pygame.K_RIGHT or event.key==pygame.K_d):
				player1.pos[1] = True
			if (event.key==pygame.K_UP or event.key==pygame.K_w):
				player1.pos[2] = True
			if (event.key==pygame.K_DOWN or event.key==pygame.K_s):
				player1.pos[3] = True

			if (event.key==pygame.K_SPACE):
				bullet = Bullet(player1.rect.x,player1.rect.y)
				all_sprites.add(bullet)
				movingsprites.add(bullet)

		if (event.type==pygame.KEYUP):
			if (event.key==pygame.K_LEFT or event.key==pygame.K_a):
				player1.pos[0] = False
			if (event.key==pygame.K_RIGHT or event.key==pygame.K_d):
				player1.pos[1] = False
			if (event.key==pygame.K_UP or event.key==pygame.K_w):
				player1.pos[2] = False
			if (event.key==pygame.K_DOWN or event.key==pygame.K_s):
				player1.pos[3] = False

	while len(enemies) < stage:
		aenemy = Enemy(375, 50)
		enemies.append(aenemy)
		all_sprites.add(aenemy)
		movingsprites.add(aenemy)

	movingsprites.update()

	screen.fill(black)

	all_sprites.draw(screen)

	pygame.display.flip()

	clock.tick(FPS)

	return True

ret = True

while ret:
	ret = Loop()