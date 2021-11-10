from neural_mmo.forge.trinity.scripted.baselines import Scripted, Combat, Meander
from neural_mmo.forge.trinity.scripted.io import Observation
import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils

import random

class LightAgent(Meander): # for some reason, subclassing off Scripted makes the agent not show up
    name = "Light_"

    def __call__(self, obs):
        super().__call__(obs)

        # signals = [0, 1, 2]
        # choice = random.choice(signals)
        # if choice == 0:
        #     self.signal_blue()
        # elif choice == 1:
        #     self.signal_purple()
        # else:
        #     self.signal_yellow()

        own_light = Observation.attribute(self.ob.agent, Stimulus.Entity.Communication)
        thresh = 2
        seen = {0:0, 1:0, 2:0, 3:0}
        if own_light:
            for agent in self.ob.agents:
                light = Observation.attribute(agent, Stimulus.Entity.Communication)
                seen[light] += 1
            if seen[(own_light%3)+1] >= thresh:
                new_light = (own_light%3)+1
            else:
                new_light = own_light

        else:
            new_light = random.randint(1,3) 

        new_light = int(new_light)
        self.signal(self.config, self.actions, new_light)

        return self.actions

    def signal_blue(self):
        self.signal(self.config, self.actions, "BLUE")

    def signal_purple(self):
        self.signal(self.config, self.actions, "PURPLE")

    def signal_yellow(self):
        self.signal(self.config, self.actions, "YELLOW")

    def signal(self, config, actions, light):
        actions[Action.Signal] = {Action.Light: light}