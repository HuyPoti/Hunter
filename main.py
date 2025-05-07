import pygame
import sys
from os.path import join
from module.Level import Level
from utils.settings import *  
from pytmx.util_pygame import load_pygame
from utils.support import *
from ui.menu import Menu
from ui.end_screen import EndScreen

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hunter')
        pygame.display.set_icon(pygame.image.load(join('.', 'assets', 'icon.png')))
        self.import_assets()
        # self.level = Level(self.tmx_maps)
        self.level = None
        self.menu = Menu(self.display_surface)
        self.end_screen = None
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        pygame.mixer.music.load(join('assets', 'music', 'music.mp3'))

        pygame.mixer.music.set_volume(0.5)
    def import_assets(self):  
        self.tmx_maps = {
            'map1': load_pygame(join('.', 'maps', 'map1.tmx')),
            'map2': load_pygame(join('.', 'maps', 'map2.tmx')),
            'map3': load_pygame(join('.', 'maps', 'map3.tmx')),
            'map4': load_pygame(join('.', 'maps', 'map4.tmx')),
            'map5': load_pygame(join('.', 'maps', 'map5.tmx'))
            }

    def run(self):
        in_menu = True
        in_game = False
        in_end_screen = False
        result = None
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if in_menu:
                # Hiển thị menu
                result = self.menu.run()
           

                if result == "play":
                    self.level = Level(self.tmx_maps)  # Bắt đầu trò chơi
                    in_game = True
                    in_menu = False
                elif result == "musicon":
                    pygame.mixer.music.play(-1)
                elif result == "musicoff":
                    pygame.mixer.music.stop()
                elif result == "quit":
                    pygame.quit()
                    sys.exit()
            elif in_game:
                self.level.run(dt)
                if self.level.player.hp <= 0:  # Người chơi thua
                    result = "lose"
                    in_game = False
                    in_end_screen = True
                    self.end_screen = EndScreen(self.display_surface, result)
                elif all(house.destroyed for house in self.level.monster_houses) and self.level.transition_check():  # Người chơi thắng
                    result = "win"
                    in_game = False
                    in_end_screen = True
                    self.end_screen = EndScreen(self.display_surface, result)

            elif in_end_screen:
                result = self.end_screen.run()
                if result == "play_again":
                    self.level = Level(self.tmx_maps)  # Tạo lại cấp độ
                    in_end_screen = False
                    in_menu = True
                elif result == "quit":
                    pygame.quit()
                    exit()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()