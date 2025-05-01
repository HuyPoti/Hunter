from utils.settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

def import_image(*path, alpha = True, format = 'png'):
    full_path = join(*path) +  f'.{format}' 
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf


def import_folder(*path):
    frames =  []
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames
def import_tilemap(*path):
    frames = []
    surf = import_image(*path)
    cell_width, cell_height = 82, 82
    rect_none = 55
    for i in range(8):
        cutout_rect = pygame.Rect(rect_none, 55, cell_width, cell_height)
        rect_none += 110 + cell_width;
        cutout_surf = pygame.Surface((cell_width, cell_height))
        cutout_surf.fill('blue')
        cutout_surf.set_colorkey('blue')
        cutout_surf.blit(surf, (0, 0), cutout_rect)
        frames.append(cutout_surf)
    return frames