from . import basic
from pygame.locals import *

def coopmenu(pygame, game, mainPath):

    def host():
        game.start(pygame, False, mainPath)
        return True

    def join():
        print("join")
        return True

    def back():
        return False

    surface = pygame.display.get_surface()
    surface.fill((51,51,51))

    mainmenu = basic.Menu(['Host', 'Join', 'Back'], pygame, mainPath)

    menuFunctions = [host,join,back]

    mainmenu.draw()
    
    pygame.key.set_repeat(199,69)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    mainmenu.draw(-1) 
                if event.key == K_DOWN:
                    mainmenu.draw(1)
                if event.key == K_RETURN:

                    ret = menuFunctions[mainmenu.get_position()]()

                    if not ret:
                        return False

                    surface.fill((51,51,51))

                    mainmenu.create_structure()
                    mainmenu.draw()

                if event.key == K_ESCAPE:
                    return False
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(8)