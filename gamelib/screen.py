from pygame import display
from pygame import Surface
from gamelib.rgb import BLACK

WIDTH = 800
HEIGHT = 600

screen = display.set_mode([WIDTH, HEIGHT])

background = Surface(screen.get_size())
background = background.convert()

background.fill(BLACK)