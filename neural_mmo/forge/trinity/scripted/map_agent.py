from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted import io, move
from neural_mmo.forge.trinity.scripted.baselines import Meander
from neural_mmo.forge.blade.io.action import static as Action
from neural_mmo.forge.trinity.scripted.io import Observation

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
Duke CS390 Fall 2021: AI Sandbox
Scripted Agent for social behavior.
'''
class SocialAgent(MapAgent):
    def __call__(self, obs):
        MapAgent.__call__(self, obs):
        self.ob = io.Observation(self.config, obs)
        my_light = Observation.attribute(self.ob.agent, Stimulus.Entity.Communication) # obtain agent's light
        my_type = None

        #red = stick, blue = stone
        if my_light == 0:
            my_type = "stick" if randint(0,1) else "stone"
        elif my_light>>16 > my_light & 255:
            my_type = "stick"
        else:
            my_type = "stone"

        self.explore()

        
