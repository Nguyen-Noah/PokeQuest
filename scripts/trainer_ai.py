import pygame
from utils.elements import Element

class TrainerAI(Element):
    def __init__(self, parent, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.parent = parent
        