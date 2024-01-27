import pygame
from utils.elements import Element

class BaseAffliction(Element):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.config = config[self.type]
        self.duration = self.config['duration']