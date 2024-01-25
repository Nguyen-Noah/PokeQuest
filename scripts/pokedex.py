import pygame
from utils.elements import Element
from .pokemon import Pokemon

class Pokedex(Element):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.owned_pokemon = []
        self.active_pokemon = []

    def add(self, pokemon):
        self.owned_pokemon.append(Pokemon(pokemon))