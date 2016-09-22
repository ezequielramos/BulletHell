import pygame
from pygame.mixer import Sound
from os import path

uri = 'sounds'

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

hit_effects = [Sound(path.join(uri, 'ouch%d.wav' % i)) for i in range(1,8)]
bulletsound = Sound(path.join(uri, "Laser_Shoot.wav"))

bulletsound.set_volume(0.05)