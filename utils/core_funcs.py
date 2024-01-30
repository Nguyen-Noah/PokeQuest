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

def filter_asset(asset_list, female, shiny):
    front = 'front_shiny' if shiny else 'front_default'
    back = 'back_shiny' if shiny else 'back_default'
    front.join('_female' if female else '')
    back.join('_female' if female else '')

    return {'front': asset_list[front], 'back': asset_list[back]}

def itr(l):
    return sorted(enumerate(l), reverse=True)