from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted import io, move
from neural_mmo.forge.trinity.scripted.baselines import Meander
from neural_mmo.forge.blade.io.action import static as Action
from neural_mmo.forge.trinity.scripted.io import Observation


class MapAgent(Meander):
    name = "Map_"

    def __call__(self, obs):
        super().__call__(obs)

        self.ob = io.Observation(self.config, obs)
        tile = self.ob.tile(0, 0)

        self.pickUpItems(self.config, self.actions)
        # self.dropItems(self.config, self.actions)

        return self.actions

    def pickUpItems(self, config, actions):
        actions[Action.PickUpItem] = {}

    def dropItems(self, config, actions):
        actions[Action.DropItem] = {}

    def signal(self, config, actions, light):
        actions[Action.Signal] = {Action.Light: light}

class TechnologyLightMapAgent(MapAgent):
    def __call__(self, obs):
        MapAgent.__call__(self, obs)
        self.ob = io.Observation(self.config, obs)

        rock_count = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        if rock_count == stick_count:
            self.signal(self.config, self.actions, 0xffffff)
        elif rock_count > stick_count:
            self.signal(self.config, self.actions, 0xff0000)
        elif stick_count > rock_count:
            self.signal(self.config, self.actions, 0x0000ff)
        else:
            self.signal(self.config, self.actions, 0)
        return self.actions

class SocialAgent(MapAgent):
    def __call__(self, obs):
        MapAgent.__call__(self, obs):
        self.ob = io.Observation(self.config, obs)
        my_light = Observation.attribute(self.ob.agent, Stimulus.Entity.Communication)
        my_type = None

        #red = stick, blue = stone
        if my_light == 0:
            my_type = "stick" if randint(0,1) else "stone"
        elif my_light>>16 > my_light & 255:
            my_type = "stick"
        else:
            my_type = "stone"

        self.explore()

        
