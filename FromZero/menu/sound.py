from . import basic
import sqlite3
import game

def soundmenu(pygame, mainPath):
    import sys

    surface = pygame.display.get_surface()
    surface.fill((51,51,51))

    optionsmenu = basic.Menu(['100%','80%','60%','40%','20%','Muted'], pygame, mainPath)#necessary
    optionsmenu.draw()
    
    pygame.key.set_repeat(199,69)
    pygame.display.update()

    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_UP:
                    optionsmenu.draw(-1) 
                if event.key == pygame.locals.K_DOWN:
                    optionsmenu.draw(1) 
                if event.key == pygame.locals.K_RETURN:

                    if optionsmenu.get_position() == 0:
                        game.static.volume = 1
                    if optionsmenu.get_position() == 1:
                        game.static.volume = 0.8
                    if optionsmenu.get_position() == 2:
                        game.static.volume = 0.6
                    if optionsmenu.get_position() == 3:
                        game.static.volume = 0.4
                    if optionsmenu.get_position() == 4:
                        game.static.volume = 0.2
                    if optionsmenu.get_position() == 5:
                        game.static.volume = 0

                    pygame.mixer.music.set_volume(0.5*game.static.volume)

                    conn = sqlite3.connect(mainPath + 'data/data.db')
                    c = conn.cursor()
                    c.execute("UPDATE config set volume = ?", (game.static.volume, ))
                    conn.commit()
                    conn.close()

                    loop = False

                if event.key == pygame.locals.K_ESCAPE:
                    loop = False

                pygame.display.update()
            elif event.type == pygame.locals.QUIT:

                pygame.display.quit()
                sys.exit()

        pygame.time.wait(8)
