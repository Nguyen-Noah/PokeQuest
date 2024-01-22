import pygame, math, random, sys, asyncio
from scripts.config import config
from utils.elements import ElementSingleton
from scripts.world import World
from scripts.input import Input
from scripts.pokeapi import Pokebase

class Game(ElementSingleton):
    def __init__(self):
        super().__init__()

        # pygame initialization ------------------------------------------- #
        pygame.init()

        self.display = pygame.display.set_mode(config['window']['resolution'])
        pygame.display.set_caption(config['window']['title'])

        self.clock = pygame.time.Clock()
        
        # initializing singletons ----------------------------------------- #
        self.world = World()
        self.input = Input()
        self.pb = Pokebase()

    def update(self):
        self.input.update()

        if self.input.mouse_state['left_click']:
            pokemon = asyncio.run(self.pb.get_pokemon())
            print(pokemon)

    def run(self):
        while True:
            self.update()
            pygame.display.flip()
            self.clock.tick(config['window']['fps'])

if __name__ == '__main__':
    game = Game()
    game.run()