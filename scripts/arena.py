import pygame
from utils.elements import ElementSingleton

class Arena(ElementSingleton):
    def __init__(self, player_pokemon, enemy_pokemon, terrain_id=1):
        super().__init__()
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.terrain_id = terrain_id
        self.asset_lib = self.e['Assets'].battle_assets[str(self.terrain_id)]

        # absolute positions to blit
        self.back_plat_pos = (self.e['Window'].display.get_width() - ['back'].get_width(), self.assets['back'].get_height())
        self.front_plat_pos = (0 - (self.assets['front'].get_width() / 4), self.assets['bg'].get_height() - self.assets['front'].get_height())
        self.player_pos = (75, self.assets['bg'].get_height() - self.player_pokemon.get_height() + 25)
        


    def update(self):
        pass

    def render(self, surf):
        pass