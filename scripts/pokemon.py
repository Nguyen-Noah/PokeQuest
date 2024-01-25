import pygame
from utils.elements import Element
from utils.core_funcs import load_config

class Pokemon(Element):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.config = load_config(self.name)
        print(self.config)