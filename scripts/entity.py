import pygame
from utils.elements import Element
from .pokedex import Pokedex

class Entity(Element):
    def __init__(self):
        super().__init__()
        self.pokedex = Pokedex(self)

    def add_pokemon(self, pokemon):
        self.pokedex.add(pokemon)