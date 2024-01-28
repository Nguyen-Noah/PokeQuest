import pygame
from utils.elements import ElementSingleton
from .player import Player
from .lottery import Lottery
from .arena import Arena
from .rival import Rival
from utils.core_funcs import center_img_x

class World(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.load()

        self.fighting = False
        self.arena_created = False

    def load(self):
        self.player = Player((0, 0))
        self.lottery = Lottery()

    def update(self):
        if self.arena_created:
            self.arena.update()
        else:
            rival = Rival('lyra')
            self.arena = Arena(rival)
            self.arena_created = True            

        if self.e['Input'].mouse_state['left_click']:
            pass
            #self.lottery.pull()

    def render(self, surf):
        if self.arena_created:
            self.arena.render(surf)