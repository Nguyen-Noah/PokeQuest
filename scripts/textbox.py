import pygame, math, random
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

        self.move_options = [(0, 0), (self.assets[self.type + '_moves'].get_width() // 2, 0), (0, self.assets[self.type + '_moves'].get_height() // 2), (self.assets[self.type + '_moves'].get_width() // 2, self.assets[self.type + '_moves'].get_height() // 2)]
        self.selected_move = 0

    def _render_text(self, surf, text):
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
        if self.e['Arena'].state == 'choose_move':
            if self.e['Input'].states['right_battle'] or self.e['Input'].states['left_battle']:
                if self.selected_move in [0, 2]:
                    self.selected_move += 1
                else:
                    self.selected_move -= 1
            if self.e['Input'].states['up_battle'] or self.e['Input'].states['down_battle']:
                if self.selected_move in [0, 1]:
                    self.selected_move += 2
                else:
                    self.selected_move -= 2

            if self.e['Input'].states['select_move']:
                self.e['Arena'].set_state('first_action')
                self.reset_text_counter()

    def render(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), (0, self.e['Arena'].assets['bg'].get_height(), self.e['Arena'].assets['bg'].get_width(), surf.get_height() - self.e['Arena'].assets['bg'].get_height()))
        render_pos = (center_img_x(surf, self.assets[self.type]), surf.get_height() - self.assets[self.type].get_height() - 3)
        surf.blit(self.current_textbox, render_pos)

        if self.e['Arena'].state == 'prebattle':
            self._render_text(surf, f'You are challenged by trainer {self.rival.name.upper()}!')

        elif self.e['Arena'].state == 'rival_deploying':
            self._render_text(surf, f'{self.rival.name.capitalize()} sent out {self.rival.active_pokemon.name.upper()}!')

        elif self.e['Arena'].state == 'deploying':
            self._render_text(surf, f'Go! {self.player.active_pokemon.name.upper()}!')

        elif self.e['Arena'].state == 'choose_action':
            self._render_text(surf, f'What will {self.player.active_pokemon.name.upper()} do?')
            self.current_textbox = self.assets[self.type + '_moves']
            surf.blit(self.assets['fight'], (self.current_textbox.get_width(), render_pos[1]))

        elif self.e['Arena'].state == 'choose_move':
            for i in range(len(self.player.active_pokemon.active_moves)):
                pos = self.move_options[i]
                pygame.draw.rect(surf, (0, 255, 0) if self.selected_move == i else (255, 0, 0), (pos[0], pos[1] + self.e['Arena'].assets['bg'].get_height(), self.current_textbox.get_width() // 2, self.current_textbox.get_height() // 2), 4)
        
        elif self.e['Arena'].state == 'first_action':
            first = self.e['Arena'].attack_order[0]
            self._render_text(surf, f'{first.name.capitalize()} used {first.active_pokemon.active_moves[self.selected_move].name.upper()}!')

        elif self.e['Arena'].state == 'last_action':
            last = self.e['Arena'].attack_order[1]
            self._render_text(surf, f'{last.name.capitalize()} used {last.active_pokemon.active_moves[0].name.upper()}!')                   # CHANGE WITH AI