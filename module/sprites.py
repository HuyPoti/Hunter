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
        self.hitbox = self.rect.inflate(-10, -self.rect.height * 0.6)

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
class TransitionSprite(Sprite):
    def __init__(self, pos, size, target, groups):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.target = target