import pygame
from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

import menu
import sqlite3

import pygame
from pygame.mixer import Sound
from os import path

import game

conn = sqlite3.connect('data/data.db')

c = conn.cursor()

try:
	for row in c.execute('SELECT width, height, volume FROM config'):
		game.static.width = row[0]
		game.static.height = row[1]
		game.static.volume = row[2]

except:

	game.static.width = 800
	game.static.height = 450
	game.static.volume = 0.4

	c.execute("CREATE TABLE config (width integer, height integer, volume decimal)")
	c.execute("INSERT INTO config VALUES (?,?,?)", (game.static.width,game.static.height, game.static.volume))
	conn.commit()

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/main.mp3")
pygame.mixer.music.set_volume(0.5*game.static.volume)
pygame.mixer.music.play(-1)

pygame.display.set_mode((game.static.width,game.static.height))

a = pygame.image.load('images/mainship_t.png')
pygame.display.set_icon(a)
pygame.display.set_caption("FromZero")

conn.close()

pygame.mouse.set_visible(False)

menu.main.mainmenu(pygame, game.run, game.static)