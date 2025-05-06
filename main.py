import pygame
import sys
from os.path import join
from module.Level import Level
from utils.settings import *  
from pytmx.util_pygame import load_pygame
from utils.support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hunter')
        pygame.display.set_icon(pygame.image.load(join('.', 'assets', 'icon.png')))
        self.import_assets()
        self.level = Level(self.tmx_maps)
        self.clock = pygame.time.Clock()
    def import_assets(self):  
        self.tmx_maps = {
            'map1': load_pygame(join('.', 'maps', 'map1.tmx')),
            'map2': load_pygame(join('.', 'maps', 'map2.tmx')),
            'map3': load_pygame(join('.', 'maps', 'map3.tmx')),
            'map4': load_pygame(join('.', 'maps', 'map4.tmx')),
            'map5': load_pygame(join('.', 'maps', 'map5.tmx'))
            }

    def run(self):
        while True:
            dt = self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.level.run(dt) 
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()