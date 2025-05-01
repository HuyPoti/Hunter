from utils.settings import *
from module.sprites import Sprite, Animation
from engine.entity import Player
from engine.groups import AllSprites
from utils.support import *
import pygame

class Level:
    def __init__(self, tmx_maps):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()
        self.overworld_frames = {
            'foam': import_tilemap('assets', 'sprites', 'Terrain', 'Water', 'Foam', 'Foam')
        }
        self.setup(tmx_maps, 'start')
        
    def setup(self, tmx_map, player_start_pos):
    
        for layer in tmx_map.layers:
            if hasattr(layer, 'tiles'):  
                for x, y, surf in layer.tiles():
                    if (layer.name == 'Foam'):
                        Animation((x * TILE_SIZE, y * TILE_SIZE), self.overworld_frames['foam'], self.all_sprites)
                    else:
                        Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)  
        for obj in tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)
        for obj in tmx_map.get_layer_by_name('Position'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites)
        
                
    def run(self, dt):
        self.display_surface.fill('black') 
        self.all_sprites.update(dt) 
        self.all_sprites.draw(self.player.rect.center)