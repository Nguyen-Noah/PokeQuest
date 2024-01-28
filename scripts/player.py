import pygame
from .entity import Entity

class Player(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.money = 0
        