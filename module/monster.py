import pygame
import math
from module.sprites import CollidableSprite, BothSprite
from utils.support import import_folder
from utils.settings import WORLD_LAYERS
from os.path import join
from utils.support import *

class Monster(BothSprite):
    def __init__(self, pos, obj, groups, collision_sprites=None, z=WORLD_LAYERS['main']):
        self.last_attack_time = 0
        self.attack_cooldown = 1.0
        self.name = obj.name
        if self.name == 'TNT':
            states = ['attack_left', 'attack_right', 'stand_left', 'stand_right', 'walk_left', 'walk_right']
        else:
            states = ['attack_left', 'attack_right', 'stand_left', 'stand_right', 'walk_left', 'walk_right', 'attack_up', 'attack_down']

        self.state = 'stand_right'
        frames = {}
        for state in states:
            frames[state] = import_folder('animation', 'monster', f"{self.name}/{state}")
            if not frames[state]:
                frames[state] = [pygame.Surface((64, 64))]
                frames[state][0].fill('red')
                print(f"Không tìm thấy frame cho {self.name}/{state}")

        super().__init__(pos, frames[self.state], groups, z)
        self.frames = frames
        self.collision_sprites = collision_sprites if collision_sprites is not None else pygame.sprite.Group()
        
        try:
            self.hp = obj.properties.get['hp']
        except (ValueError, TypeError) as e:
            self.hp = 100
            
        try:
            self.speed = float(obj.properties.get['speed'])
        except (ValueError, TypeError) as e:
            self.speed = 100.0
            
        try:
            self.damage = int(obj.properties.get['damage'])
        except (ValueError, TypeError) as e:
            self.damage = 10

        self.pos = list(pos)
        self.direction = pygame.math.Vector2()
        self.is_attacking = False
        self.has_thrown_tnt = False
        self.frames_index = 0

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')

        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')

        # Cập nhật self.pos
        self.pos = list(self.rect.center)

    def collisions(self, axis):
        if not self.collision_sprites:
            return
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def animate(self, dt):
        self.frames_index += (ANIMATION_SPEED / 2) * dt  # Tốc độ animation, có thể điều chỉnh
        if self.frames_index >= len(self.frames[self.state]):
            self.frames_index = 0 
        self.image = self.frames[self.state][int(self.frames_index)]

    def monster_update(self, dt, player_pos, player, all_sprites):
        self.animate(dt)

        # Tính hướng di chuyển dựa trên vị trí của Player
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        self.direction = pygame.math.Vector2((dx, dy))
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        distance = (dx**2 + dy**2)**0.5

        # Chọn trạng thái animation dựa trên khoảng cách và hướng

        if self.name == 'Torch':
            if distance > 20 and distance < 500:
                self.is_attacking = False
                if abs(dx) >= abs(dy):
                    self.state = 'walk_right' if dx >= 0 else 'walk_left'
                else:
                    self.state = 'walk_right' if dy >= 0 else 'walk_left'
                self.move(dt)
            elif distance > 500:
                self.is_attacking = False
                if abs(dx) > abs(dy):
                    self.state = 'stand_right' if dx > 0 else 'stand_left'
                else:
                    self.state = 'stand_right' if dy > 0 else 'stand_left'
            else:
                self.is_attacking = True
                if abs(dx) > abs(dy):
                    self.state = 'attack_right' if dx >= 0 else 'attack_left'
                else:
                    self.state = 'attack_down' if dy >= 0 else 'attack_up'

            current_time = pygame.time.get_ticks() / 1000
            if (self.is_attacking and self.hitbox.colliderect(player.hitbox) and 
                int(self.frames_index) >= len(self.frames[self.state]) - 1 and 
                current_time - self.last_attack_time >= self.attack_cooldown):
                self.last_attack_time = current_time
                player.hp -= self.damage
                print(f"{self.name} tấn công người chơi! HP người chơi: {player.hp}")
                if player.hp <= 0:
                    print("Game Over!")


        elif self.name == 'TNT':
            if  distance > 300:
                self.is_attacking = False
                if abs(dx) > abs(dy):
                    self.state = 'stand_right' if dx > 0 else 'stand_left'
                else:
                    self.state = 'stand_right' if dy > 0 else 'stand_left'
            else:
                if distance>200:
                    self.move(dt)
                if abs(dx) > abs(dy):
                    self.state = 'attack_right' if dx >= 0 else 'attack_left'
                else:
                    self.state = 'attack_right' if dy > 0 else 'attack_left'

                current_time = pygame.time.get_ticks() / 1000
                if (not self.has_thrown_tnt and 
                    int(self.frames_index) == 2 and
                    current_time - self.last_attack_time >= self.attack_cooldown):
                    self.has_thrown_tnt = True
                    self.last_attack_time = current_time
                    tnt_pos = (self.rect.centerx, self.rect.centery)
                    tnt_obj = tnt(tnt_pos, self.direction, all_sprites, WORLD_LAYERS['main'])
                    print(f"{self.name} ném TNT tại {tnt_pos}")
                    self.has_thrown_tnt = False



        self.animate(dt)
        self.rect = self.image.get_frect(center = self.pos)
        self.hitbox = self.rect.copy(). inflate(-10, -10)



