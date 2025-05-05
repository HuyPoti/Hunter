from utils.settings import *
from utils.support import *
from module.sprites import Arrow

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
class Player(Entity):
    def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
        super().__init__(pos, frames ,groups, facing_direction)
        self.collision_sprites = collision_sprites
        self.all_sprites = groups[0]
        self.arrow_sprites = groups[1]
        self.mode = 'warrior'
        self.damage = {
            'archer' : 10,
            'warrior' : 20
        }
        #attack
        self.attack_cooldown = 500
        self.attacking = False
        self.last_attack_time = 0
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
            self.speed = 200
        else:
            self.mode = 'archer'
            self.speed = 250
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
        self.original_rect = self.rect.copy()
        if attack_type == 'attack_up':
            self.rect.x -= 20
        self.image = self.frames[self.mode][attack_type][self.frames_index]
        if self.mode == 'warrior':
            # Tạo vùng sát thương cho warrior
            if attack_type == 'attack_left':
                self.attack_hitbox = pygame.Rect(self.rect.left - 50, self.rect.top, 50, self.rect.height)
            elif attack_type == 'attack_right':
                self.attack_hitbox = pygame.Rect(self.rect.right, self.rect.top, 50, self.rect.height)
            elif attack_type == 'attack_up':
                self.attack_hitbox = pygame.Rect(self.rect.left, self.rect.top - 50, self.rect.width, 50)
            elif attack_type == 'attack_down':
                self.attack_hitbox = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 50)
        elif self.mode == 'archer':
            # Tạo mũi tên
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

            # Tạo mũi tên
            Arrow(rotated_arrow, pos, direction, (self.all_sprites, self.arrow_sprites))
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
            self.frames_index += ANIMATION_SPEED * dt
            if self.frames_index >= len(self.frames[self.mode][self.attack_type]):
                # Kết thúc hoạt ảnh tấn công
                self.unblock()
                self.attacking = False
                self.frames_index = 0
                self.image = self.frames[self.mode][self.get_state()][self.frames_index]
                if hasattr(self, 'original_rect'):
                    self.rect = self.original_rect
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
