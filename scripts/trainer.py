import pygame
from .entity import Entity

class Trainer(Entity):
    def __init__(self, name):
        super().__init__()
        self.name = name