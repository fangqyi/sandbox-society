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

