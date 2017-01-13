import sys
import pygame

bulletImage = pygame.image.load('images/simple_laser_shot_t.png')
backgroundImage = pygame.image.load('images/background.jpg')
enemyImage = pygame.image.load('images/mainship_t_o.png')

pygame.mixer.init() 
bulletsound = pygame.mixer.Sound("sounds/Laser_Shoot.wav")
explosion = pygame.mixer.Sound("sounds/Explosion.wav")

def Play(pygame, player1, bulletSprites):

	#surface = pygame.display.get_surface()
	#surface.fill((51,51,51))


	for event in pygame.event.get():

		if (event.type==pygame.KEYDOWN):

			if (event.key==pygame.K_LEFT or event.key==pygame.K_a):
				player1.pos[0] = True
			if (event.key==pygame.K_RIGHT or event.key==pygame.K_d):
				player1.pos[1] = True
			if (event.key==pygame.K_UP or event.key==pygame.K_w):
				player1.pos[2] = True
			if (event.key==pygame.K_DOWN or event.key==pygame.K_s):
				player1.pos[3] = True

			if event.key == pygame.K_ESCAPE:
				return False

			if (event.key==pygame.K_SPACE):
				bullet = Bullet(player1.rect.x,player1.rect.y)
				bulletSprites.add(bullet)

		if (event.type==pygame.KEYUP):
			if (event.key==pygame.K_LEFT or event.key==pygame.K_a):
				player1.pos[0] = False
			if (event.key==pygame.K_RIGHT or event.key==pygame.K_d):
				player1.pos[1] = False
			if (event.key==pygame.K_UP or event.key==pygame.K_w):
				player1.pos[2] = False
			if (event.key==pygame.K_DOWN or event.key==pygame.K_s):
				player1.pos[3] = False

			pygame.display.update()

		elif event.type == pygame.QUIT:
			pygame.display.quit()
			sys.exit()
			return False

	player1.update()

	return True

def start(pygame):

	pygame.key.set_repeat(199,69)#(delay,interval)
	pygame.display.update()

	FPS = 60

	clock = pygame.time.Clock()

	a = Player(375,400)
	nave = pygame.sprite.Group()
	nave.add(a)

	backgrounds = pygame.sprite.Group()

	background = Background(0,0)
	backgrounds.add(background)

	background = Background(0,-663)
	backgrounds.add(background)

	bulletSprites = pygame.sprite.Group()

	enemies = pygame.sprite.Group()
	enemy = Enemy(375,50)
	enemies.add(enemy)

	surface = pygame.display.get_surface()

	explosions = pygame.sprite.Group()

	while Play(pygame, a, bulletSprites):

		backgrounds.update()
		bulletSprites.update()
		enemies.update()
		explosions.update()

		backgrounds.draw(surface)
		nave.draw(surface)
		bulletSprites.draw(surface)

		collisions = pygame.sprite.groupcollide(enemies,bulletSprites,False,False)

		if collisions:

			for enemy in collisions:
				for bullet in collisions[enemy]:

					enemy.hit(bullet.damage)

					if enemy.heath < 1:

						Explosion(enemy.rect.x,enemy.rect.y,explosions)

						enemies.remove(enemy)
						del enemy

					bulletSprites.remove(bullet)
					del bullet

		explosions.draw(surface)
		enemies.draw(surface)

		pygame.display.flip()
		clock.tick(FPS)
		
class Player(pygame.sprite.Sprite):

	width = 32
	height = 32
	def __init__(self, x, y):

		super(Player,self).__init__()

		self.image = pygame.image.load('images/mainship_t.png')

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

		self.pos = [False,False,False,False]

	def update(self):

		if self.pos[0]:
			self.rect.x = self.rect.x-3
		elif self.pos[1]:
			self.rect.x = self.rect.x+3

		if self.pos[2]:
			self.rect.y = self.rect.y-3
		elif self.pos[3]:
			self.rect.y = self.rect.y+3

class Bullet(pygame.sprite.Sprite):
	width = 3
	height = 6
	damage = 1

	def __init__(self, x, y):

		bulletsound.play()

		super(Bullet,self).__init__()

		self.image = bulletImage

		self.rect = self.image.get_rect()

		self.rect.x = x + 15
		self.rect.y = y

	def update(self):

		self.rect.y = self.rect.y-10

		'''
		all_sprites.remove(self)
		movingsprites.remove(self)
		playerbullets.remove(self)
		del self
		'''

class Background(pygame.sprite.Sprite):
	width = 1178
	height = 663

	def __init__(self, x, y):

		super(Background,self).__init__()

		self.image = backgroundImage

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

	def update(self):

		self.rect.y = self.rect.y+1

		if self.rect.y == 663:
			self.rect.y = -663



class Enemy(pygame.sprite.Sprite):

	width = 32
	height = 32
	heath = 5

	def __init__(self, x, y):

		super(Enemy,self).__init__()

		self.hitimage = pygame.image.load('images/hitted_t.png')

		self.image = enemyImage

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

	def hit(self, damage):
		self.heath = self.heath - damage
		self.image = self.hitimage

	def update(self):
		self.image = enemyImage

class Explosion(pygame.sprite.Sprite):

	width = 32
	height = 32
	fps = 0

	def __init__(self, x, y, sprite_group):

		explosion.play()

		super(Explosion,self).__init__()

		self.image = pygame.image.load('images/explosion_t.png')

		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y
		self.sprite_group = sprite_group

		self.sprite_group.add(self)

	def update(self):
		self.fps += 1

		if self.fps > 30:
			self.sprite_group.remove(self)
			del self