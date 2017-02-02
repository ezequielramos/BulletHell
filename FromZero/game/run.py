import sys
import pygame
import static
import objects
import HUD

def Play(pygame, player1):

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
					player1.shot()

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

def start(pygame, singlePlayer):

	pygame.key.set_repeat(199,69)#(delay,interval)
	pygame.display.update()

	static.score = 0
	static.lifes = 1

	FPS = 60

	clock = pygame.time.Clock()

	if singlePlayer:
		nave = objects.player.Player(375,350)
	else:
		nave = objects.player.Player(275,350)

	gameHud = HUD.HUD()
	gameInfoHud = HUD.score.Score()
	lifesHud = HUD.lifes.Lifes()

	#backgrounds = objects.background.Background()

	enemies = [];

	for i in range(0,17):

		enemy = objects.enemy.Enemy(-50 + (i*(-50)),50)
		enemies.append(enemy)

	surface = pygame.display.get_surface()

	gameover = HUD.gameover.GameOver(surface.get_rect().centerx,surface.get_rect().centery)

	explosions = objects.explosion.Explosions()

	while Play(pygame, nave):

		#backgrounds.update()

		surface.fill((0,0,0))

		for enemy in enemies:
			enemy.update()

		explosions.update()

		#backgrounds.draw(surface)
		nave.draw(surface)

		nave.bullets.draw(surface)

		for enemy in enemies:

			enemy.update()
			collisions = pygame.sprite.groupcollide(enemy.group,nave.bullets,False,False)

			if collisions:

				enemySprite, bulletsSprites = collisions.popitem()

				for bullet in bulletsSprites:

					try:
						enemy.hit(nave.bullets.damage)

						#abstrair isso aqui
						if enemy.heath < 1:
							explosions.addExplosion(enemy.x,enemy.y)

							enemies.remove(enemy)
							del enemy

							static.score += 100

						nave.bullets.remove(bullet)
						del bullet
					except:

						nave.bullets.remove(bullet)
						del bullet

			else:

				collisions = pygame.sprite.groupcollide(enemy.group,nave.group,False,False)

				if collisions:
					explosions.addExplosion(nave.imagem.rect.x,nave.imagem.rect.y)

					enemy.hit(3)

					if enemy.heath < 1:
						explosions.addExplosion(enemy.x,enemy.y)

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