from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.item.item import ItemType, Item
from neural_mmo.forge.trinity.scripted import io
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

        tile = self.ob.tile(0, 0)

        rock_count_prev = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count_prev = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        MapAgent.__call__(self, obs)
        # self.pickUpItems(self.config, self.actions)

        rock_count_curr = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count_curr = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        rock_collected = rock_count_prev < rock_count_curr
        stick_collected = stick_count_prev < stick_count_curr

        if rock_collected and stick_collected:
            self.signal(self.config, self.actions, 0x6a0dad)
        elif rock_collected:
            self.signal(self.config, self.actions, 0xff0000)
        elif stick_collected:
            self.signal(self.config, self.actions, 0x0000ff)

        return self.actions


