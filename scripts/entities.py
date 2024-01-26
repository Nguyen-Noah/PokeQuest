import pygame
from utils.elements import ElementSingleton
from .player import Player

class Entities(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.entities = []

    def gen_player(self):
        self.entities.append(Player((0, 0)))
        return self.entities[-1]

    def update(self):
        pass