class tnt(BothSprite):
    def __init__(self, pos, direction, groups, z=WORLD_LAYERS['main']):
        frames = [pygame.image.load(join('animation', 'candle', 'frame_0_delay-0.08s.png')).convert_alpha()]
        super().__init__(pos, frames, groups, z)
        
        self.frames = frames
        self.frames_index = 0
        self.direction = direction
        self.speed = 300
        self.damage = 15
        self.lifetime = 2.0
        self.creation_time = pygame.time.get_ticks() / 1000
        self.exploded = False
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.copy().inflate(-10, -10)
        print(f"Tạo TNT tại {pos}, hướng {self.direction}")

    def update(self, dt, player):
        if self.exploded:
            return

        self.frames_index += 8 * dt  # Tốc độ hoạt ảnh
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

        # Di chuyển TNT
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        self.hitbox.center = self.rect.center

        # Kiểm tra va chạm với người chơi
        if self.hitbox.colliderect(player.hitbox):
            player.hp -= self.damage
            print(f"TNT nổ! HP người chơi: {player.hp}")
            if player.hp <= 0:
                print("Game Over!")
                pygame.quit()
                exit()
            self.exploded = True
            self.kill()

        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.creation_time >= self.lifetime:
            print(f"TNT hết thời gian, nổ tại {self.rect.center}")
            self.exploded = True
            self.kill()

class MonsterHouse(CollidableSprite):
    def __init__(self, pos, obj, groups, z=WORLD_LAYERS['main']):
        frames = import_image('animation', 'building', 'Goblin_House')
        self.destroyed = False
        super().__init__(pos, frames, groups, z)
        
        try:
            self.hp = int(obj.properties['hp'])
        except (ValueError, TypeError) as e:
            self.hp = 200
            
        self.pos = list(pos)
        
        try:
            self.spawn_rate = float(obj.properties.get('spawn_rate', 5))
        except (ValueError, TypeError) as e:
            self.spawn_rate = 5
            
        self.monster_type = obj.properties['monster_type']
        self.last_spawn = pygame.time.get_ticks() / 2500
        print(f"Đã tạo MonsterHouse tại vị trí {self.pos}, kích thước: {self.image.get_size()}")
    def take_damage(self, damage):
        """
        Giảm HP của MonsterHouse khi bị tấn công và kiểm tra nếu bị phá hủy.
        """
        self.hp -= damage
        print(f"MonsterHouse tại {self.pos} nhận {damage} sát thương! HP còn lại: {self.hp}")
        
        if self.hp <= 0:
            self.destroyed = True
            print(f"MonsterHouse tại {self.pos} đã bị phá hủy!")
            self.kill()  # Xóa MonsterHouse khỏi tất cả các nhóm sprite
    def spawn(self, player_pos):
        current_time = pygame.time.get_ticks() / 2500
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        distance = (dx**2 + dy**2)**0.5

        # Chỉ spawn quái nếu khoảng cách <= 200
        if distance <= 500 and current_time - self.last_spawn >= self.spawn_rate:
            self.last_spawn = current_time
            class TempObj:
                pass
            new_monster = TempObj()
            new_monster.name = self.monster_type
            if self.monster_type == 'TNT':
                new_monster.properties = {'hp': 50, 'speed': 50.0, 'damage': 10}
            else:
                new_monster.properties = {'hp': 70, 'speed': 50.0, 'damage': 15}
            print(f"MonsterHouse spawn quái {self.monster_type}")
            return new_monster
        return None