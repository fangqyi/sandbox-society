from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted import io
from neural_mmo.forge.trinity.scripted.baselines import Meander
from neural_mmo.forge.blade.io.action import static as Action
from neural_mmo.forge.trinity.scripted.io import Observation


class TechnologyAgent(Meander):
    name = "Technology_"

    def __call__(self, obs):
        super().__call__(obs)

        self.ob = io.Observation(self.config, obs)
        agent = self.ob.agent
        self.food = io.Observation.attribute(agent, Stimulus.Entity.Food)
        self.water = io.Observation.attribute(agent, Stimulus.Entity.Water)

        shield_status = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallStoneTechnology)
        sword_status = Observation.attribute(self.ob.agent, Stimulus.Entity.LargeBoulderTechnology)
        hoe_status = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallStickTechnology)
        improved_hoe_status = Observation.attribute(self.ob.agent, Stimulus.Entity.LargeBranchTechnology)

        # print(shield_status, sword_status, hoe_status, improved_hoe_status)

        if self.food >= 10:
            # print("obtained small stick")
            self.insertIntoInventory(self.config, self.actions, "SMALL_STICK", 1)
            if hoe_status == 1.0:
                # print("obtained large branch")
                self.insertIntoInventory(self.config, self.actions, "LARGE_BRANCH", 1)

        if self.water >= 10:
            # print("obtained small rock")
            self.insertIntoInventory(self.config, self.actions, "SMALL_ROCK", 1)
            if shield_status == 1.0:
                # print("obtained large boulder")
                self.insertIntoInventory(self.config, self.actions, "LARGE_BOULDER", 1)

        if shield_status == 1.0 or sword_status == 1.0 or hoe_status == 1.0 or improved_hoe_status == 1.0:
            print("obtained tech")
            self.checkTechnology(self.config, self.actions)

        if shield_status == 1.0 and sword_status == 1.0 and hoe_status == 1.0 and improved_hoe_status == 1.0:
            print("resetting technology")
            self.removeFromInventory(self.config, self.actions, "LARGE_BOULDER", 1)
            self.removeFromInventory(self.config, self.actions, "SMALL_ROCK", 1)
            self.removeFromInventory(self.config, self.actions, "LARGE_BRANCH", 1)
            self.removeFromInventory(self.config, self.actions, "SMALL_STICK", 1)
            self.checkTechnology(self.config, self.actions)

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

        if type == "LARGE_BOULDER":
            itemType = ItemType.LARGE_BOULDER
        elif type == "LARGE_BRANCH":
            itemType = ItemType.LARGE_BRANCH
        elif type == "SMALL_STICK":
            itemType = ItemType.SMALL_STICK

        actions[Action.InventoryRemoval] = {Action.ItemType: itemType, numItems: numItems}

    def checkTechnology(self, config, actions):
        actions[Action.TechnologyStatus] = {}

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