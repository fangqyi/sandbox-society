from neural_mmo.forge.trinity.scripted.baselines import Scripted, Combat
from neural_mmo.forge.trinity.scripted.io import Observation
import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils

import random

class LightAgent(Combat): # for some reason, subclassing off Scripted makes the agent not show up
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

        chance = 2*(random.randint(0,100)==0)
        for agent in self.ob.agents:
            if Observation.attribute(agent, Stimulus.Entity.Communication):
                if random.randint(0,1) == 0:
                    chance = 2
        if Observation.attribute(self.ob.agent, Stimulus.Entity.Communication):
            chance = 2

        self.signal(self.config, self.actions, chance)

        return self.actions

    def signal_blue(self):
        self.signal(self.config, self.actions, "BLUE")

    def signal_purple(self):
        self.signal(self.config, self.actions, "PURPLE")

    def signal_yellow(self):
        self.signal(self.config, self.actions, "YELLOW")

    def signal(self, config, actions, light):
        actions[Action.Signal] = {Action.Light: light}
        # actions["comm"] = light