import pygame, random
from utils.elements import Element
from utils.core_funcs import load_config, filter_asset
from .move import Move

class Pokemon(Element):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.config = load_config(self.name)
        self.load()
        print(self.active_moves)

    def load(self):
        # female/shiny -------- #
        self.female = self.config['misc']['gender_rate'] > random.randint(0, 8)
        self.shiny = random.randint(1, 8192) == 1

        # stats --------------- #
        self.hp = sum(self.config['base_stats']['hp'])
        self.attack = sum(self.config['base_stats']['attack'])
        self.defense = sum(self.config['base_stats']['defense'])
        self.special_attack = sum(self.config['base_stats']['special-attack'])
        self.special_defense = sum(self.config['base_stats']['special-defense'])
        self.speed = sum(self.config['base_stats']['speed'])

        self.level = 0
        self.exp = 0

        # moves --------------- #
        self.active_moves = []
        for move in self.config['moves']:
            for learn_method in self.config['moves'][move]:
                if learn_method['learn_method'] == 'level-up' and learn_method['level_learned'] == 1:
                    self.active_moves.append(Move(move))

        # assets -------------- #
        self.assets = filter_asset(self.e['Assets'].pokemon[self.name], self.female, self.shiny)

    def gain_exp(self, amt):
        self.exp += amt

    def __repr__(self):
        return f'hp: {self.hp}, atk: {self.attack}, def: {self.defense}, sp_atk: {self.special_attack}, sp_def: {self.special_defense}, speed: {self.speed}'
    
    def __str__(self):
        gender = 'female' if self.female else 'male'
        return f'{self.name}, {gender}, {self.shiny}'