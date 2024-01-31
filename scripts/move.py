import pygame
from utils.elements import Element
from .config import config

class Move(Element):
    def __init__(self, move, owner):
        super().__init__()
        self.name = move
        self.owner = owner
        self.trainer = self.owner.owner
        self.config = config['moves'][self.name]
        self.load()

    def load(self):
        self.accuracy = self.config['accuracy']
        self.damage_class = self.config['damage_class']
        self.effect_chance = self.config['effect_chance']
        self.power = self.config['power']
        self.pp = self.config['pp']
        self.priority = self.config['priority']
        self.target_type = self.config['target']
        self.type = self.config['type']

        self.stat_changes = self.config['stat_changes']

        m = self.config['meta']
        self.ailment = m['ailment']
        self.ailment_chance = m['ailment_chance']

        self.crit_rate = m['crit_rate']
        self.drain = m['drain']
        self.flinch_chance = m['flinch_chance']
        self.healing = m['healing']
        self.max_hits = m['max_hits']
        self.min_hits = m['min_hits']
        self.max_turns = m['max_turns']
        self.min_turns = m['min_turns']
        self.stat_chance = m['stat_chance']

    def set_target(self):
        if self.target_type in ['selected-pokemon', 'selected-pokemon-me-first']:
            self.target = self.e['World'].player.active_pokemon if self.trainer.type == 'rival' else self.e['Arena'].rival.active_pokemon

        else:
            self.target = self.config['target']

    def use(self):
        """
        possible targets:

        user
        selected-pokemon
        selected-pokmon-me-first
        all-pokemon
        specific-move
        users-field
        opponents-field
        entire-field
        """

        self.set_target()

        # generic damage calculation
        # Damage = (((2 * Level / 5 + 2) * Power * [Attack/Defense]) / 50 + 2) * Modifier
        # Modifier = targets * weather * badge * critical * random * STAB * type * burn * other

        if self.target_type in ['selected-pokemon', 'selected-pokemon-me-first']:
            if self.damage_class != 'status':
                if self.damage_class == 'physical':
                    var = self.owner.attack / self.target.defense
                elif self.damage_class == 'special':
                    var = self.owner.special_attack / self.target.special_defense

                damage = (((2 * self.owner.level / 5 + 2) * self.power * var) / 50 + 2)
                self.target.damage(damage)
            else:
                pass
        
        elif self.damage_class == 'all-pokemon':
            pass

        elif self.damage_class in ['users-field', 'opponents-field', 'entire-field']:
            pass