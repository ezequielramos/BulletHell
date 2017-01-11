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

conn = sqlite3.connect('data/data.db')

c = conn.cursor()

x = 0
y = 0
volume = 0

try:
	for row in c.execute('SELECT length, height, volume FROM config'):
		x = row[0]
		y = row[1]
		volume = row[2]

except:

	x = 800
	y = 450
	volume = 0.4

	c.execute("CREATE TABLE config (length integer, height integer, volume decimal)")
	c.execute("INSERT INTO config VALUES (?,?,?)", (x,y, volume))
	conn.commit()

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/main.mp3")
pygame.mixer.music.set_volume(0.5*volume)
pygame.mixer.music.play(-1)

pygame.display.set_mode((x,y))

a = pygame.image.load('images/mainship.png')
pygame.display.set_icon(a)
pygame.display.set_caption("FromZero")

conn.close()

menu.main.mainmenu(pygame)