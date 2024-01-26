import pygame
from utils.elements import Element
from .pokemon import Pokemon

class Pokedex(Element):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.max_team_size = 6
        self.owned_pokemon = {}
        self.active_pokemon = []

    def add(self, pokemon):
        if pokemon not in self.owned_pokemon:
            new_pkm = Pokemon(pokemon)
            self.owned_pokemon[pokemon] = new_pkm
            
            if len(self.active_pokemon) < self.max_team_size:
                self.active_pokemon.append(new_pkm)
        else:
            print('pokemon already owned')

    def __str__(self):
        return ' '.join(pokemon for pokemon in self.owned_pokemon)