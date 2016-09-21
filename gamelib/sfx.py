import pygame
from pygame.mixer import Sound
from os import path

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

hit_effects = [Sound(path.join('sounds', 'ouch%d.wav' % i)) for i in range(1,8)]
bulletsound = pygame.mixer.Sound("../Laser_Shoot.wav")