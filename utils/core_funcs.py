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