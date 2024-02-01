import pygame, math
from utils.elements import ElementSingleton
from utils.core_funcs import center_img_x
from .textbox import Textbox

class Arena(ElementSingleton):
    def __init__(self, rival, terrain_id=1):
        super().__init__()
        self.rival = rival
        self._terrain_id = terrain_id
        self.assets = self.e['Assets'].battle_assets[str(self._terrain_id)]
        self.state = 'opening'
        self._click_timer = 50
        self._field_effects = {
            'player': [],
            'rival': []
        }
        self.attack_order = [self.e['World'].player.active_pokemon, self.rival.active_pokemon]

        self._available_moves = []
        self._available_switches = []

        self.e['Input'].set_input_mode('battle')

        # audio
        self.e['Audio'].load('battle_theme.wav', 1.0)
        #self.e['Audio'].play('battle_theme')

        # font
        self.textbox = Textbox('hg')

        # Timers/Offsets -------------------------------- #
        # timer for when the battle sequence starts
        self._transition = 160

        # little intro where the platforms transition to position
        self.plat_offset = 800

        # wait timer between pokemon attacks
        self._action_timer = 80

        # absolute positions to blit
        self.back_plat_pos = (self.e['Window'].display.get_width() - self.assets['back'].get_width() + 30, self.assets['back'].get_height())
        self.front_plat_pos = (0 - (self.assets['front'].get_width() / 4), self.assets['bg'].get_height() - self.assets['front'].get_height())

    def set_state(self, state):
        self.state = state

    def update(self):
        self._available_moves = []
        self._available_switches = []

        self.e['World'].player.update()
        self.rival.update()
        self.textbox.update()

        if self.e['World'].player.active_pokemon is not None:
            self._available_moves.extend(self.e['World'].player.active_pokemon.get_moves())

        for pokemon in self.rival.team_pokemon:
            if not pokemon.active and not pokemon.fainted:
                self._available_switches.append(pokemon)

        if self._transition >= 0:
            self._transition -= 1
        else:
            if self.state == 'opening':
                self.plat_offset -= 10
                if self.plat_offset <= 0:
                    self.state = 'prebattle'

        # START OF BATTLE LOOP
        if self.state == 'prebattle':
            self._click_timer -= 1
            if self.e['Input'].mouse_state['left_click'] and self._click_timer <= 0:
                self.state = 'rival_deploying'
                self.textbox.reset_text_counter()

        elif self.state == 'choose_action':
            if self.e['Input'].mouse_state['left_click']:
                self.state = 'choose_move'

                # calculate who will move first
                if self.e['World'].player.active_pokemon.speed > self.rival.active_pokemon.speed:
                    self.attack_order = [self.e['World'].player.active_pokemon, self.rival.active_pokemon]
                else:
                    self.attack_order = [self.rival.active_pokemon, self.e['World'].player.active_pokemon]

        elif self.state == 'choose_move':
            self.rival.choose_move(self)

        elif self.state == 'first_action':
            if self._action_timer > 0:
                self._action_timer -= 1
            else:
                if self.attack_order[1].damage_taken < 0:
                    self.state = 'last_action'
                    self._action_timer = 80
                    self.textbox.reset_text_counter()

                if not self.attack_order[0].attacked:
                    self.attack_order[0].use_move(self.textbox.selected_move)

        elif self.state == 'last_action':
            if self._action_timer > 0:
                self._action_timer -= 1
            else:
                if self.attack_order[0].damage_taken < 0:
                    self.state = 'end_loop'

                if not self.attack_order[1].attacked:
                    self.attack_order[1].use_move(self.rival.selected_move)                    # CHANGE WITH AI

        elif self.state == 'end_loop':
            self._action_timer = 80
            self.attack_order[0].reset_battle_loop()
            self.attack_order[1].reset_battle_loop()
            self.textbox.reset_text_counter()
            # use for whatever
            self.state = 'choose_action'

        #print(self.state)

    def render(self, surf):
        if self._transition <= 0:
            surf.blit(self.assets['bg'], (0, 0))

            # platforms
            surf.blit(self.assets['back'], (self.back_plat_pos[0] - self.plat_offset, self.back_plat_pos[1]))
            surf.blit(self.assets['front'], (self.front_plat_pos[0] + self.plat_offset, self.front_plat_pos[1]))
            
            self.rival.render(surf)
            self.e['World'].player.render(surf)

            # text box
            self.textbox.render(surf)


    @property
    def available_moves(self):
        return self._available_moves