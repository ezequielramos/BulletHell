import sys
import pygame
import static

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

	a = Player(375,350)
	nave = pygame.sprite.Group()
	nave.add(a)

	gameHud = HUD()

	backgrounds = pygame.sprite.Group()

	background = Background(0,0)
	backgrounds.add(background)

	background = Background(0,-663)
	backgrounds.add(background)

	bulletSprites = pygame.sprite.Group()

	#enemies = pygame.sprite.Group()
	enemies = [];

	enemy = Enemy(50,50)
	enemies.append(enemy)

	enemy = Enemy(0,50)
	enemies.append(enemy)

	#enemies.add(enemy)

	surface = pygame.display.get_surface()

	explosions = pygame.sprite.Group()

	while Play(pygame, a, bulletSprites):

		backgrounds.update()
		bulletSprites.update()

		for enemy in enemies:
			enemy.update()

		explosions.update()

		backgrounds.draw(surface)
		nave.draw(surface)
		bulletSprites.draw(surface)

		for enemy in enemies:

			enemy.update()
			collisions = pygame.sprite.groupcollide(enemy.group,bulletSprites,False,False)

			if collisions:

				for enemySprite in collisions:

					if enemySprite.collidible:

						for bullet in collisions[enemySprite]:

							enemy.hit(bullet.damage)

							if enemy.heath < 1:

								Explosion(enemy.x,enemy.y,explosions)

								enemies.remove(enemy)
								del enemy



							bulletSprites.remove(bullet)
							del bullet

		explosions.draw(surface)

		for enemy in enemies:
			enemy.draw(surface)

		gameHud.draw(surface)

		pygame.display.flip()
		clock.tick(FPS)

class HUD(pygame.sprite.Group):

	x = 0
	y = 0

	def __init__(self):

		super(HUD,self).__init__()

		self.x = 0
		self.y = static.height - 50
		'''self.group = pygame.sprite.Group()
		self.hitimage = pygame.image.load('images/hitted_t.png')'''

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([static.width, 50])
		base.image.fill((51,51,51))

		base.rect = base.image.get_rect()

		base.rect.x = self.x
		base.rect.y = self.y

		self.add(base)

	def update(self):

		for sprite in self:
			sprite.rect.x = sprite.rect.x + 1
			sprite.image = enemyImage

		for sprite in self.group:
			sprite.rect.x = sprite.rect.x + 1

		self.x = self.x + 1

		self.group.update()
		
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
			if self.rect.x-3 < 0:
				self.rect.x = 0
			else:
				self.rect.x = self.rect.x-3
		elif self.pos[1]:
			if self.rect.x+3 > (static.width - 32):
				self.rect.x = static.width - 32
			else:
				self.rect.x = self.rect.x+3

		if self.pos[2]:
			if self.rect.y-3 < 0:
				self.rect.y = 0
			else:
				self.rect.y = self.rect.y-3
		elif self.pos[3]:
			if self.rect.y+3 > (static.height - 50 - 32):
				self.rect.y = static.height - 50 - 32
			else:
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



class Enemy(pygame.sprite.Group):

	width = 32
	height = 32
	heath = 5

	def __init__(self, x, y):

		super(Enemy,self).__init__()

		self.x = x
		self.y = y
		self.group = pygame.sprite.Group()
		self.hitimage = pygame.image.load('images/hitted_t.png')

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([self.width, 8])

		base.rect = base.image.get_rect()

		base.rect.x = x
		base.rect.y = y
		base.collidible = True

		self.group.add(base)

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([6, 22])

		base.rect = base.image.get_rect()

		base.rect.x = x + 14
		base.rect.y = y + 8
		base.collidible = True

		self.group.add(base)

		imagem = pygame.sprite.Sprite()

		imagem.image = enemyImage
		imagem.rect = imagem.image.get_rect()

		imagem.rect.x = x
		imagem.rect.y = y

		imagem.collidible = False

		self.add(imagem)

	def hit(self, damage):
		self.heath = self.heath - damage

		for sprite in self:
			sprite.image = self.hitimage

	def update(self):

		for sprite in self:
			sprite.rect.x = sprite.rect.x + 1
			sprite.image = enemyImage

		for sprite in self.group:
			sprite.rect.x = sprite.rect.x + 1

		self.x = self.x + 1

		self.group.update()



class Explosion(pygame.sprite.Sprite):

	width = 32
	height = 32
	fps = 0

	def __init__(self, x, y, sprite_group):

		explosion.play()

		static.score += 10
		print static.score

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