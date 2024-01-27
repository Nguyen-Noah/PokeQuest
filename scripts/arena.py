import pygame
from utils.elements import ElementSingleton
from utils.core_funcs import center_img_x

class Arena(ElementSingleton):
    def __init__(self, terrain_id=1):
        super().__init__()
        self.terrain_id = terrain_id
        self.assets = self.e['Assets'].battle_assets[str(self.terrain_id)]

        self.transitioning = True
        self.plat_offset = 800

        # absolute positions to blit
        self.back_plat_pos = (self.e['Window'].display.get_width() - self.assets['back'].get_width() + 30, self.assets['back'].get_height())
        self.front_plat_pos = (0 - (self.assets['front'].get_width() / 4), self.assets['bg'].get_height() - self.assets['front'].get_height())

    def update(self):
        if self.transitioning:
            self.plat_offset -= 10
            if self.plat_offset <= 0:
                self.transitioning = False
        #self.fastest = self.player_pokemon if self.player_pokemon.speed > self.enemy_pokemon.speed else self.enemy_pokemon

    def render(self, surf):
        surf.blit(self.assets['bg'], (0, 0))

        # platforms
        surf.blit(self.assets['back'], (self.back_plat_pos[0] - self.plat_offset, self.back_plat_pos[1]))
        surf.blit(self.assets['front'], (self.front_plat_pos[0] + self.plat_offset, self.front_plat_pos[1]))

        # text box
        pygame.draw.rect(surf, (0, 0, 0), (0, self.assets['bg'].get_height(), self.assets['bg'].get_width(), surf.get_height() - self.assets['bg'].get_height()))
        surf.blit(self.e['Assets'].text_boxes['hg'], (center_img_x(surf, self.e['Assets'].text_boxes['hg']), self.e['Window'].display.get_height() - self.e['Assets'].text_boxes['hg'].get_height() - 3))