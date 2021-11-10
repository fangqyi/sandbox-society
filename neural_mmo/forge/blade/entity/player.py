import numpy as np
import random
from pdb import set_trace as T

from neural_mmo.forge.blade.systems import ai, equipment
from neural_mmo.forge.blade.lib import material

from neural_mmo.forge.blade.systems.skill import Skills
from neural_mmo.forge.blade.systems.achievement import Diary
from neural_mmo.forge.blade.entity import entity
from neural_mmo.forge.blade.io.stimulus import Static
from neural_mmo.forge.blade.systems.inventory import Inventory
from neural_mmo.forge.blade.item.item import Item, ItemType


class Player(entity.Entity):
    def __init__(self, realm, pos, agent):
        super().__init__(realm, pos, agent.iden, agent.name, agent.color, agent.pop)
        self.agent = agent
        self.pop = agent.pop
        self.inv = Inventory()

        # Communication light
        self.communication_light = 0

        # Scripted hooks
        self.target = None
        self.food = None
        self.water = None
        self.vision = 7

        # Submodules
        self.skills = Skills(self)
        self.achievements = Diary(realm.config)

        self.dataframe.init(Static.Entity, self.entID, self.pos)

    @property
    def serial(self):
        return self.population, self.entID

    @property
    def isPlayer(self) -> bool:
        return True

    @property
    def population(self):
        return self.pop

    def insertItemsIntoInventory(self, items):
        self.inv.insertItems(items)

    def removeItemsFromInventory(self, item_type, num_items):
        self.inv.removeItems(item_type, num_items)

    def getSwordStatus(self):
        small_stone_status, large_boulder_status = self.inv.checkStoneTechnologyStatus()
        return large_boulder_status

    def getShieldStatus(self):
        small_stone_status, large_boulder_status = self.inv.checkStoneTechnologyStatus()
        return small_stone_status

    def getHoeStatus(self):
        small_stick_status, large_branch_status = self.inv.checkWoodTechnologyStatus()
        return small_stick_status

    def getImprovedHoeStatus(self):
        small_stick_status, large_branch_status = self.inv.checkWoodTechnologyStatus()
        return large_branch_status

    def getLightNumeric(self):
        return self.communication_light

    def getLight(self):
        if self.communication_light == 0:
            return "OFF"
        elif self.communication_light == 1:
            return "PURPLE"
        elif self.communication_light == 2:
            return "YELLOW"
        elif self.communication_light == 3:
            return "BLUE"
        else:
            return "OFF"

    def setLight(self, color):
        if type(color) == int:
            self.communication_light = color
            return
        if color == "OFF":
            self.communication_light = 0
        elif color == "PURPLE":
            self.communication_light = 1
        elif color == "YELLOW":
            self.communication_light = 2
        elif color == "BLUE":
            self.communication_light = 3
        else:
            self.communication_light = 0


    def applyDamage(self, dmg, style): # ADD INVENTORY INTERACTION
        hoe_status = self.getHoeStatus()
        improved_hoe_status = self.getImprovedHoeStatus()
        chance = 0.5
        if hoe_status:
            chance = 0.75
        if improved_hoe_status:
            chance = 1.0

        if chance >= random.uniform(0, 1):
            self.resources.food.increment(dmg)
            self.resources.water.increment(dmg)

        self.skills.applyDamage(dmg, style)

    def receiveDamage(self, source, dmg): # ADD INVENTORY INTERACTION
        if not super().receiveDamage(source, dmg):
            if source:
                source.history.playerKills += 1
            return

        self.resources.food.decrement(dmg)
        self.resources.water.decrement(dmg)
        self.skills.receiveDamage(dmg)
        self.inv.removeItems(ItemType.GOLD, 2)

    def receiveLoot(self, loadout):
        if loadout.chestplate.level > self.loadout.chestplate.level:
            self.loadout.chestplate = loadout.chestplate
        if loadout.platelegs.level > self.loadout.platelegs.level:
            self.loadout.platelegs = loadout.platelegs

    def packet(self):
        data = super().packet()

        data['entID'] = self.entID
        data['annID'] = self.population

        data['base'] = self.base.packet()
        data['resource'] = self.resources.packet()
        data['skills'] = self.skills.packet()

        return data

    def update(self, realm, actions):
        '''Post-action update. Do not include history'''
        super().update(realm, actions)

        if not self.alive:
            return

        self.resources.update(realm, self, actions)
        self.skills.update(realm, self, actions)
        self.achievements.update(realm, self)
        # self.inventory.update(world, actions)
