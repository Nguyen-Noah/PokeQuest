from enum import Enum, auto, unique
from .config import config

@unique
class PokemonType(Enum):
    BUG = auto()
    DARK = auto()
    DRAGON = auto()
    ELECTRIC = auto()
    FIGHT = auto()
    FIRE = auto()
    FLYING = auto()
    GHOST = auto()
    GRASS = auto()
    GROUND = auto()
    ICE = auto()
    NORMAL = auto()
    POISON = auto()
    PSYCHIC = auto()
    ROCK = auto()
    STEEL = auto()
    WATER = auto()

    def __str__(self):
        return f'{self.name} (pokemon type) object'
    
    def damage_multiplier(self, type_1, type_2):
        damage_multiplier = config['typechart'][type_1.name.lower()]['damageTaken'][self.name.lower().capitalize()]
        if type_2 is not None:
            return damage_multiplier * config['typechart'][type_2.name.lower()]['damageTaken'][self.name.lower().capitalize()]
        
        return damage_multiplier
    
    @staticmethod
    def from_name(name):
        return PokemonType[name.upper()]