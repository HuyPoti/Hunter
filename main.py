import pygame
import sys
from os.path import join
from module.Level import Level
from utils.settings import *  
from pytmx.util_pygame import load_pygame
from utils.support import *
from ui.menu import Menu  

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hunter')
        pygame.display.set_icon(pygame.image.load(join('.', 'assets', 'icon.png')))
        
        # Tạo menu từ lớp Menu
        self.menu = Menu(self.display_surface)
        self.game_state = "menu"  # 'menu' hoặc 'playing'
        
        # Tải các tài nguyên game
        self.import_assets()
        self.current_stage = Level(self.tmx_maps[1])
        self.clock = pygame.time.Clock()

    def import_assets(self):
        self.tmx_maps = {
            1: load_pygame(join('.', 'maps', 'map1.tmx')),
            2: load_pygame(join('.', 'maps', 'map2.tmx')),
            3: load_pygame(join('.', 'maps', 'map3.tmx')),
            4: load_pygame(join('.', 'maps', 'map4.tmx')),
            5: load_pygame(join('.', 'maps', 'map5.tmx'))
        }

    def run(self):
        while True:
            dt = self.clock.tick() / 1000  # Delta time
            for event in pygame.event.get():
                if self.game_state == "menu":
                    action = self.menu.handle_event(event)
                    if action == "quit":
                        pygame.quit()
                        sys.exit()
                elif self.game_state == "playing":
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            # Xử lý trạng thái game
            if self.game_state == "menu":
                action = self.menu.run()
                if action == "quit":
                    pygame.quit()
                    sys.exit()
                elif action == "play":
                    self.game_state = "playing"
            elif self.game_state == "playing":
                self.current_stage.run(dt)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()