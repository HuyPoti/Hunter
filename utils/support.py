from utils.settings import *
from os.path import join, isdir
from os import walk
import os
from pytmx.util_pygame import load_pygame

def import_image(*path, alpha = True, format = 'png'):
    full_path = join(*path) +  f'.{format}' 
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

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
def import_folder(*path):
    frames =  []
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key=lambda x: int(x.split('.')[0])):
            full_path = join(folder_path, image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames
def import_all_characters(*path):
    characters = {}
    root_path = join(*path)
    for character_name in os.listdir(root_path):
        character_path = join(root_path, character_name)
        if isdir(character_path):
            action_dict = {}
            for action in os.listdir(character_path):
                action_path = join(character_path, action)
                if isdir(action_path):
                    action_dict[action] = import_folder(action_path)
                    action_dict[f'{action}_idle'] = [action_dict[action][0]] if action_dict[action] else []
            characters[character_name] = action_dict
    return characters


def check_connection(radius, entity, target, tolerance = 30):
    relation = vector(target.rect.center) - vector(entity.rect.center)
    if relation.length() < radius:
        if entity.facing_direction == 'stand_left' and relation.x < 0 and abs(relation.y) < tolerance or \
            entity.facing_direction == 'stand_right' and relation.x > 0 and abs(relation.y) < tolerance:
            return True