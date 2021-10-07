from neural_mmo.forge.blade.item import item, armor
from neural_mmo.forge.blade.item.item import Item, ItemType
from neural_mmo.forge.blade.systems.equipment import Armor


class Inventory:
    def __init__(self):
        self.items = dict()

    def checkWoodTechnologyStatus(self):
        amount = self.getItemAmount(ItemType.SMALL_STICK)
        if amount >= 10:
            return True
        else:
            return False

    def getItemAmount(self, item_type):
        if item_type not in self.items.keys():
            return 0
        else:
            return self.items[item_type]

    def hasItems(self, item_type, item_amount):
        if self.items[item_type] >= item_amount:
            return True
        return False

    def removeItems(self, item_type, item_amount):
        if self.items[item_type] < item_amount:
            print("not enough to remove")
            return False
        else:
            for i in range(item_amount):
                print("remove: ", item_type)
                self.items[item_type] = self.items[item_type] - 1
            return True

    def insertItems(self, items_list):
        for item_ele in items_list:
            print("insert: ", item_ele.item_type)
            if item_ele.item_type in self.items.keys():
                self.items[item_ele.item_type] = self.items[item_ele.item_type] + 1
            else:
                self.items[item_ele.item_type] = 1


def runInventoryTest():
    test_inv = Inventory()
    test_inv.insertItems([
        Item(ItemType.COAL, "lump of coal"),
        Item(ItemType.COAL, "lump of coal"),
        Item(ItemType.COAL, "lump of coal"),
        Item(ItemType.COAL, "lump of coal")
    ])
    test_inv.insertItems([
        Item(ItemType.GOLD, "gold"),
        Item(ItemType.DIRT, "dirt"),
        Item(ItemType.DIRT, "dirt"),
        Item(ItemType.IRON, "iron")
    ])
    print("has 4 coal:", test_inv.hasItems(ItemType.COAL, 4))
    print("has 6 coal:", test_inv.hasItems(ItemType.COAL, 6))
    print(test_inv.removeItems(ItemType.COAL, 2))
    print("has 4 coal:", test_inv.hasItems(ItemType.COAL, 4))
    print("gold amount:", test_inv.getItemAmount(ItemType.GOLD))
    print("small stick amount:", test_inv.getItemAmount(ItemType.SMALL_STICK))
    print("wood tech status:", test_inv.checkWoodTechnologyStatus())
    test_inv.insertItems([
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick"),
        Item(ItemType.SMALL_STICK, "small stick")
    ])
    print("small stick amount:", test_inv.getItemAmount(ItemType.SMALL_STICK))
    print("wood tech status:", test_inv.checkWoodTechnologyStatus())


runInventoryTest()
