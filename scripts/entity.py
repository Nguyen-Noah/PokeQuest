import pygame
from utils.elements import Element
from .pokedex import Pokedex

class Entity(Element):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.pokedex = Pokedex(self)

    def add_pokemon(self, pokemon):
        self.pokedex.add(pokemon)

    def update(self):
        pass

    def render(self, surf):
        pass