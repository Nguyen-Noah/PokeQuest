import pygame, random, os, json
from utils.elements import ElementSingleton

class Lottery(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.num_pulls = 0
        self.load_probabilities()
        
    def load_probabilities(self):
        path = 'data/pokemon'
        for dir in os.listdir(path):
            for file in os.listdir(path + '/' + dir):
                if file == 'config.json':
                    with open(path + '/' + dir + '/' + file, 'r') as f:
                        print(dir + ' ' + f)

    def pull(self):
        self.num_pulls += 1