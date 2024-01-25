import pygame
from utils.elements import Element
from utils.core_funcs import load_config, filter_asset

class Pokemon(Element):
    def __init__(self, name, female=False, shiny=False):
        super().__init__()
        self.name = name
        self.female = female
        self.shiny = shiny
        self.config = load_config(self.name)
        self.load()

    def load(self):
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

        # assets -------------- #
        self.assets = filter_asset(self.e['Assets'].pokemon[self.name], self.female, self.shiny)

    def gain_exp(self, amt):
        self.exp += amt

    def __repr__(self):
        return f'hp: {self.hp}, atk: {self.attack}, def: {self.defense}, sp_atk: {self.special_attack}, sp_def: {self.special_defense}, speed: {self.speed}'
    
    def __str__(self):
        return self.name