import pygame, random
from utils.elements import Element
from utils.core_funcs import load_config, filter_asset, itr
from .move import Move
from .healthbar import Healthbar
from .config import config
from .afflictions import affliction_map

def slow(level):
    return 5 * level ** 3 // 4

def medium_slow(level):
    return (6 * level ** 3 // 5) - (15 * level ** 2) + (100 * level) - 140

def medium(level):
    return level ** 3

def fast(level):
    return 4 * level ** 3 // 5

exp_map = {
    'slow': slow,
    'medium-slow': medium_slow,
    'medium': medium,
    'fast': fast
}

class Pokemon(Element):
    def __init__(self, name, owner, custom_id=False, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.name = name
        self.owner = owner
        self.config = load_config(self.name)
        self.damage_taken = 0
        self.afflictions = []
        self.attacked = False
        self.alive = True
        self._load()
        self.blink_timer = 7
  
    def _load(self):
        # female/shiny -------- #
        self.female = self.config['misc']['gender_rate'] > random.randint(0, 8)
        self.shiny = random.randint(1, 8192) == 1

        # stats --------------- #
        self.level = 1
        self.exp = 0

        self.calculate_exp = exp_map[self.config['misc']['growth_rate']]
        self.exp_to_level_up = self.calculate_exp(self.level)
        if self.exp_to_level_up == 0:
            self._process_exp()

        self.nature, self.nature_stat = random.choice(list(config['pokemon_constants']['natures'].items()))
        self._load_stats()

        self._boosts = {
            'accuracy': 0,
            'attack': 0,
            'defense': 0,
            'evasion': 0,
            'special_attack': 0,
            'special_defense': 0,
            'speed': 0
        }

        # moves --------------- #
        self.active_moves = []
        for move in self.config['moves']:
            for learn_method in self.config['moves'][move]:                                         # this loop runs at most 4 times, rarely more than once
                if learn_method['learn_method'] == 'level-up' and learn_method['level_learned'] == 1:
                    self.active_moves.append(Move(move, self))

        # assets -------------- #
        self.img = filter_asset(self.e['Assets'].pokemon[self.name], self.config['misc']['has_gender_differences'], self.shiny, 'back' if self.owner.type == 'player' else 'front')

        # healthbar ----------- #
        self.healthbar = Healthbar(self)

    def _process_exp(self):
        while self.exp >= self.exp_to_level_up:
            self.exp -= self.exp_to_level_up
            self.level += 1
            self.exp_to_level_up = self.calculate_exp(self.level)

    def _load_stats(self):
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
        self._calculate_stats()
        self.current_hp = self.max_hp

    def _calculate_stats(self):
        # use after fights to reset all of the stats
        self.max_hp = self.calculate_health()
        self.attack = self.calculate_stat(self.atk_dict)
        self.defense = self.calculate_stat(self.def_dict)
        self.special_attack = self.calculate_stat(self.sp_atk_dict)
        self.special_defense = self.calculate_stat(self.sp_def_dict)
        self.speed = self.calculate_stat(self.speed_dict)

    def calculate_stat(self, stat_dict):
        return (((2 * stat_dict['base'] + stat_dict['iv'] + (stat_dict['ev'] / 4)) * self.level) / 100 + 5) * stat_dict['nature']

    def calculate_health(self):
        return ((2 * self.hp_dict['base'] + self.hp_dict['iv'] + (self.hp_dict['ev'] / 4)) * self.level) / 100 + self.level + 10

    @property
    def boosts(self):
        return self._boosts

    def boost(self, stat, amt):
        self._boosts[stat] += amt
        if self._boosts[stat] > 6:
            self._boosts[stat] = 6
        elif self._boosts[stat] < -6:
            self._boosts[stat] = 6

    def clear_boosts(self):
        for stat in self._boosts:
            self._boosts[stat] = 0

    def clear_negative_boosts(self):
        for stat in self._boosts:
            if self._boosts[stat] < 0:
                self._boosts[stat] = 0

    def clear_positive_boosts(self):
        for stat in self._boosts:
            if self._boosts[stat] > 0:
                self._boosts[stat] = 0

    def invert_boosts(self):
        self._boosts = {k: -v for k, v in self._boosts.items()}

    def use_move(self, index):
        print(self.name, self.active_moves[index].name)
        self.active_moves[index].use()
        self.attacked = True

    def reset_battle_loop(self):
        self.attacked = False
    
    def _die(self):
        if self.owner.type == 'rival':
            exp_amt = (self.config['base_exp'] * self.level) / 7    # generic exp calculation
            self.e['World'].player.active_pokemon.gain_exp(exp_amt)
        self.alive = False

    def damage(self, amt):
        self.damage_taken = amt

    def gain_exp(self, amt):
        self.exp += amt
        self._process_exp()

    def update(self):
        self.healthbar.update()

        self._calculate_stats()

        # used to tick down health instead of just subtracting it all at once
        tick_damage = 0.1
        if self.damage_taken > 0:
            # storing the health in a temporary variable to make sure it is non-negative
            self.damage_taken -= tick_damage
            temp_health = self.current_hp
            temp_health -= tick_damage
            self.current_hp = max(0, temp_health)

            # blinking animation when hit
            if self.blink_timer > 0:
                self.img.set_alpha(255)
            elif self.blink_timer <= 0 and self.blink_timer > -7:
                self.img.set_alpha(0)
            else:
                self.blink_timer = 10
            self.blink_timer -= 1

            if self.current_hp == 0:
                self._die()
        else:
            self.img.set_alpha(255)

        # updating afflictions if there are any
        if self.afflictions:
            for i, afflicion in itr(self.afflictions):
                alive = afflicion.update()
                if not alive:
                    self.afflictions.pop(i)

        if self.e['Input'].mouse_state['right_click']:
            self.gain_exp(1)

    def render(self, surf, pos):
        surf.blit(self.img, (pos[0], pos[1] + 40))
        self.healthbar.render(surf)

    def __repr__(self):
        return f'hp: {self.current_hp}, atk: {self.attack}, def: {self.defense}, sp_atk: {self.special_attack}, sp_def: {self.special_defense}, speed: {self.speed}'
    
    def __str__(self):
        gender = 'female' if self.female else 'male'
        return f'{self.name}, {gender}, {self.shiny}'