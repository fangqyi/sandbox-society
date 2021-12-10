from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted import io, move
from neural_mmo.forge.trinity.scripted.baselines import Meander, Scripted
from neural_mmo.forge.blade.io.action import static as Action
from neural_mmo.forge.trinity.scripted.io import Observation
from neural_mmo.forge.blade.lib import material

from random import randint

'''
Duke CS390 Fall 2021: AI Sandbox
Scripted Agent for map interaction.
'''
class MapAgent(Meander):
    name = "Map_"

    def __call__(self, obs):
        super().__call__(obs)

        self.ob = io.Observation(self.config, obs)
        tile = self.ob.tile(0, 0)

        self.pickUpItems(self.config, self.actions) # pick up items from map
        # self.dropItems(self.config, self.actions)

        return self.actions

    def pickUpItems(self, config, actions):
        actions[Action.PickUpItem] = {}

    def dropItems(self, config, actions):
        actions[Action.DropItem] = {}

    def signal(self, config, actions, light):
        actions[Action.Signal] = {Action.Light: light}

'''
Duke CS390 Fall 2021: AI Sandbox
Scripted Agent for map interaction with technology.
'''
class TechnologyLightMapAgent(MapAgent):
    def __call__(self, obs):
        MapAgent.__call__(self, obs)
        self.ob = io.Observation(self.config, obs)

        # obtain rocks and sticks count
        rock_count = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        # signal a light based on what items are collected
        if rock_count == stick_count: # if equal counts, signal white
            self.signal(self.config, self.actions, 0xffffff)
        elif rock_count > stick_count: # if more rocks, signal red
            self.signal(self.config, self.actions, 0xff0000)
        elif stick_count > rock_count: # if more sticks, signal blue
            self.signal(self.config, self.actions, 0x0000ff)
        return self.actions

'''
Duke CS390 Fall 2021: AI Sandbox, Maverick Chung
Scripted Agent for social behavior.
'''
class SocialAgent(MapAgent):
    def __call__(self, obs):
        MapAgent.__call__(self, obs)
        self.ob = io.Observation(self.config, obs)
        my_light = Observation.attribute(self.ob.agent, Stimulus.Entity.Communication) # obtain agent's light
        my_light = int(my_light)
        my_type = None

        #red = stick, blue = stone
        if my_light == 0:
            my_type = "stick" if randint(0,1) else "stone"
        elif my_light>>16 > my_light & 255:
            my_type = "stick"
        else:
            my_type = "stone"

        # self.explore()

        vis = self.config.NSTIM
        for r in range(-1, 2):
            for c in range(-1, 2):
                tile = self.ob.tile(r, c)
                Tile = Stimulus.Tile
                matl     = io.Observation.attribute(tile, Tile.Index)
                if matl == material.Forest.index and my_type == "stick":
                    self.actions[Action.Gather] = {Action.Direction: (r,c)}
                if matl == material.Orerock.index and my_type == "stone":
                    self.actions[Action.Gather] = {Action.Direction: (r,c)}

        new_light = 0xff0000 if my_type == "stick" else 0xff
        self.signal(self.config, self.actions, new_light)

        my_sticks =  Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks)
        my_stones =  Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks)

        for target in self.ob.agents:
            other_light = Observation.attribute(target, Stimulus.Entity.Communication)
            other_type = "stick" if my_light>>16 > my_light & 255 else "stone"
            other_sticks = Observation.attribute(target, Stimulus.Entity.SmallSticks)
            other_stones = Observation.attribute(target, Stimulus.Entity.SmallRocks)
            if my_type == other_type == "stick":
                num_to_give = 0
                if (my_sticks > other_sticks and my_sticks <= 5) or other_sticks > 5:
                    continue
                if my_sticks < other_sticks:
                    num_to_give = min(my_sticks, 5 - other_sticks)
                elif my_sticks > 5:
                    num_to_give = min(my_sticks - 5, 5 - other_sticks)
                if num_to_give <= 0:
                    continue
                my_sticks -= num_to_give
                self.actions[Action.GiveItems] = {Action.Direction: (target, ItemType.SMALL_STICK, num_to_give)}

            if my_type == other_type == "stone":
                num_to_give = 0
                if (my_stones > other_stones and my_stones <= 5) or other_stones > 5:
                    continue
                if my_stones < other_stones:
                    num_to_give = min(my_stones, 5 - other_stones)
                elif my_stones > 5:
                    num_to_give = min(my_stones - 5, 5 - other_stones)
                if num_to_give <= 0:
                    continue
                my_stones -= num_to_give
                self.actions[Action.GiveItems] = {Action.Direction: (target, ItemType.SMALL_ROCK, num_to_give)}

        return self.actions
