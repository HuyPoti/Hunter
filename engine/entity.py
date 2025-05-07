from utils.settings import *
from module.sprites import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(groups)
        
        self.z = WORLD_LAYERS['main']
        #graphics
        self.facing_direction = facing_direction

        #movement
        self.direction = vector()
        self.speed = 250
        self.blocked = False

         
    def change_facing_direction(self, target_pos):
        relation = vector(target_pos) - vector(self.rect.center)
        if abs(relation.y) < 30:
            self.facing_direction = 'stand_right' if relation.x > 0 else 'stand_left'
        else:
            self.facing_direction = 'stand_down' if relation.y > 0 else 'stand_up'
    def block(self):
        self.blocked = True
        self.direction = vector(0,0)
    def unblock(self):
        self.blocked = False
class Character(Entity):
    def __init__(self, pos, frames, groups, facing_direction, character_type, character_data):
        super().__init__(pos, frames ,groups, facing_direction)
        self.direction = vector()
        self.z = WORLD_LAYERS['top'] if character_type != 'introducer' else WORLD_LAYERS['main']
        self.character_data = character_data
        self.frames_index, self.frames = 0, frames
        self.image = self.frames[self.get_state()][self.frames_index]
        #setup
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
        self.y_sort = self.rect.centery
    def get_dialog(self):
        return self.character_data['dialog']['default']
    def get_state(self):
        return f"{self.facing_direction}"
    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frames_index % len(self.frames[self.get_state()]))]
    def update(self, dt):
        self.animate(dt)

