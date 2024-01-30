import pygame, math
from utils.elements import ElementSingleton
from utils.core_funcs import center_img_x

class Textbox(ElementSingleton):
    def __init__(self, type, custom_id=None):
        super().__init__(custom_id)
        self.type = type
        self.font = pygame.font.Font('data/fonts/pokemon-ds-font.ttf', 40)
        self.text_counter = 0
        self.assets = self.e['Assets'].text_boxes
        self.current_textbox = self.assets[self.type]
        self.selected_option = 0            # 0, 1, 2, 3

        # getting the trainers for simplicity
        self.player = self.e['World'].player
        self.rival = self.e['Arena'].rival

    def render_text(self, surf, text):
        text_surf = self.font.render(text[:math.floor(self.text_counter)], True, (80, 80, 80))
        shadow_text = self.font.render(text[:math.floor(self.text_counter)], True, (200, 200, 200))
        self.text_counter += 0.5
        # render the text shadow and then the text
        surf.blit(shadow_text, (38, 455))
        surf.blit(shadow_text, (38, 457))
        surf.blit(shadow_text, (36, 457))
        surf.blit(text_surf, (36, 455))

    def reset_text_counter(self):
        self.text_counter = 0

    def update(self):
        pass

    def render(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), (0, self.e['Arena'].assets['bg'].get_height(), self.e['Arena'].assets['bg'].get_width(), surf.get_height() - self.e['Arena'].assets['bg'].get_height()))
        render_pos = (center_img_x(surf, self.assets[self.type]), surf.get_height() - self.assets[self.type].get_height() - 3)
        surf.blit(self.current_textbox, render_pos)

        if self.e['Arena'].state == 'prebattle':
            self.render_text(surf, f'You are challenged by trainer {self.rival.name.upper()}!')
        elif self.e['Arena'].state == 'rival_deploying':
            self.render_text(surf, f'{self.rival.name.capitalize()} sent out {self.rival.active_pokemon.name.upper()}!')
        elif self.e['Arena'].state == 'deploying':
            self.render_text(surf, f'Go! {self.player.active_pokemon.name.upper()}!')
        elif self.e['Arena'].state == 'choose_action':
            self.render_text(surf, f'What will {self.player.active_pokemon.name.upper()} do?')
            self.current_textbox = self.assets[self.type + '_moves']
            surf.blit(self.assets['fight'], (self.current_textbox.get_width(), render_pos[1]))