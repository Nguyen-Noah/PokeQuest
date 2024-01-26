from utils.elements import ElementSingleton

class Renderer(ElementSingleton):
    def __init__(self):
        super().__init__()

    def update(self):
        surf = self.e['Window'].display
        self.e['World'].render(surf)