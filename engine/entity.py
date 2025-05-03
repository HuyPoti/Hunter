from utils.settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(groups)
        self.z = WORLD_LAYERS['main']
        #graphics
        self.frames_index, self.frames = 0, frames
        self.facing_direction = facing_direction

        #movement
        self.direction = vector()
        self.speed = 250
        self.blocked = False

        #setup
        self.image = self.frames[self.get_state()][self.frames_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
        self.y_sort = self.rect.centery
    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frames_index % len(self.frames[self.get_state()]))]
    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x!=0:
                self.facing_direction = 'walk_right' if self.direction.x > 0 else 'walk_left'
        else:
            if self.facing_direction == 'walk_right':
                self.facing_direction = 'stand_right'
            elif self.facing_direction == 'walk_left':
                self.facing_direction = 'stand_left'
        return f"{self.facing_direction}" 
    def change_facing_direction(self, target_pos):
        relation = vector(target_pos) - vector(self.rect.center)
        if abs(relation.y) < 30:
            self.facing_direction = 'stand_right' if relation.x > 0 else 'stand_left'
    def block(self):
        self.blocked = True
        self.direction = vector(0,0)
    def unblock(self):
        self.block = False
class Character(Entity):
    def __init__(self, pos, frames, groups, facing_direction, character_type, character_data):
        super().__init__(pos, frames ,groups, facing_direction)
        self.direction = vector()
        self.z = WORLD_LAYERS['top'] if character_type != 'introducer' else WORLD_LAYERS['main']
        self.character_data = character_data
    def get_dialog(self):
        return self.character_data['dialog']['default']
    def update(self, dt):
        self.animate(dt)
class Player(Entity):
    def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
        super().__init__(pos, frames ,groups, facing_direction)
        self.collision_sprites = collision_sprites
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
    def update(self, dt):
        self.y_sort = self.rect.centery
        if not self.blocked:
            self.input()
            self.move(dt)
        self.animate(dt)
