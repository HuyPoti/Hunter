from utils.settings import *
# import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
class Animation(Sprite):
    def __init__(self, pos, frames, groups, frame_duration = 0.1):
        self.frames_index, self.frames = 0, frames
        super().__init__(pos, frames[0], groups)
    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]
    def update(self, dt):
        self.animate(dt)