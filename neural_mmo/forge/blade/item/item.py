from enum import Enum


class Item:
    def __init__(self, item_type):
        self.item_type = item_type

    def getType(self):
        return self.item_type

class ItemType(Enum):
    RED_BERRY = 1
    BLUE_BERRY = 2
    YELLOW_BERRY = 3
    DIRT = 4
    SMALL_STICK = 5
    LARGE_BRANCH = 6
    SMALL_ROCK = 7
    LARGE_BOULDER = 8
    COAL = 9
    IRON = 10
    GOLD = 11
    MEAT = 12