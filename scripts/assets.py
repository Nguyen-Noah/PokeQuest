import pygame, os, json
from utils.elements import ElementSingleton
from .config import config

class Assets(ElementSingleton):
    def __init__(self):
        super().__init__()

        self.scale_ratio = config['window']['scale_ratio']

        self.battle_assets = self.load_dirs('data/graphics/battle_platforms', colorkey=(255, 255, 255))
        self.pokemon = self.load_pokemon('data/pokemon')
        self.text_boxes = self.load_dir('data/graphics/text_boxes', colorkey=(0, 0, 0))
        self.health_bars = self.load_dir('data/graphics/health_bars', colorkey=(0, 19, 127))

    def load_pokemon(self, path):
        pokemon_list = {}
        for pokemon in os.listdir(path):
            pokemon_list[pokemon] = self.load_dir(path + '/' + pokemon + '/sprites')
        return pokemon_list

    def load_dirs(self, path, colorkey=None):
        dirs = {}
        for dir in os.listdir(path):
            dirs[dir] = self.load_dir(path + '/' + dir, colorkey=colorkey)
        return dirs
    
    def load_dir(self, path, colorkey=None):
        image_dir = {}
        for file in os.listdir(path):
            if file.split('.')[-1] == 'png':
                if colorkey:
                    image_dir[file.split('.')[0]] = self.load_img(path + '/' + file, colorkey=colorkey)
                else:
                    image_dir[file.split('.')[0]] = self.load_img(path + '/' + file)
        return image_dir

    def load_img(self, path, colorkey=None):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * self.scale_ratio, img.get_height() * self.scale_ratio))
        if path.split('/')[-1].split('.')[0] == 'bg':
            img = pygame.transform.gaussian_blur(img, 10)
        img.set_colorkey(colorkey)
        return img