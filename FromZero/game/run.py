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

			if event.key == pygame.K_ESCAPE:
				return False

			if static.lifes >= 0:

				if (event.key==pygame.K_LEFT or event.key==pygame.K_a):
					player1.pos[0] = True
				if (event.key==pygame.K_RIGHT or event.key==pygame.K_d):
					player1.pos[1] = True
				if (event.key==pygame.K_UP or event.key==pygame.K_w):
					player1.pos[2] = True
				if (event.key==pygame.K_DOWN or event.key==pygame.K_s):
					player1.pos[3] = True

				if (event.key==pygame.K_SPACE):
					bullet = Bullet(player1.imagem.rect.x,player1.imagem.rect.y, bulletSprites)
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

	nave = objects.player.Player(375,350)
	#nave = pygame.sprite.Group()
	#nave.add(a)

	gameHud = HUD.HUD()
	gameInfoHud = HUD.score.Score()
	lifesHud = HUD.lifes.Lifes()

	backgrounds = pygame.sprite.Group()

	background = Background(0,0)
	backgrounds.add(background)

	background = Background(0,-663)
	backgrounds.add(background)

	bulletSprites = pygame.sprite.Group()

	#enemies = pygame.sprite.Group()
	enemies = [];

	for i in range(0,17):

		enemy = objects.enemy.Enemy(-50 + (i*(-50)),50)
		enemies.append(enemy)

	#enemies.add(enemy)

	surface = pygame.display.get_surface()

	gameover = HUD.gameover.GameOver(surface.get_rect().centerx,surface.get_rect().centery)

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

		lifesHud.update()
		lifesHud.draw(surface)

		if len(nave.sprites()) == 0:
			gameover.draw(surface)

		pygame.display.flip()
		clock.tick(FPS)

class Bullet(pygame.sprite.Sprite):
	width = 3
	height = 6
	damage = 1

	def __init__(self, x, y, bulletSprites):

		bulletsound.play()

		super(Bullet,self).__init__()

		self.bulletSprites = bulletSprites

		self.image = bulletImage

		self.rect = self.image.get_rect()

		self.rect.x = x + 15
		self.rect.y = y

	def update(self):

		self.rect.y = self.rect.y-10

		if self.rect.y < 6:
			self.bulletSprites.remove(self)
			del self

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