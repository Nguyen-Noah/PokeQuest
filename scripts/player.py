import pygame
from .trainer import Trainer

class Player(Trainer):
    def __init__(self, pos):
        super().__init__('player', 'player')
        self.pos = pos
        self.money = 0
        self.state = 'fighting'
        self.assets = self.e['Assets'].player
        self.current_img = self.assets['arena_idle']
        self.add_pokemon('clefairy')

        self.throw_timer = 0
        self.throw_offset = 0
        self.state_padding = 0              # padding some time after the pokemon is deployed
        
    def update(self):
        super().update()
        if self.state == 'fighting':
            if self.e['Arena'].state == 'deploying':
                self.current_img = self.assets['arena_charge']
                self.render_pokemon = True
                self.throw_timer += 1
                if self.throw_timer >= 30:
                    self.current_img = self.assets['arena_throw']

                if self.throw_offset <= 360:
                    self.throw_offset += 6
                else:
                    self.state_padding += 1
                    if self.state_padding >= 50:
                        self.e['Arena'].textbox.reset_text_counter()
                        self.e['Arena'].set_state('choose_action')

            self.selected_move = self.active_pokemon.active_moves[self.e['Textbox'].selected_move]

        #print(self.active_pokemon.__repr__())

    def render(self, surf):
        if self.state == 'fighting':
            render_pos = (self.current_img.get_width() - 140, self.e['Arena'].assets['bg'].get_height() - self.current_img.get_height())
            if self.e['Arena'].state == 'opening':
                surf.blit(self.current_img, (render_pos[0] + self.e['Arena'].plat_offset, render_pos[1]))
            elif self.e['Arena'].state in ['prebattle', 'rival_deploying']:
                surf.blit(self.current_img, render_pos)
            elif self.e['Arena'].state == 'deploying':
                surf.blit(self.current_img, (render_pos[0] - self.throw_offset, render_pos[1]))

            if self.render_pokemon:
                self.active_pokemon.render(surf, (render_pos[0] - 400 + self.throw_offset, self.e['Arena'].assets['bg'].get_height() - 260))
                

    @property
    def name(self):
        return self._name