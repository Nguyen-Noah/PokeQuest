import pygame, math
from utils.elements import ElementSingleton
from utils.core_funcs import center_img_x
from .rival import Rival

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
        self.text = pygame.font.Font('data/fonts/pokemon-ds-font.ttf', 40)
        self.text_counter = 0

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

    def render_text(self, surf, text, newline):
        text_surf = self.text.render(text[:math.floor(self.text_counter)], True, (80, 80, 80))
        shadow_text = self.text.render(text[:math.floor(self.text_counter)], True, (200, 200, 200))
        self.text_counter += 0.5
        # render the text shadow and then the text
        surf.blit(shadow_text, (38, 455))
        surf.blit(shadow_text, (38, 457))
        surf.blit(shadow_text, (36, 457))
        surf.blit(text_surf, (36, 455))

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

        if self.state == 'deploying':
            self.pokeball_spin += 10

    def render(self, surf):
        if self.transition <= 0:
            surf.blit(self.assets['bg'], (0, 0))

            # platforms
            surf.blit(self.assets['back'], (self.back_plat_pos[0] - self.plat_offset, self.back_plat_pos[1]))
            surf.blit(self.assets['front'], (self.front_plat_pos[0] + self.plat_offset, self.front_plat_pos[1]))
            
            self.rival.render(surf)
            self.e['World'].player.render(surf)

            # text box
            pygame.draw.rect(surf, (0, 0, 0), (0, self.assets['bg'].get_height(), self.assets['bg'].get_width(), surf.get_height() - self.assets['bg'].get_height()))
            text_box_pos = (center_img_x(surf, self.e['Assets'].text_boxes['hg']), self.e['Window'].display.get_height() - self.e['Assets'].text_boxes['hg'].get_height() - 3)
            surf.blit(self.current_textbox, text_box_pos)

            # START OF THE BATTLE LOOP ------------------------------------ #
            if self.state == 'prebattle':
                # text
                self.render_text(surf, f'You are challenged by trainer {self.rival.name.upper()}!', 20)
                
                self.click_timer -= 1
                if self.e['Input'].mouse_state['left_click'] and self.click_timer <= 0:
                    self.state = 'rival_deploying'
                    self.text_counter = 0

            elif self.state == 'rival_deploying':
                self.render_text(surf, f'{self.rival.name.capitalize()} sent out {self.rival.active_pokemon.name.upper()}!', 20)

            elif self.state == 'deploying':
                self.player_pokemon = self.e['World'].player.active_pokemon.name.upper()
                self.render_text(surf, f'Go! {self.player_pokemon}!', 20)

            elif self.state == 'choose_move':
                self.render_text(surf, f'What will {self.player_pokemon} do?', 20)
                self.current_textbox = self.e['Assets'].text_boxes['hg_moves']
                surf.blit(self.e['Assets'].misc['fight'], (self.current_textbox.get_width(), self.assets['bg'].get_height()))