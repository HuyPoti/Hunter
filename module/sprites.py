from utils.settings import *
from utils.support import *
# import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.copy()

class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class CollidableSprite(Sprite):
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.inflate(-20, -self.rect.height * 0.6)

class Animation(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frames_index, self.frames = 0, frames
        super().__init__(pos, frames[0], groups, z)
    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]
    def update(self, dt):
        self.animate(dt)

class BothSprite(Animation, CollidableSprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        Animation.__init__(self, pos, frames, groups, z)
        CollidableSprite.__init__(self, pos, frames[0], groups)
        self.z = z
class Arrow(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize()  # Hướng di chuyển
        self.speed = speed
        self.lifetime = 2000  # Thời gian tồn tại của mũi tên (ms)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        # Di chuyển mũi tên
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        # Kiểm tra thời gian tồn tại
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()