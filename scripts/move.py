import pygame
from utils.elements import Element
from .config import config

class Move(Element):
    def __init__(self, move, owner):
        super().__init__()
        self.name = move
        self.owner = owner
        self.config = config['moves'][self.name]
        self.load()

    def load(self):
        self.accuracy = self.config['accuracy']
        self.damage_class = self.config['damage_class']
        self.effect_chance = self.config['effect_chance']
        self.power = self.config['power']
        self.pp = self.config['pp']
        self.priority = self.config['priority']
        self.target = self.config['target']
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

    def use(self, target):
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

        # generic damage calculation
        # Damage = (((2 * Level / 5 + 2) * Power * [Attack/Defense]) / 50 + 2) * Modifier
        # Modifier = targets * weather * badge * critical * random * STAB * type * burn * other

        if self.damage_class in ['selected-pokemon', 'selected-pokemon-me-first']:
            if self.damage_class == 'physical':
                var = self.owner.attack / target.defense
            elif self.damage_class == 'special':
                var = self.owner.special_attack / target.special_defense

            damage = (((2 * self.owner.level / 5 + 2) * self.power * var) / 50 + 2)
            target.damage(damage)
        
        elif self.damage_class == 'all-pokemon':
            pass

        elif self.damage_class in ['users-field', 'opponents-field', 'entire-field']:
            pass