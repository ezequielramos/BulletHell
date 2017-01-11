import basic
import sqlite3

def resolutionmenu(pygame):
    import sys

    surface = pygame.display.get_surface()
    surface.fill((51,51,51))

    optionsmenu = basic.Menu(['1280 x 720','800 x 450'], pygame)#necessary
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
                        x = 1280
                        y = 720
                    if optionsmenu.get_position() == 1:
                        x = 800
                        y = 450

                    surface = pygame.display.set_mode((x,y))

                    conn = sqlite3.connect('data/data.db')
                    c = conn.cursor()
                    c.execute("UPDATE config set length = ?, height = ?", (x, y))
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
