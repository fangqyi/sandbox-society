from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted import io
from neural_mmo.forge.trinity.scripted.baselines import Meander
from neural_mmo.forge.blade.io.action import static as Action
from neural_mmo.forge.trinity.scripted.io import Observation

'''
Duke CS390 Fall 2021: AI Sandbox
Scripted Agent for technology.
'''
class TechnologyAgent(Meander):
    name = "Technology_"

    def __call__(self, obs):
        super().__call__(obs)

        self.ob = io.Observation(self.config, obs) # obtain observations
        agent = self.ob.agent
        self.food = io.Observation.attribute(agent, Stimulus.Entity.Food) # obtain food status from tile
        self.water = io.Observation.attribute(agent, Stimulus.Entity.Water) # obtain water status from tile

        # obtain all technology status
        shield_status = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallStoneTechnology)
        sword_status = Observation.attribute(self.ob.agent, Stimulus.Entity.LargeBoulderTechnology)
        hoe_status = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallStickTechnology)
        improved_hoe_status = Observation.attribute(self.ob.agent, Stimulus.Entity.LargeBranchTechnology)

        # print(shield_status, sword_status, hoe_status, improved_hoe_status)

        # if tile has enough food
        if self.food >= 10:
            # print("obtained small stick")
            # give agent a small stick
            self.insertIntoInventory(self.config, self.actions, "SMALL_STICK", 1)
            if hoe_status == 1.0: # if agent has small stick technology
                # print("obtained large branch")
                # give agent a large stick
                self.insertIntoInventory(self.config, self.actions, "LARGE_BRANCH", 1)

        # if tile has enough water
        if self.water >= 10:
            # print("obtained small rock")
            # give agent a small rock
            self.insertIntoInventory(self.config, self.actions, "SMALL_ROCK", 1)
            if shield_status == 1.0: # if agent has small rock technology
                # print("obtained large boulder")
                # give agent a large rock
                self.insertIntoInventory(self.config, self.actions, "LARGE_BOULDER", 1)

        # if agent has obtained a new technology, retrieve and send to frontend.
        if shield_status == 1.0 or sword_status == 1.0 or hoe_status == 1.0 or improved_hoe_status == 1.0:
            print("obtained tech")
            self.checkTechnology(self.config, self.actions)

        # if agent has all technology, remove 1 of each item from the agent.
        if shield_status == 1.0 and sword_status == 1.0 and hoe_status == 1.0 and improved_hoe_status == 1.0:
            print("resetting technology")
            self.removeFromInventory(self.config, self.actions, "LARGE_BOULDER", 1)
            self.removeFromInventory(self.config, self.actions, "SMALL_ROCK", 1)
            self.removeFromInventory(self.config, self.actions, "LARGE_BRANCH", 1)
            self.removeFromInventory(self.config, self.actions, "SMALL_STICK", 1)
            self.checkTechnology(self.config, self.actions)

        return self.actions

    # Method for inserting items into the agent's inventory.
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

    # Method for removing items from the agent's inventory.
    def removeFromInventory(self, config, actions, type, numItems):
        itemType = ItemType.SMALL_ROCK

        if type == "LARGE_BOULDER":
            itemType = ItemType.LARGE_BOULDER
        elif type == "LARGE_BRANCH":
            itemType = ItemType.LARGE_BRANCH
        elif type == "SMALL_STICK":
            itemType = ItemType.SMALL_STICK

        actions[Action.InventoryRemoval] = {Action.ItemType: itemType, numItems: numItems}

    # Method for checking the agent's technology status.
    def checkTechnology(self, config, actions):
        actions[Action.TechnologyStatus] = {}

    # Method for giving items to another agent.
    def giveItems(self, config, actions, entity, type, numItems):
        self.removeFromInventory(config, actions, type, numItems)
        item = Item(ItemType.SMALL_ROCK)

        if type == "LARGE_BOULDER":
            item = Item(ItemType.LARGE_BOULDER)
        elif type == "SMALL_STICK":
            item = Item(ItemType.SMALL_STICK)
        elif type == "LARGE_BRANCH":
            item = Item(ItemType.LARGE_BRANCH)

        items = []

        for i in range(numItems):
            items.append(item)

        actions[Action.GiveItems] = {entity: entity, Action.ItemType: itemType, numItems: numItems}