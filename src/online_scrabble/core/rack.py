from typing import List, Optional, Tuple

from .bag import Bag, BagError, WILD_LETTER
from .character import Character


RACK_LENGTH = 7


def populate_rack(rack: str, bag: Bag) -> str:
    try:
        for _ in range(len(rack), RACK_LENGTH):
            rack += bag.get_character()
    except BagError:
        pass
    return rack


def remove_letters_from_rack(rack: str, letters: List[Character]) -> str:
    for letter in letters:
        value = WILD_LETTER if letter.wild else letter.value
        rack = rack.replace(value, "", 1)
    return rack


def remove_index_from_rack(rack: str, index: int) -> str:
    return rack[:index] + rack[index + 1 :]


def find_wild_in_rack(rack: str, char: str) -> Tuple[Optional[Character], str]:
    index = rack.find(WILD_LETTER)

    if index == -1:
        return None, rack

    return Character(char, True), remove_index_from_rack(rack, index)


def find_in_rack(rack: str, char: str) -> Tuple[Optional[Character], str]:
    index = rack.find(char)

    if index == -1:
        return find_wild_in_rack(rack, char)

    return Character(char, False), remove_index_from_rack(rack, index)
