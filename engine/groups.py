from utils.settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
    def draw(self, player_center):
        self.offset.x = -(player_center[0] - self.display_surface.get_width() / 2)
        self.offset.y = -(player_center[1] - self.display_surface.get_height() / 2)

        self.offset.x = max(min(0, self.offset.x), self.display_surface.get_width() - MAP_WIDTH*TILE_SIZE)
        self.offset.y = max(min(0, self.offset.y), self.display_surface.get_height() - MAP_HEIGHT*TILE_SIZE)
        bg_sprites = [sprite for sprite in self if hasattr(sprite, 'z') and isinstance(sprite.z, int) and sprite.z < WORLD_LAYERS['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['main']], key=lambda s: s.y_sort)
        fg_sprites = [sprite for sprite in self if hasattr(sprite, 'z') and isinstance(sprite.z, int) and sprite.z > WORLD_LAYERS['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
