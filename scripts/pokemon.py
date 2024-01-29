import pygame, random
from utils.elements import Element
from utils.core_funcs import load_config, filter_asset
from .move import Move
from .config import config

class Pokemon(Element):
    def __init__(self, name, owner):
        super().__init__()
        self.name = name
        self.owner = owner
        self.config = load_config(self.name)
        self.load()
        if self.owner.type == 'player':
            self.healthbar_transition = self.e['Assets'].health_bars[self.owner.type + '_main'].get_width()
        else:
            self.healthbar_transition = -self.e['Assets'].health_bars[self.owner.type + '_main'].get_width()
        self.text = pygame.font.Font('data/fonts/pokemon-ds-font.ttf', 45)

    def load(self):
        # female/shiny -------- #
        self.female = self.config['misc']['gender_rate'] > random.randint(0, 8)
        self.shiny = random.randint(1, 8192) == 1

        # stats --------------- #
        self.nature, self.nature_stat = random.choice(list(config['pokemon_constants']['natures'].items()))
        self.load_stats()

        self.level = 1
        self.exp = 0

        # moves --------------- #
        self.active_moves = []
        for move in self.config['moves']:
            for learn_method in self.config['moves'][move]:                                         # this loop runs at most 4 times, rarely more than once
                if learn_method['learn_method'] == 'level-up' and learn_method['level_learned'] == 1:
                    self.active_moves.append(Move(move, self))

        # assets -------------- #
        self.assets = filter_asset(self.e['Assets'].pokemon[self.name], self.female, self.shiny)

    def __repr__(self):
        return f'hp: {self.hp}, atk: {self.attack}, def: {self.defense}, sp_atk: {self.special_attack}, sp_def: {self.special_defense}, speed: {self.speed}'
    
    def __str__(self):
        gender = 'female' if self.female else 'male'
        return f'{self.name}, {gender}, {self.shiny}'

    def load_stats(self):
        c = self.config['base_stats']
        up, down = self.nature_stat
        self.hp_dict = {
            'base': c['hp'][0],                                                     # the base stat
            'ev': c['hp'][1],                                                       # the ev value <- this is incrememnted throughout the game
            'iv': random.randint(0, 31),                                            # the iv value <- this is immutable and stays constant in range [0, 31]
            'nature': 1.1 if up == 'health' else 0.9 if down == 'health' else 1.0
        }
        self.atk_dict = {
            'base': c['attack'][0],
            'ev': c['attack'][1],
            'iv': random.randint(0, 31),
            'nature': 1.1 if up == 'attack' else 0.9 if down == 'attack' else 1.0
        }
        self.def_dict = {
            'base': c['defense'][0],
            'ev': c['defense'][1],
            'iv': random.randint(0, 31),
            'nature': 1.1 if up == 'defense' else 0.9 if down == 'defense' else 1.0
        }
        self.sp_atk_dict = {
            'base': c['special-attack'][0],
            'ev': c['special-attack'][1],
            'iv': random.randint(0, 31),
            'nature': 1.1 if up == 'special_attack' else 0.9 if down == 'special_attack' else 1.0
        }
        self.sp_def_dict = {
            'base': c['special-defense'][0],
            'ev': c['special-defense'][1],
            'iv': random.randint(0, 31),
            'nature': 1.1 if up == 'special_defense' else 0.9 if down == 'special_defense' else 1.0
        }
        self.speed_dict = {
            'base': c['speed'][0],
            'ev': c['speed'][1],
            'iv': random.randint(0, 31),
            'nature': 1.1 if up == 'speed' else 0.9 if down == 'speed' else 1.0
        }

    def reset_stats(self):
        # use after fights to reset all of the stats
        self.hp = self.calculate_health()
        self.attack = self.calculate_stat(self.atk_dict)
        self.defense = self.calculate_stat(self.def_dict)
        self.special_attack = self.calculate_stat(self.sp_atk_dict)
        self.special_defense = self.calculate_stat(self.sp_def_dict)
        self.speed = self.calculate_stat(self.speed_dict)

    def calculate_stat(self, stat_dict):
        return (((2 * stat_dict['base'] + stat_dict['iv'] + (stat_dict['ev'] / 4)) * self.level) / 100 + 5) * stat_dict['nature']
    
    def calculate_health(self):
        return ((2 * self.hp_dict['base'] + self.hp_dict['iv'] + (self.hp_dict['ev'] / 4)) * self.level) / 100 + self.level + 10

    def gain_exp(self, amt):
        self.exp += amt

    def render_health(self, surf):
        if self.owner.type == 'player':
            name_offset = (60, 25)
            render_pos = (surf.get_width() - self.e['Assets'].health_bars[self.owner.type + '_main'].get_width(), 280)
            if self.healthbar_transition > 0:
                self.healthbar_transition -= min(12, self.healthbar_transition)
        else:
            name_offset = (10, 25)
            render_pos = (0, 50)
            if self.healthbar_transition <= 0:
                self.healthbar_transition += min(12, abs(self.healthbar_transition))

        render_pos = (render_pos[0] + self.healthbar_transition, render_pos[1])
        surf.blit(self.e['Assets'].health_bars[self.owner.type + '_main'], render_pos)

        text_surf = self.text.render(self.name.capitalize(), True, (80, 80, 80))
        shadow_surf = self.text.render(self.name.capitalize(), True, (200, 200, 200))
        surf.blit(shadow_surf, (render_pos[0] + name_offset[0] + 2, render_pos[1] + name_offset[1]))
        surf.blit(shadow_surf, (render_pos[0] + name_offset[0] + 2, render_pos[1] + name_offset[1] + 2))
        surf.blit(shadow_surf, (render_pos[0] + name_offset[0], render_pos[1] + name_offset[1] + 2))
        surf.blit(text_surf, (render_pos[0] + name_offset[0], render_pos[1] + name_offset[1]))

    def update(self):
        self.reset_stats()

    def render(self, surf, pos, direction='back'):
        surf.blit(self.assets[direction], (pos[0], pos[1] + 40))
        self.render_health(surf)