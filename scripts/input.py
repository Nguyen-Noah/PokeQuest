import pygame, sys
from pygame.locals import *
from utils.elements import ElementSingleton
from .config import config

class Input(ElementSingleton):
    def __init__(self):
        super().__init__()
        #pygame.event.set_grab(True)

        self.states = {}
        self.mouse_pos = (0, 0)

        self.input_mode = 'core'

        self.reset()

    def reset(self):
        for binding in config['input']:
            self.states[binding] = False

        self.mouse_state = {
            'left_click': False,
            'right_click': False,
            'left_hold': False,
            'right_hold': False,
            'left_release': False,
            'right_release': False,
            'scroll_down': False,
            'scroll_up': False
        }

    def hold_reset(self):
        for binding in config['input']:
            if config['input'][binding]['toggle'] == 'hold':
                self.states[binding] = False

    def soft_reset(self):
        for binding in config['input']:
            if config['input'][binding]['toggle'] == 'press':
                self.states[binding] = False

        for binding in self.mouse_state:
            self.mouse_state[binding] = False

    def set_input_mode(self, input_mode):
        self.input_mode = input_mode

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()

        self.soft_reset()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == 27):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                for binding in config['input']:
                    if set(config['input'][binding]['mode']).intersection({'all', self.input_mode}):
                        if config['input'][binding]['button'][0] == 'keyboard':
                            if config['input'][binding]['toggle'] in ['hold', 'press']:
                                if event.key in config['input'][binding]['button'][1]:
                                    self.states[binding] = True
            if event.type == KEYUP:
                for binding in config['input']:
                    if set(config['input'][binding]['mode']).intersection({'all', self.input_mode}):
                        if config['input'][binding]['button'][0] == 'keyboard':
                            if config['input'][binding]['toggle'] in ['hold', 'press']:
                                if event.key in config['input'][binding]['button'][1]:
                                    self.states[binding] = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_state['left_click'] = True
                    self.mouse_state['left_hold'] = True
                if event.button == 3:
                    self.mouse_state['right_click'] = True
                    self.mouse_state['right_hold'] = True
                if event.button == 4:
                    self.mouse_state['scroll_up'] = True
                if event.button == 5:
                    self.mouse_state['scroll_down'] = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_state['left_release'] = True
                    self.mouse_state['left_hold'] = False
                if event.button == 3:
                    self.mouse_state['right_release'] = True
                    self.mouse_state['right_hold'] = False