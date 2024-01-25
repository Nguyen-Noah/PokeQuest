import pygame
from utils.elements import ElementSingleton
from .config import config

class Window(ElementSingleton):
    def __init__(self):
        super().__init__()
        
        # pygame initialization ------------------------------------------- #
        pygame.init()

        # FULLSCREEN BORDERLESS
        self.scaled_resolution = config['window']['scaled_resolution']
        #self.base_resolution = config['window']['base_resolution']

        self.display = pygame.display.set_mode(self.scaled_resolution)
        #self.display = pygame.Surface(self.base_resolution)
        pygame.display.set_caption(config['window']['title'])

        self.clock = pygame.time.Clock()

    def update(self):
        #self.screen.blit(pygame.transform.scale(self.display, self.scaled_resolution), (0, 0))
        pygame.display.flip()
        self.clock.tick(config['window']['fps'])