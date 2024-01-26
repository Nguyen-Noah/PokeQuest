import pygame
from utils.elements import Element
from .config import config

class Move(Element):
    def __init__(self, move):
        super().__init__()
        self.name = move
        self.config = config['moves'][self.name]
        self.load()

    def load(self):
        self.accuracy = self.config['accuracy']
        self.effect_chance = self.config['effect_chance']
        self.pp = self.config['pp']
        self.priority = self.config['priority']
        self.power = self.config['power']

        category_config = self.config['category']
        self.category = category_config['name']
        self.min_hits = category_config['min_hits']
        self.max_hits = category_config['max_hits']
        self.min_turns = category_config['min_turns']
        self.max_turns = category_config['max_turns']
        self.drain = category_config['drain']
        self.healing = category_config['healing']
        self.crit_rate = category_config['crit_rate']
        self.ailment_chance = category_config['ailment_chance']
        self.flinch_chance = category_config['flinch_chance']
        self.stat_chance = category_config['stat_chance']