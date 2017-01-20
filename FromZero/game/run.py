import sys
import pygame
import static
import objects
import HUD

bulletImage = pygame.image.load('images/simple_laser_shot_t.png')
backgroundImage = pygame.image.load('images/background.jpg')

pygame.mixer.init() 
bulletsound = pygame.mixer.Sound("sounds/Laser_Shoot.wav")
explosion = pygame.mixer.Sound("sounds/Explosion.wav")

def Play(pygame, player1, bulletSprites):

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
				bullet = Bullet(player1.imagem.rect.x,player1.imagem.rect.y)
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

	static.score = 0
	static.lifes = 1

	FPS = 60

	clock = pygame.time.Clock()

	nave = Player(375,350)
	#nave = pygame.sprite.Group()
	#nave.add(a)

	gameHud = HUD.HUD()
	gameInfoHud = HUD.score.Score()

	backgrounds = pygame.sprite.Group()

	background = Background(0,0)
	backgrounds.add(background)

	background = Background(0,-663)
	backgrounds.add(background)

	bulletSprites = pygame.sprite.Group()

	#enemies = pygame.sprite.Group()
	enemies = [];

	enemy = objects.enemy.Enemy(50,50)
	enemies.append(enemy)

	enemy = objects.enemy.Enemy(0,50)
	enemies.append(enemy)

	#enemies.add(enemy)

	surface = pygame.display.get_surface()

	gameover = GameOver(surface.get_rect().centerx,surface.get_rect().centery)

	explosions = pygame.sprite.Group()

	while Play(pygame, nave, bulletSprites):

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

					for bullet in collisions[enemySprite]:

						enemy.hit(bullet.damage)

						if enemy.heath < 1:

							Explosion(enemy.x,enemy.y,explosions)

							enemies.remove(enemy)
							del enemy

							static.score += 100

						bulletSprites.remove(bullet)
						del bullet

			else:

				collisions = pygame.sprite.groupcollide(enemy.group,nave.group,False,False)

				if collisions:

					Explosion(nave.imagem.rect.x,nave.imagem.rect.y,explosions)

					enemy.hit(3)

					if enemy.heath < 1:

						Explosion(enemy.x,enemy.y,explosions)

						enemies.remove(enemy)
						del enemy

						static.score += 100

					static.lifes -= 1
					if static.lifes < 0:

						for sprite in nave.group:
							nave.group.remove(sprite)

						for sprite in nave:
							nave.remove(sprite)

					else:
						nave.imagem.rect.x = 375
						nave.imagem.rect.y = 350

						nave.base.rect.x = nave.imagem.rect.x
						nave.base.rect.y = nave.imagem.rect.y + 24
						nave.tronco.rect.x = nave.imagem.rect.x + 14
						nave.tronco.rect.y = nave.imagem.rect.y + 2


		explosions.draw(surface)

		for enemy in enemies:
			enemy.draw(surface)

		gameHud.draw(surface)

		gameInfoHud.update()
		gameInfoHud.draw(surface)

		if len(nave.sprites()) == 0:
			gameover.draw(surface)

		pygame.display.flip()
		clock.tick(FPS)

class GameOver(pygame.sprite.Group):

	def __init__(self,x,y):

		super(GameOver,self).__init__()

		self.font = pygame.font.Font('data/coders_crux/coders_crux.ttf', 64)
		surface = self.font.render("GAME OVER", 1, (255, 255, 153) )

		self.Score = pygame.sprite.Sprite()
		self.Score.image = surface
		self.Score.rect = surface.get_rect()
		self.Score.rect.x = x - surface.get_rect().centerx
		self.Score.rect.y = y - surface.get_rect().centery

		self.add(self.Score)

class Player(pygame.sprite.Group):

	width = 32
	height = 32
	def __init__(self, x, y):

		super(Player,self).__init__()

		self.group = pygame.sprite.Group()
		
		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([self.width, 8])

		base.rect = base.image.get_rect()

		base.rect.x = x
		base.rect.y = y + 24

		self.base = base

		self.group.add(self.base)

		base = pygame.sprite.Sprite()

		base.image = pygame.Surface([6, 22])

		base.rect = base.image.get_rect()

		base.rect.x = x + 14
		base.rect.y = y + 2

		self.tronco = base

		self.group.add(self.tronco)

		self.imagem = pygame.sprite.Sprite()

		self.imagem.image = pygame.image.load('images/mainship_t.png')

		self.imagem.rect = self.imagem.image.get_rect()

		self.imagem.rect.x = x
		self.imagem.rect.y = y

		self.pos = [False,False,False,False]

		self.add(self.imagem)

	def update(self):

		differX = 0
		differY = 0

		if self.pos[0]:
			if self.imagem.rect.x-3 < 0:
				differX = 0
			else:
				differX = -3
		elif self.pos[1]:
			if self.imagem.rect.x+3 > (static.width - 32):
				differX = 0
			else:
				differX = 3

		if self.pos[2]:
			if self.imagem.rect.y-3 < 0:
				differY = 0
			else:
				differY = -3
		elif self.pos[3]:
			if self.imagem.rect.y+3 > (static.height - 50 - 32):
				differY = 0
			else:
				differY = 3

		for sprite in self:
			sprite.rect.x = sprite.rect.x + differX
			sprite.rect.y = sprite.rect.y + differY

		for sprite in self.group:
			sprite.rect.x = sprite.rect.x + differX
			sprite.rect.y = sprite.rect.y + differY

		self.group.update()

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