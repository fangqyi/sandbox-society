from neural_mmo.forge.trinity.scripted.baselines import Scripted, Combat
import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils

import random

class LightAgent(Combat):
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
        self.signal(self.config, self.actions, random.randint(0,3))

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