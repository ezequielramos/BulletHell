class Surface:

    def __init__(self, pygame):    
        text = ''
        surface = pygame.Surface
        surface_rect = pygame.Rect
        select_rect = pygame.Rect

class Menu:

    def __init__(self, list, pygame, mainPath):

        self.list = []
        self.flap = []
        self.font_size = 32
        self.mainPath = mainPath
        self.font_path = 'data/coders_crux/coders_crux.ttf'
        self.font = pygame.font.Font
        self.dest_surface = pygame.display.get_surface()
        self.quantity_pol = 0
        self.background_color = (51,51,51)
        self.text_color =  (255, 255, 153)
        self.selected_color = (153,102,255)
        self.position_selected = 0
        self.menu_width = 0
        self.menu_height = 0
        self.pygame = pygame

        self.list = list
        self.quantity_pol = len(self.list)

        self.create_structure()

    def move_menu(self, top, left):
        self.position_paste = (top,left) 

    def set_colors(self, text, selection, background):
        self.background_color = background
        self.text_color =  text
        self.selected_color = selection
        
    def set_fontsize(self,font_size):
        self.font_size = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.position_selected
        
    def draw(self,move=0):

        if move:
            self.position_selected += move 
            if self.position_selected == -1:
                self.position_selected = self.quantity_pol - 1
            self.position_selected %= self.quantity_pol
        menu = self.pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.background_color)
        select_rect = self.flap[self.position_selected].select_rect
        self.pygame.draw.rect(menu,self.selected_color,select_rect)

        for i in range(self.quantity_pol):
            menu.blit(self.flap[i].surface,self.flap[i].surface_rect)
        self.pygame.display.get_surface().blit(menu,self.position_paste)
        return self.position_selected

    def create_structure(self):

        self.position_paste = (0,0)

        movement = 0
        self.menu_height = 0
        self.font = self.pygame.font.Font(self.mainPath + self.font_path, self.font_size)
        for i in range(self.quantity_pol):
            self.flap.append(Surface(self.pygame))
            self.flap[i].text = self.list[i]
            self.flap[i].surface = self.font.render(self.flap[i].text, 1, self.text_color)

            self.flap[i].surface_rect = self.flap[i].surface.get_rect()
            movement = int(self.font_size * 0.2)

            height = self.flap[i].surface_rect.height
            self.flap[i].surface_rect.left = movement
            self.flap[i].surface_rect.top = movement+(movement*2+height)*i

            width = self.flap[i].surface_rect.width+movement*2
            height = self.flap[i].surface_rect.height+movement*2            
            left = self.flap[i].surface_rect.left-movement
            top = self.flap[i].surface_rect.top-movement

            self.flap[i].select_rect = (left,top ,width, height)
            if width > self.menu_width:
                self.menu_width = width
            self.menu_height += height

        x = self.pygame.display.get_surface().get_rect().centerx - self.menu_width / 2
        y = self.pygame.display.get_surface().get_rect().centery - self.menu_height / 2
        mx, my = self.position_paste
        self.position_paste = (x+mx, y+my) 