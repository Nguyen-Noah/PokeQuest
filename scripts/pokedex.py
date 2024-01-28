import pygame
from utils.elements import Element
from .pokemon import Pokemon

class Pokedex(Element):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.max_team_size = 6
        self.owned_pokemon = {}
        self.team_pokemon = []

    def change_active_pokemon(self, target_pokemon):
        self.team_pokemon[target_pokemon], self.team_pokemon[0] = self.team_pokemon[0], self.team_pokemon[target_pokemon]

    def __str__(self):
        return ' '.join(pokemon for pokemon in self.owned_pokemon)
    
    def add(self, pokemon):
        if pokemon not in self.owned_pokemon:
            new_pkm = Pokemon(pokemon, self.owner)
            self.owned_pokemon[pokemon] = new_pkm
            
            if len(self.team_pokemon) < self.max_team_size:
                self.team_pokemon.append(new_pkm)
        else:
            print('pokemon already owned')

    def update(self):
        for pokemon in self.team_pokemon:
            pokemon.update()