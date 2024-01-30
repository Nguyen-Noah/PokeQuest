import pygame
from utils.elements import Element

class BaseAffliction(Element):
    def __init__(self, type, owner):
        super().__init__()
        self.type = type
        self.owner = owner
        #self.config = config[self.type]
        #self.duration = self.config['duration']