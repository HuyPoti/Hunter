from utils.settings import *

from module.sprites import Sprite, Animation, BorderSprite, CollidableSprite, BothSprite, TransitionSprite
from module.monster import Monster, MonsterHouse, tnt
from engine.entity import Player, Character, Arrow, Coin, Meat
from engine.groups import AllSprites
from utils.support import *
from data.game_data import *
from ui.dialog import DialogTree
from ui.end_screen import EndScreen
import pygame

class Level:
    def __init__(self, tmx_maps):
        self.display_surface = pygame.display.get_surface()
        self.tmx_maps = tmx_maps
#         self.all_sprites = AllSprites()
#         self.collision_sprites = pygame.sprite.Group()
#         self.character_sprites = pygame.sprite.Group()
#         self.arrow_sprites = pygame.sprite.Group()  # Nhóm để chứa các mũi tên (projectiles)
        self.transition_sprites = pygame.sprite.Group()

        self.transition_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600
        self.current_map = 'map1'
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()  # Nhóm để chứa các mũi tên (projectiles)
        self.monsters = pygame.sprite.Group()  # Nhóm cho quái
        self.monster_houses = pygame.sprite.Group()  # Nhóm cho nhà quái
        self.items = pygame.sprite.Group()  # Nhóm cho tiền và thịt

        self.overworld_frames = {
            'foam': import_folder('animation', 'resource', 'foam'),
            'rock': import_folder('animation', 'resource', 'rock'),
            'tree': import_folder('animation', 'resource', 'tree'),
            'fire': import_folder('animation', 'resource', 'fire'),
            'character': import_all_characters('animation', 'character', 'player'),
            'meat': import_folder('animation', 'resource', 'meat')
        }
        self.fonts = {
            'dialog': pygame.font.Font(join('assets', 'font', 'PixelifySans.ttf'), 20)
        }
        self.setup(self.tmx_maps[self.current_map], 'start')
        self.dialog_tree = None
        
    def setup(self, tmx_map, player_start_pos):
    
        # for layer in tmx_map.layers:
        #     if hasattr(layer, 'tiles'):  
        #         for x, y, surf in layer.tiles():
        #             Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # Xóa các sprite hiện tại
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.character_sprites.empty()
        self.projectiles.empty()
        self.monsters.empty()
        self.monster_houses.empty()
        self.items.empty()
        self.transition_sprites.empty()
        # Lưu trạng thái Player
        player_state = None
        if hasattr(self, 'player'):
            player_state = {
                'hp': self.player.hp,
                'damage': self.player.damage,
                'mode': self.player.mode,
                'speed': self.player.speed,
                'attack_cooldown': self.player.attack_cooldown
            }

        for x, y, surf in tmx_map.get_layer_by_name('Water').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['water'])

        for obj in tmx_map.get_layer_by_name('Foam'):
            Animation((obj.x, obj.y) , self.overworld_frames['foam'], self.all_sprites, WORLD_LAYERS['foam'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Flat_Beach').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Grass').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])
        
        for obj in tmx_map.get_layer_by_name('Rock'):
            Animation((obj.x, obj.y) , self.overworld_frames['rock'], self.all_sprites, WORLD_LAYERS['bg'])
        
        for x, y, surf in tmx_map.get_layer_by_name('Elevation').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites), WORLD_LAYERS['main'])
        
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'Tree':
                BothSprite((obj.x, obj.y), self.overworld_frames['tree'], (self.all_sprites, self.collision_sprites), WORLD_LAYERS['main'])
            else:
                CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in tmx_map.get_layer_by_name('Effect'):
            BothSprite((obj.x, obj.y), self.overworld_frames['fire'], (self.all_sprites, self.collision_sprites), WORLD_LAYERS['top'])

        for obj in tmx_map.get_layer_by_name('Collision'):
            BorderSprite((obj.x, obj.y),  pygame.Surface((int(obj.width), int(obj.height))), self.collision_sprites)
        for obj in tmx_map.get_layer_by_name('Transition'):
            print(obj.properties)
            TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target']),self.transition_sprites)
        for obj in tmx_map.get_layer_by_name('Position'):
            if obj.name == 'Player' and 'pos' in obj.properties and obj.properties['pos'] == player_start_pos:
                self.player = Player(
                    (obj.x, obj.y), 
                    self.overworld_frames['character'], 
                    self.all_sprites,
                    'stand_right', 
                    self.collision_sprites)
                if player_state:
                    self.player.hp = player_state.get('hp', self.player.hp)
                    self.player.damage = player_state.get('damage', self.player.damage)
                    self.player.mode = player_state.get('mode', self.player.mode)
                    self.player.speed = player_state.get('speed', self.player.speed)
                    self.player.attack_cooldown = player_state.get('attack_cooldown', self.player.attack_cooldown)
                
            elif obj.name == 'Character':
                Character(
                    (obj.x, obj.y),
                    self.overworld_frames['character'][obj.properties['graphic']],
                    (self.all_sprites, self.collision_sprites, self.character_sprites),
                    obj.properties['direction'],
                    obj.properties['character_type'],
                    DIALOG_DATA[obj.properties['character_id']])

            elif obj.name == 'Coin':
                Coin((obj.x, obj.y), (self.all_sprites, self.items), WORLD_LAYERS['main'])
            
            elif obj.name == 'Meat':
                Meat((obj.x, obj.y), self.overworld_frames['meat'],(self.all_sprites, self.items), WORLD_LAYERS['main'])

            # elif obj.name == 'Portal':
            #     target_map = int(obj.properties.get('target_map', 2))
            #     Portal((obj.x, obj.y), (self.all_sprites, self.items), target_map, WORLD_LAYERS['main'])

            elif obj.name in ('Torch', 'TNT'):

                Monster((obj.x, obj.y), obj, (self.all_sprites, self.monsters), self.collision_sprites)

            elif obj.name == 'MonsterHouse':
                MonsterHouse((obj.x, obj.y), obj, (self.all_sprites, self.monster_houses))

    def check_collisions(self):
        just_pressed = pygame.key.get_just_pressed()
        if just_pressed[pygame.K_SPACE]:
            self.player.attack(pygame.key.get_pressed())
            self.player.has_damaged = False
        if self.player.attacking and hasattr(self.player, 'attack_hitbox') and not self.player.has_damaged:
            damage = self.player.damage
            if damage is None:
                print(f"Lỗi: damage là None! Dùng giá trị mặc định 10.")
                damage = 10
            for monster in self.monsters:
                if self.player.attack_hitbox.colliderect(monster.hitbox):
                    try:
                        # self.player
                        monster.hp -= damage
                        self.player.has_damaged = True
                        print(f"Quái {monster.name} bị tấn công! HP còn lại: {monster.hp}")
                        if monster.hp <= 0:
                            monster.kill()
                            print(f"Đã tiêu diệt {monster.name}!")
                    except TypeError as e:
                        print(f"Lỗi khi trừ HP quái vật: {e}, damage: {damage}, monster.hp: {monster.hp}")
            for house in self.monster_houses:
                if self.player.attack_hitbox.colliderect(house.rect):
                    try:
                        self.player.has_damaged = True
                        print(f"Điểm spawn quái HP: {house.hp}")
                        house.take_damage(damage)
                    except TypeError as e:
                        print(f"Lỗi khi trừ HP nhà quái: {e}, damage: {damage}, house.hp: {house.hp}")

    # def change_map(self, target_map):
    #     if target_map in self.tmx_maps:
    #         self.current_map = target_map
    #         self.setup(self.tmx_maps[self.current_map], 'start')
    #         print(f"Đã chuyển sang map {self.current_map}")
    #     else:
    #         print(f"Map {target_map} không tồn tại!")

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
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)
    def end_dialog(self, character):
        self.dialog_tree = None
        self.player.unblock()
    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites and  all(house.destroyed for house in self.monster_houses):
            self.player.block()
            self.transition_target = [sprite.target for sprite in sprites]  # Lấy danh sách các target
            self.tint_mode = 'tint'
            if self.transition_target[0] == 'end':
                return True
        return False
    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
            
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                if self.transition_target and self.transition_target[0] in self.tmx_maps:
                    self.current_map = self.transition_target[0]
                    if (self.current_map == 'end'):
                        EndScreen(self.display_surface, 'win')
                    self.setup(self.tmx_maps[self.transition_target[0]], 'start')
                    self.tint_mode = 'untint'
                    self.transition_target = None
                else:
                    print(f"Lỗi: Bản đồ {self.transition_target[0]} không tồn tại hoặc không hợp lệ")
        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0, 0))


    def display_hp(self): # Hiển thị HP và Damage
        hp_text = self.fonts['dialog'].render(f"HP: {self.player.hp}", True, (0, 128, 0))
        attack_cooldown = self.fonts['dialog'].render(f"Speed_Attack: {self.player.attack_cooldown}", True, (255, 0, 0))
        screen_width, screen_height = self.display_surface.get_size()
        hp_rect = hp_text.get_rect(bottomleft=(10, screen_height - 10))
        damage_rect = attack_cooldown.get_rect(bottomleft=(10, screen_height - 40))
        self.display_surface.blit(hp_text, hp_rect)
        self.display_surface.blit(attack_cooldown, damage_rect)

    def run(self, dt):
        self.display_surface.fill('black') 

        # Spawn quái từ điểm spawn
        for house in self.monster_houses:
        # Điều chỉnh vị trí spawn quái vật
            spawn_pos = house.rect.center  #spawn giữa nhà quái

            new_monster = house.spawn(self.player.rect.center)
            if new_monster:
                Monster(spawn_pos, new_monster, (self.all_sprites, self.monsters), self.collision_sprites)
    
        # Quái update
        for monster in self.monsters:
            monster.monster_update(dt, self.player.rect.center, self.player, self.all_sprites)

        # Cập nhật tất cả sprite còn lại
        for sprite in self.all_sprites:
            if not isinstance(sprite, (tnt, Arrow, Coin, Meat)):
                sprite.update(dt)
        
        # Cập nhật tnt với player
        for sprite in self.all_sprites:
            if isinstance(sprite, tnt):
                sprite.update(dt, self.player)
        
        # Cập nhật arrow với monsters
        for sprite in self.all_sprites:
            if isinstance(sprite, Arrow):
                sprite.update(dt, self.monsters)
        
        # Cập nhật coin và meat với player
        for sprite in self.all_sprites:
            if isinstance(sprite, (Coin, Meat)):
                sprite.update(dt, self.player)
        
        # Cập nhật portal với player và callback
        # for sprite in self.all_sprites:
        #     if isinstance(sprite, Portal):
        #         sprite.update(dt, self.player, self.change_map)

        # Kiểm tra va chạm
        self.check_collisions()

        # self.player.check_attack_collisions(self.character_sprites)
        self.all_sprites.draw(self.player.rect.center)
        self.display_hp()
        self.input()
        self.transition_check()
        # self.all_sprites.update(dt)

        self.all_sprites.draw(self.player.rect.center)
        self.display_hp() 
        if self.dialog_tree: self.dialog_tree.update()

        self.tint_screen(dt)