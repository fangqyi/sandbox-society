from neural_mmo.forge.blade.item import item, armor
from neural_mmo.forge.blade.item.item import Item
from neural_mmo.forge.blade.systems.equipment import Armor


class Inventory:
    def __init__(self, config):
        # self.ammo = 0
        self.items = []
        # self.resetArmor()
        # self.resetMelee()
        # self.resetRanged()

    # def resetArmor(self):
    #    self.armor = Armor.Base()
    #
    # def resetMelee(self):
    #    self.melee = Item.Base()
    #
    # def resetRanged(self):
    #    self.ranged = Item.Base()

    def insertItem(self, item):
        self.items.append(item)

    def simplifiedInventory(self):
        inv = dict()
        for item_ele in self.items:
            if item_ele.item_type in inv:
                inv[item_ele.item_type] = inv[item_ele.item_type] + 1
            else:
                inv[item_ele.item_type] = 1
        return inv
