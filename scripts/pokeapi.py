import random
import pokebase as pb
from utils.elements import ElementSingleton

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

class Pokebase(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.pokedex_len = 1025

    async def get_pokemon(self):
        random_pokemon = random.randint(1, self.pokedex_len)
        pokemon = pb.pokemon(random_pokemon)
        return pokemon