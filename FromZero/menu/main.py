from . import basic
from . import options
from . import coop
import sys
from pygame.locals import *

def mainmenu(pygame, game, static):

    def singleplayer():
        game.start(pygame, True)
        return True

    def coopMenu():
        coop.coopmenu(pygame, game)
        return True

    def optionsMenu():
        options.optionsmenu(pygame)
        return True

    def quit():
        pygame.display.quit()
        sys.exit()
        return False

    surface = pygame.display.get_surface()
    surface.fill((51,51,51))

    mainmenu = basic.Menu(['Singleplayer', 'Co-op','Options','Quit'], pygame)#necessary

    menuFunctions = [singleplayer,coopMenu,optionsMenu,quit]

    mainmenu.draw()#necessary
    
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    mainmenu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    mainmenu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:

                    ret = menuFunctions[mainmenu.get_position()]()

                    if not ret:
                        return False

                    surface.fill((51,51,51))

                    mainmenu.create_structure()
                    mainmenu.draw()

                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(8)