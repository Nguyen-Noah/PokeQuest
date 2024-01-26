import pygame, random, os, json
from utils.elements import ElementSingleton
from utils.core_funcs import load_config
from .pokemon import Pokemon

class Lottery(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.num_pulls = 0
        self.load_probabilities()
        
    def load_probabilities(self):
        path = 'data/pokemon'
        self.base_pokemon_probabilities = {}
        for dir in os.listdir(path):
            with open(path + '/' + dir + '/config.json', 'r') as f:
                data = json.load(f)
                if data['base_evolution']:
                    self.base_pokemon_probabilities[dir] = data['misc']['rate']

    def pull(self):
        self.num_pulls += 1
        pokemon_name = random.choices(list(self.base_pokemon_probabilities.keys()), list(self.base_pokemon_probabilities.values()), k=1)[0]
        self.e['World'].player.add_pokemon(pokemon_name)