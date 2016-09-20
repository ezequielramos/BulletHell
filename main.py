import pygame
import time
from os import path
from pygame.mixer import Sound
from random import randint

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (0, 0, 255)
whiteblue = (150, 200, 255)
red = (255, 0, 0)
green = (0, 255, 0)

players = []

#I'm initialize the mixer manually(pygame.init would initialize it automatically) to be able to load the sound file globally
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096) 
hit_effects = [Sound(path.join('sounds', 'ouch%d.wav' % i)) for i in range(1,8)]
bulletsound = pygame.mixer.Sound("Laser_Shoot.wav")
class Player(pygame.sprite.Sprite):

	width = 50
	height = 50
	my_joystick = None
	step_size = 5

	def __init__(self, x, y, joystick_no):

		super(Player, self).__init__()

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(white)

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

		joystick_count = pygame.joystick.get_count()
		if joystick_count < joystick_no+1:
			print ("Error, I didn't find enough joysticks. Found ", joystick_count)
		else:
			self.my_joystick = pygame.joystick.Joystick(joystick_no)
			self.my_joystick.init()

		all_sprites.add(self)
		movingsprites.add(self)

	def update(self):

		#controle xbox
		if self.my_joystick != None:
			vert_ayis_pos = self.my_joystick.get_axis(0) #x
			vert_axis_pos = self.my_joystick.get_axis(1) #y
		
			if not(vert_axis_pos > -0.2 and vert_axis_pos < 0.2 and vert_ayis_pos > -0.2 and vert_ayis_pos < 0.2):
				self.rect.x = self.rect.x+vert_ayis_pos*10
				self.rect.y = self.rect.y+vert_axis_pos*10

			#cada botao do controle
			'''
			if self.my_joystick.get_button(0):
				self.image.fill(green)
			elif self.my_joystick.get_button(1):
				self.image.fill(red)
			elif self.my_joystick.get_button(2):
				self.image.fill(blue)
			elif self.my_joystick.get_button(3):
				self.image.fill(yellow)
			else:
				self.image.fill(white)'''

		#teclado

	def move(self, axys, forward=True, steps=1):
		self.rect[axys] += ((self.step_size * steps) * (1 if forward else -1))
		
		#self.rect.x = 0
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x + self.width > screen_width:
			self.rect.x = screen_width - self.width

		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y + self.height > screen_height:
			self.rect.y = screen_height - self.height	
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

		self.atirar = (pygame.time.get_ticks() / 1000) * 1000


		self.framescount = 0

		all_sprites.add(self)
		movingsprites.add(self)
		enemies_group.add(self)

	def dispara(self):

		self.bullet = EnemyBullet(self.rect.x,self.rect.y)

	def update(self):
		self.image.fill(red)

		self.framescount += 1

		if self.framescount % 60 == 0:
			self.framescount = 0
			self.dispara()

class Bullet(pygame.sprite.Sprite):
	width = 5
	height = 5
	my_joystick = None

	def __init__(self, x, y):

		bulletsound.play()

		super(Bullet,self).__init__()

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(whiteblue)

		self.rect = self.image.get_rect()

		self.rect.x = x + 24
		self.rect.y = y

		all_sprites.add(self)
		movingsprites.add(self)
		playerbullets.add(self)

	def update(self):
		self.rect.y = self.rect.y-10
		self.image.fill(whiteblue)

		if(self.rect.y < 0):
			all_sprites.remove(self)
			movingsprites.remove(self)
			playerbullets.remove(self)
			del self

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

		all_sprites.add(self)
		movingsprites.add(self)
		enemiesbullets.add(self)

	def update(self):

		self.rect.y = self.rect.y+10
		self.image.fill(green)
		for player in players:
			if self.rect.colliderect(player.rect):
				self.kill()
				hit_effects[randint(0,6)].play()
				break

		if(self.rect.y > screen_height):
			all_sprites.remove(self)
			movingsprites.remove(self)
			enemiesbullets.remove(self)
			del self

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
playerbullets = pygame.sprite.Group()

enemies_group = pygame.sprite.Group()

player1 = Player(275, 500, 0)
players.append(player1)

Enemy(200, 50)

Enemy(500, 50)

clock = pygame.time.Clock()

FPS = 60

def is_moving_up(key): return key[pygame.K_UP] or key[pygame.K_w]
def is_moving_down(key): return key[pygame.K_DOWN] or key[pygame.K_s]
def is_moving_right(key): return key[pygame.K_RIGHT] or key[pygame.K_d]
def is_moving_left(key): return key[pygame.K_LEFT] or key[pygame.K_a]

def Loop():

	global atiro

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
			return False
		elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
			bullet = Bullet(player1.rect.x,player1.rect.y)
			all_sprites.add(bullet)
			movingsprites.add(bullet)

	key = pygame.key.get_pressed()
	
	if(is_moving_down(key)): player1.move(1)
	if(is_moving_right(key)): player1.move(0)
	if(is_moving_up(key)): player1.move(1, False)
	if(is_moving_left(key)): player1.move(0, False)	

	movingsprites.update()

	screen.fill(black)

	all_sprites.draw(screen)

	pygame.display.flip()

	clock.tick(FPS)

	if pygame.sprite.spritecollideany(player1,enemiesbullets):
		print("morreu")
		pygame.quit()
		return False

	pygame.sprite.groupcollide(enemies_group,playerbullets, True, True)

	if len(enemies_group) == 0:
		print("venceu")
		pygame.quit()
		return False

	return True

ret = True

while ret:
	ret = Loop()