from utils.elements import ElementSingleton
from scripts.window import Window
from scripts.assets import Assets
from scripts.input import Input
from scripts.renderer import Renderer
from scripts.world import World
from scripts.audio import Audio

class Game(ElementSingleton):
    def __init__(self):
        super().__init__()
        
        # initializing singletons ----------------------------------------- #
        self.window = Window()
        self.assets = Assets()
        self.input = Input()
        self.renderer = Renderer()
        self.world = World()
        self.audio = Audio()

    def update(self):
        self.input.update()
        self.window.update()
        self.world.update()
        self.renderer.update()

    def run(self):
        while True:
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()