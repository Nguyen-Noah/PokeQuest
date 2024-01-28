import pygame
from utils.elements import Element
from .pokedex import Pokedex

class Entity(Element):
    def __init__(self):
        super().__init__()
        self.pokedex = Pokedex(self)

    @property
    def active_pokemon(self):
        return self.pokedex.active_pokemon[0]

    def add_pokemon(self, pokemon):
        self.pokedex.add(pokemon)

    def update(self):
        self.pokedex.update()

    def render(self, surf):
        pass
