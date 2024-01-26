import pygame
from utils.elements import ElementSingleton
from .entities import Entities
from .lottery import Lottery
from utils.core_funcs import center_img_x

class World(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.entities = Entities()
        self.player = self.entities.gen_player()
        self.lottery = Lottery()

    def update(self):
        if self.e['Input'].mouse_state['left_click']:
            self.lottery.pull()
            #print(self.player.pokedex)

    def render(self, surf):
        assets = self.e['Assets'].battle_assets['1']
        pokemon = self.e['Assets'].pokemon['dragonite']['back_default']
        enemy = self.e['Assets'].pokemon['snorlax']['front_default']
        text_box = self.e['Assets'].text_boxes['hg']

        surf.blit(assets['bg'], (0, 0))

        back_plat_pos = (self.e['Window'].display.get_width() - assets['back'].get_width(), assets['back'].get_height())
        surf.blit(assets['back'], back_plat_pos)

        front_plat_pos = (0 - (assets['front'].get_width() / 4), assets['bg'].get_height() - assets['front'].get_height())
        surf.blit(assets['front'], front_plat_pos)

        player_pos = (75, assets['bg'].get_height() - pokemon.get_height() + 25)
        surf.blit(pokemon, player_pos)

        pygame.draw.rect(surf, (0, 0, 0), (0, assets['bg'].get_height(), assets['bg'].get_width(), surf.get_height() - assets['bg'].get_height()))
        surf.blit(text_box, (center_img_x(surf, text_box), self.e['Window'].display.get_height() - text_box.get_height()))