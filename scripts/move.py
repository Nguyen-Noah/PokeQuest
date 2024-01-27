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