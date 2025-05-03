from utils.settings import *
from module.sprites import Sprite, Animation, BorderSprite, CollidableSprite
from engine.entity import Player, Character
from engine.groups import AllSprites
from utils.support import *
from data.game_data import *
from ui.dialog import DialogTree
import pygame

class Level:
    def __init__(self, tmx_maps):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.overworld_frames = {
            'foam': import_tilemap('assets', 'sprites', 'Terrain', 'Water', 'Foam', 'Foam'),
            'character': import_all_characters('assets', 'sprites', 'Factions', 'Knights', 'Player')
        }
        self.fonts = {
            'dialog' : pygame.font.Font(join('assets', 'font', 'PixelifySans.ttf'), 20)
        }
        self.setup(tmx_maps, 'start')
        self.dialog_tree = None
        
    def setup(self, tmx_map, player_start_pos):
    
        # for layer in tmx_map.layers:
        #     if hasattr(layer, 'tiles'):  
        #         for x, y, surf in layer.tiles():
        #             Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
        for x, y, surf in tmx_map.get_layer_by_name('Water').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['water'])

        for obj in tmx_map.get_layer_by_name('Foam'):
            Animation((obj.x, obj.y) , self.overworld_frames['foam'], self.all_sprites, WORLD_LAYERS['foam'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Flat_Beach').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Grass').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Rock').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['foam'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Elevation').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites), WORLD_LAYERS['main'])
        
        for obj in tmx_map.get_layer_by_name('Object'):
            CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in tmx_map.get_layer_by_name('Collision'):
            BorderSprite((obj.x, obj.y),  pygame.Surface((int(obj.width), int(obj.height))), self.collision_sprites)
        
        for obj in tmx_map.get_layer_by_name('Position'):
            if obj.name == 'Player' and 'pos' in obj.properties and obj.properties['pos'] == player_start_pos:
                self.player = Player(
                    (obj.x, obj.y), 
                    self.overworld_frames['character']['Archer'], 
                    self.all_sprites, 'stand_right', 
                    self.collision_sprites)
                
            elif obj.name == 'Character':
                Character(
                    (obj.x, obj.y),
                    self.overworld_frames['character'][obj.properties['graphic']],
                    (self.all_sprites, self.collision_sprites, self.character_sprites),
                    obj.properties['direction'],
                    obj.properties['character_type'],
                    DIALOG_DATA[obj.properties['character_id']])
    def input(self):
        if not self.dialog_tree:
            keys = pygame.key.get_just_pressed()
            input_vector = vector()
            if keys[pygame.K_n]:
                for character in self.character_sprites:
                    if check_connection(80, self.player, character):
                        # block player input
                        self.player.block()
                        # entities face each other
                        character.change_facing_direction(self.player.rect.center)
                        #create dialog
                        self.create_dialog(character)
    def create_dialog(self, character):
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'])
    def run(self, dt):
        self.display_surface.fill('black') 
        self.all_sprites.update(dt) 
        self.all_sprites.draw(self.player.rect.center)
        self.input()
        if self.dialog_tree: self.dialog_tree.update()