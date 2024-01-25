import pygame
from utils.elements import ElementSingleton

class Arena(ElementSingleton):
    def __init__(self, player_pokemon, enemy_pokemon):
        super().__init__()
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon

    def update(self):
        pass

    def render(self, surf):
        pass