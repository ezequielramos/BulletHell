import pygame.sprite
from pygame.sprite import Sprite
from pygame import Surface
from gamelib.rgb import WHITEBLUE
from math import sin
from math import cos
from sprites import miscs
from entities import players
from entities import ai
from gamelib.sfx import bulletsound
from gamelib.sfx import hit_effects
from random import randint

class Bullet(Sprite):
	width = 5
	height = 5
	speed = 10
	enemy_entities = None

	def __init__(self, spriteOrigin, angle):
		Sprite.__init__(self, miscs)
		super(Bullet, self).__init__()

		self.image = Surface([self.width, self.height])
		self.image.fill(WHITEBLUE)

		self.rect = self.image.get_rect()

		self.rect.x = spriteOrigin.rect.x + 20
		self.rect.y = spriteOrigin.rect.y

		self.move_y = (-1 * round(sin(angle))) * 10
		self.move_x = (-1 * round(cos(angle))) * 10
		self.spriteOrigin = spriteOrigin
		
		for player in players:
			if spriteOrigin in player:
				self.enemy_entities = ai
				break
		if self.enemy_entities is None:
			self.enemy_entities = players

		bulletsound.play()

	def update(self):
		self.rect.y += self.move_y
		self.rect.x += self.move_x

		# Depending on the direction shot the bullet wont be killed
		if self.rect.y < 0:
			self.kill()
		else:
			for group in self.enemy_entities:
				enemy = pygame.sprite.spritecollideany(self, group)				
				if enemy:
					# This shouldnt be here
					hit_effects[randint(0,6)].play()
					enemy.kill()
					self.kill()
					break
