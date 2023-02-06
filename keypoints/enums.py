from enum import Enum


class ClothType(Enum):
    BLOUSE = 'blouse'
    OUTWEAR = 'outwear'
    TROUSERS = 'trousers'
    SKIRT = 'skirt'
    DRESS = 'dress'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

