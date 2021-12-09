from neural_mmo.forge.blade.item import item, armor
from neural_mmo.forge.blade.item.item import Item, ItemType
from neural_mmo.forge.blade.systems.equipment import Armor


class Inventory:
    def __init__(self):
        self.items = dict()
        self.technology = dict()

        # SMALL_STICK = 5
        # LARGE_BRANCH = 6
        # SMALL_ROCK = 7
        # LARGE_BOULDER = 8

    '''
    Duke CS390 Fall 2021: AI Sandbox
    Method to obtain stone technology status from inventory.
    '''
    def checkStoneTechnologyStatus(self):
        small_rock_status = False
        large_boulder_status = False
        small_rock_amount = self.getItemAmount(ItemType.SMALL_ROCK)
        if small_rock_amount >= 10:
            small_rock_status = True
        large_boulder_amount = self.getItemAmount(ItemType.LARGE_BOULDER)
        if large_boulder_amount >= 10:
            large_boulder_status = True
        return small_rock_status, large_boulder_status

    '''
    Duke CS390 Fall 2021: AI Sandbox
    Method to obtain wood technology status from inventory.
    '''
    def checkWoodTechnologyStatus(self):
        small_stick_status = False
        large_branch_status = False
        small_stick_amount = self.getItemAmount(ItemType.SMALL_STICK)
        if small_stick_amount >= 10:
            small_stick_status = True
        large_branch_amount = self.getItemAmount(ItemType.LARGE_BRANCH)
        if large_branch_amount >= 10:
            large_branch_status = True
        return small_stick_status, large_branch_status

    '''
    Duke CS390 Fall 2021: AI Sandbox
    Method to obtain the amount of a certain item.
    '''
    def getItemAmount(self, item_type):
        if item_type not in self.items.keys():
            return 0
        else:
            return self.items[item_type]

    '''
    Duke CS390 Fall 2021: AI Sandbox
    Method to check if the inventory has a certain item amount.
    '''
    def hasItems(self, item_type, item_amount):
        if self.items[item_type] >= item_amount:
            return True
        return False

    '''
    Duke CS390 Fall 2021: AI Sandbox
    Method to remove items from the inventory.
    '''
    def removeItems(self, item_type, item_amount):
        if item_type not in self.items or self.items[item_type] < item_amount:
            # print("not enough to remove")
            return False
        else:
            for i in range(item_amount):
                # print("remove: ", item_type)
                self.items[item_type] = self.items[item_type] - 1
            return True

    '''
    Duke CS390 Fall 2021: AI Sandbox
    Method to insert items into the inventory.
    '''
    def insertItems(self, items_list):
        for item_ele in items_list:
            # print("insert: ", item_ele.item_type)
            if item_ele.item_type in self.items.keys():
                self.items[item_ele.item_type] = self.items[item_ele.item_type] + 1
            else:
                self.items[item_ele.item_type] = 1


'''
Duke CS390 Fall 2021: AI Sandbox
Test for inventory interactions.
'''
def runInventoryTest():
    test_inv = Inventory()
    test_inv.insertItems([
        Item(ItemType.COAL),
        Item(ItemType.COAL),
        Item(ItemType.COAL),
        Item(ItemType.COAL)
    ])
    test_inv.insertItems([
        Item(ItemType.GOLD),
        Item(ItemType.DIRT),
        Item(ItemType.DIRT),
        Item(ItemType.IRON)
    ])
    print("has 4 coal:", test_inv.hasItems(ItemType.COAL, 4))
    print("has 6 coal:", test_inv.hasItems(ItemType.COAL, 6))
    print(test_inv.removeItems(ItemType.COAL, 2))
    print("has 4 coal:", test_inv.hasItems(ItemType.COAL, 4))
    print("gold amount:", test_inv.getItemAmount(ItemType.GOLD))
    print("small stick amount:", test_inv.getItemAmount(ItemType.SMALL_STICK))
    print("wood tech status:", test_inv.checkWoodTechnologyStatus())
    test_inv.insertItems([
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK),
        Item(ItemType.SMALL_STICK)
    ])
    print("small stick amount:", test_inv.getItemAmount(ItemType.SMALL_STICK))
    print("wood tech status:", test_inv.checkWoodTechnologyStatus())
    print("stone tech status:", test_inv.checkStoneTechnologyStatus())

if __name__ == '__main__':
    runInventoryTest()
