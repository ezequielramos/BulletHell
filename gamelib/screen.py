from pygame import display
from pygame import Surface
from gamelib.rgb import BLACK

WIDTH = 1024
HEIGHT = 720

screen = display.set_mode([WIDTH, HEIGHT])

background = Surface(screen.get_size())
background = background.convert()

background.fill(BLACK)