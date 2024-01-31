import pygame, os, json

def load_config(filename):
    config_path = f'data/pokemon/{filename}/config.json'
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    return config

def center_img_x(window, image):
    return (window.get_width() // 2) - (image.get_width() // 2)

def center_img_y(window, image):
    return (window.get_height() // 2) - (image.get_height() // 2)

def center_img(window, image):
    return (center_img_x(window, image), center_img_y(window, image))

def filter_asset(asset_list, female, shiny, direction):
    base = direction
    base += '_shiny' if shiny else '_default'
    base += '_female' if female else ''

    return asset_list[base]

def itr(l):
    return sorted(enumerate(l), reverse=True)

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()