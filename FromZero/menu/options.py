import basic
import resolution
import sound

def optionsmenu(pygame):
    import sys
    from pygame.locals import *

    surface = pygame.display.get_surface()
    surface.fill((51,51,51))

    optionsmenu = basic.Menu(['Sound Volume','Keys','Resolution', 'Back'], pygame)#necessary
    optionsmenu.draw()#necessary
    
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()

    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    optionsmenu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    optionsmenu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:

                    if optionsmenu.get_position() == 0:#som
                        sound.soundmenu(pygame)

                    if optionsmenu.get_position() == 1:#keys
                        print "vitoria"

                    if optionsmenu.get_position() == 2:#resolution
                        resolution.resolutionmenu(pygame)

                    if optionsmenu.get_position() == 3:#back
                        loop = False

                    surface.fill((51,51,51))

                    optionsmenu.create_structure()
                    optionsmenu.draw()


                if event.key == K_ESCAPE:
                    loop = False

                pygame.display.update()
            elif event.type == QUIT:

                pygame.display.quit()
                sys.exit()

        pygame.time.wait(8)