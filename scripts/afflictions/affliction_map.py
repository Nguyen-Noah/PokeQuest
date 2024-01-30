from .burn import Burn
from .confusion import Confusion
from .curse import Curse
from .freeze import Freeze
from .infatuation import Infatuation
from .nightmare import Nightmare
from .paralysis import Paralysis
from .poison import Poison
from .sleep import Sleep

primary_status = {
    'burn': Burn,
    'freeze': Freeze,
    'paralysis': Paralysis,
    'poison': Poison,
    'sleep': Sleep
}

secondary_status = {
    'confusion': Confusion,
    'infatuation': Infatuation,
    'curse': Curse
}


"""
none
paralysis
leech-seed
poison
confusion
infatuation
ingrain
sleep
burn
no-type-immunity
freeze
trap
unknown
disable
torment
perish-song
yawn
nightmare
embargo
heal-block
"""