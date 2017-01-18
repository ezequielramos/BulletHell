import basic
import options

def mainmenu(pygame, game):
    import sys
    from pygame.locals import *

    surface = pygame.display.get_surface()
    surface.fill((51,51,51))

    mainmenu = basic.Menu(['Start','Options','Quit'], pygame)#necessary
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

                    if mainmenu.get_position() == 0:#start
                        game.start(pygame)

                    if mainmenu.get_position() == 1:#options

                        options.optionsmenu(pygame)

                    if mainmenu.get_position() == 2:#quit
                        pygame.display.quit()
                        sys.exit()
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