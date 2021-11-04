from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted.baselines import Scripted, Combat, Meander
from neural_mmo.forge.trinity.scripted.io import Observation
import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils

import random

class TechnologyAgent(Meander):
    name = "Technology_"

    def __call__(self, obs):
        super().__call__(obs)

        return self.actions

    def insertIntoInventory(self, config, actions, itemType, numItems):

        item = Item(ItemType.SMALL_ROCK)

        if itemType == "LARGE_BOULDER":
            item = Item(ItemType.LARGE_BOULDER)
        elif itemType == "SMALL_STICK":
            item = Item(ItemType.SMALL_STICK)
        elif itemType == "LARGE_BRANCH":
            item = Item(ItemType.LARGE_BRANCH)

        items = []

        for i in range(numItems):
            items.append(item)

        actions[Action.InventoryInsertion] = {Action.InventoryItem: items}

    def removeFromInventory(self, config, actions, type, numItems):
        itemType = ItemType.SMALL_ROCK

        if type == "large LARGE_BOULDER":
            itemType = ItemType.LARGE_BOULDER
        elif type == "LARGE_BRANCH":
            itemType = ItemType.LARGE_BRANCH
        elif type == "SMALL_STICK":
            itemType = ItemType.SMALL_STICK

        actions[Action.InventoryRemoval] = {Action.ItemType: itemType, numItems: numItems}