class Arrow(Sprite):
    def __init__(self, surf, pos, direction, damage , groups, z=WORLD_LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.image = surf
        self.direction = direction
        self.speed = 400
        self.damage = damage
        self.lifetime = 2.0
        self.creation_time = pygame.time.get_ticks() / 1000
        self.exploded = False
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.copy().inflate(20, 20)

    def update(self, dt, monsters):
        if self.exploded:
            return


        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        self.hitbox.center = self.rect.center
        

        for monster in monsters:
            if self.hitbox.colliderect(monster.hitbox):
                monster.hp -= self.damage
                if monster.hp <= 0:
                    monster.kill()
                self.exploded = True
                self.kill()
                break

        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.creation_time >= self.lifetime:
            self.exploded = True
            self.kill()

class Coin(BothSprite):
    def __init__(self, pos, groups, z=WORLD_LAYERS['main']):
        frame = [pygame.image.load(join('animation', 'resource', 'gold', '0.png')).convert_alpha()]
        super().__init__(pos, frame, groups, z)
        
        self.frames = frame
        # self.frames_index = 0
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.copy().inflate(-8, -8)
        self.value = 10
        print(f"Tạo Coin tại {pos}")

    def update(self, dt, player):
        self.image = self.frames[0]
        if self.hitbox.colliderect(player.hitbox):
            player.attack_cooldown  += self.value
            print(f"Nhặt Coin! Damage người chơi: {player.damage}")
            self.kill()

class Meat(BothSprite):
    def __init__(self, pos, frame, groups, z=WORLD_LAYERS['main']):
        super().__init__(pos, frame, groups, z)
        
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.copy().inflate(-8, -8)
        self.value = 15
        print(f"Tạo Meat tại {pos}")

    def update(self, dt, player):
        self.animate(dt)
        if self.hitbox.colliderect(player.hitbox):
            player.hp += self.value
            print(f"Nhặt Meat! HP người chơi: {player.hp}")
            self.kill()


class Player(Entity):
    def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
        super().__init__(pos, frames ,groups, facing_direction)
        self.hp = 200
        self.collision_sprites = collision_sprites
        # self.z = WORLD_LAYERS['main']
        self.mode = 'warrior'
        self.speed = 200
        self.damage = 50
        #attack
        self.attack_cooldown = 100
        self.attacking = False
        self.last_attack_time = 0
        self.attack_type = None
        self.frames_index, self.frames = 0, frames
        self.image = self.frames[self.mode][self.get_state()][self.frames_index]
        #setup
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
        self.y_sort = self.rect.centery

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        self.direction = input_vector.normalize() if input_vector.magnitude() > 0 else input_vector
        just_pressed = pygame.key.get_just_pressed()
        if just_pressed[pygame.K_LCTRL]:
            self.switch_mode()
        if just_pressed[pygame.K_SPACE]:
            self.attack(keys)
    def switch_mode(self):
        if self.mode == 'archer':
            self.mode = 'warrior'
            self.damage = 50
            self.speed = 200
        else:
            self.mode = 'archer'
            self.speed = 250
            self.damage = 30
        self.frames_index = 0
        self.image = self.frames[self.mode][self.get_state()][self.frames_index]
    def attack(self, keys):
        if not self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time < self.attack_cooldown:
                return
            self.attacking = True
            if keys[pygame.K_UP]:
                self.perform_attack('attack_up')
            elif keys[pygame.K_DOWN]:
                self.perform_attack('attack_down')
            elif keys[pygame.K_LEFT]:
                self.perform_attack('attack_left')
            elif keys[pygame.K_RIGHT]:
                self.perform_attack('attack_right')
            else:
                # Nếu không nhấn phím mũi tên, tấn công theo hướng đang đứng
                if self.facing_direction == 'stand_right':
                    self.perform_attack('attack_right')
                elif self.facing_direction == 'stand_left':
                    self.perform_attack('attack_left')
                elif self.facing_direction == 'stand_up':
                    self.perform_attack('attack_up')
                elif self.facing_direction == 'stand_down':
                    self.perform_attack('attack_down')
            self.last_attack_time = current_time
    def perform_attack(self, attack_type):
        self.block()
        self.frames_index = 0
        self.attack_type = attack_type
        # self.original_rect = self.rect.copy()
        # if attack_type == 'attack_up':
        #     self.rect.x -= 20
        self.image = self.frames[self.mode][attack_type][self.frames_index]
        if self.mode == 'warrior':
            # Tạo vùng sát thương cho warrior
            if attack_type == 'attack_left':
                self.attack_hitbox = pygame.Rect(self.rect.left - 50, self.rect.top, self.rect.width + 50, self.rect.height)
            elif attack_type == 'attack_right':
                self.attack_hitbox = pygame.Rect(self.rect.right + 50, self.rect.top, self.rect.width + 50, self.rect.height)
            elif attack_type == 'attack_up':
                self.attack_hitbox = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.width + 50)
            elif attack_type == 'attack_down':
                self.attack_hitbox = pygame.Rect(self.rect.left, self.rect.top , self.rect.width, self.rect.height + 50)
        else:
            # Tạo mũi tên cho archer
            direction = vector(0, 0)
            angle = 0  # Góc xoay của mũi tên
            if attack_type == 'attack_left':
                direction = vector(-1, 0)
                angle = 180
            elif attack_type == 'attack_right':
                direction = vector(1, 0)
                angle = 0
            elif attack_type == 'attack_up':
                direction = vector(0, -1)
                angle = 90
            elif attack_type == 'attack_down':
                direction = vector(0, 1)
                angle = -90

            # Xoay hình ảnh mũi tên
            self.arrow_surf = import_image(join('animation', 'resource', 'arrow'))
            rotated_arrow = pygame.transform.rotate(self.arrow_surf, angle)

            # Vị trí bắt đầu của mũi tên
            pos = self.rect.center + direction * 50
            Arrow(rotated_arrow, pos, direction, self.damage, self.groups() + [self.collision_sprites])
            
    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')

        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')
    def collisions(self, axis):
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
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
    # def check_attack_collisions(self, enemies):
    #     if self.mode == 'warrior' and hasattr(self, 'attack_hitbox'):
    #         for enemy in enemies:
    #             if self.attack_hitbox.colliderect(enemy.hitbox):
    #                 enemy.take_damage(self.damage['warrior'])
    def get_state(self):
        if self.attacking:
            return f"{self.facing_direction}"
        moving = bool(self.direction)
        if moving:
            if self.direction.x!=0:
                self.facing_direction = 'walk_right' if self.direction.x > 0 else 'walk_left'
            elif self.direction.y!=0:
                self.facing_direction = 'walk_down' if self.direction.y > 0 else 'walk_up'
        else:
            if self.facing_direction == 'walk_right':
                self.facing_direction = 'stand_right'
            elif self.facing_direction == 'walk_left':
                self.facing_direction = 'stand_left'
            elif self.facing_direction == 'walk_down':
                self.facing_direction = 'stand_down'
            elif self.facing_direction == 'walk_up':
                self.facing_direction = 'stand_up'
        return f"{self.facing_direction}"
    def animate(self, dt):
        if self.attacking:
            # Hoạt ảnh tấn công
            self.frames_index += (self.speed / 10) * dt
            if self.frames_index >= len(self.frames[self.mode][self.attack_type]):
                # Kết thúc hoạt ảnh tấn công
                self.unblock()
                self.attacking = False
                self.frames_index = 0
                self.image = self.frames[self.mode][self.get_state()][self.frames_index]
                # if hasattr(self, 'original_rect'):
                #     self.rect = self.original_rect
            else:
                # Hiển thị khung hình tiếp theo của hoạt ảnh tấn công
                self.image = self.frames[self.mode][self.attack_type][int(self.frames_index)]
        else:
            # Hoạt ảnh di chuyển hoặc đứng yên
            self.frames_index += ANIMATION_SPEED * dt
            self.image = self.frames[self.mode][self.get_state()][int(self.frames_index % len(self.frames[self.mode][self.get_state()]))]
    def update(self, dt):
        self.y_sort = self.rect.centery
        if not self.blocked:
            self.input()
            self.move(dt)
        self.animate(dt)
