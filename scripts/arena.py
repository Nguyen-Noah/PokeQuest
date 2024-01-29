import pygame, math
from utils.elements import ElementSingleton
from utils.core_funcs import center_img_x
from .textbox import Textbox

class Arena(ElementSingleton):
    def __init__(self, rival, terrain_id=1):
        super().__init__()
        self.rival = rival
        self.terrain_id = terrain_id
        self.assets = self.e['Assets'].battle_assets[str(self.terrain_id)]
        self.state = 'opening'
        self.click_timer = 50
        self.current_textbox = self.e['Assets'].text_boxes['hg']

        # audio
        self.e['Audio'].load('battle_theme.wav', 1.0)
        self.e['Audio'].play('battle_theme')

        # font
        self.textbox = Textbox('hg')

        # timer for when the battle sequence starts
        self.transition = 160

        # little intro where the platforms transition to position
        self.shifting_plats = True
        self.plat_offset = 800

        # absolute positions to blit
        self.back_plat_pos = (self.e['Window'].display.get_width() - self.assets['back'].get_width() + 30, self.assets['back'].get_height())
        self.front_plat_pos = (0 - (self.assets['front'].get_width() / 4), self.assets['bg'].get_height() - self.assets['front'].get_height())

        # misc
        self.pokeball_spin = 0          # degrees

    def set_state(self, state):
        self.state = state

    def update(self):
        self.e['World'].player.update()
        self.rival.update()

        if self.transition >= 0:
            self.transition -= 1
        else:
            if self.state == 'opening':
                self.plat_offset -= 10
                if self.plat_offset <= 0:
                    self.state = 'prebattle'

        # START OF BATTLE LOOP
        if self.state == 'prebattle':
            self.click_timer -= 1
            if self.e['Input'].mouse_state['left_click'] and self.click_timer <= 0:
                self.state = 'rival_deploying'
                self.textbox.reset_text_counter()
        elif self.state == 'choose_action':
            if self.e['Input'].mouse_state['left_click']:
                self.state = 'choose_move'

    def render(self, surf):
        if self.transition <= 0:
            surf.blit(self.assets['bg'], (0, 0))

            # platforms
            surf.blit(self.assets['back'], (self.back_plat_pos[0] - self.plat_offset, self.back_plat_pos[1]))
            surf.blit(self.assets['front'], (self.front_plat_pos[0] + self.plat_offset, self.front_plat_pos[1]))
            
            self.rival.render(surf)
            self.e['World'].player.render(surf)

            # text box
            self.textbox.render(surf)