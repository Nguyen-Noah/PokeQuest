from enum import Enum, auto, unique

@unique
class Status(Enum):
    BRN = auto()
    FNT = auto()
    FRZ = auto()
    PAR = auto()
    PSN = auto()
    SLP = auto()
    TOX = auto()

    def __str__(self) -> str:
        return f'{self.name} (status) object'