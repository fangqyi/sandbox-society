from neural_mmo.forge.trinity.scripted.baselines import Scripted, Combat, Meander
from neural_mmo.forge.trinity.scripted.io import Observation
from neural_mmo.forge.trinity.scripted.map_agent import MapAgent
import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils

import random


class LightAgent(Meander):  # for some reason, subclassing off Scripted makes the agent not show up
    name = "Light_"

    lights = [0, 0x6e3caf, 0x57380f, 0x00525a]
    thresh = 2

    def __call__(self, obs):
        super().__call__(obs)

        d = {v: i for i, v in enumerate(self.lights)}
        my_ob = Observation.attribute(self.ob.agent, Stimulus.Entity.Communication)
        # print("My ob:", my_ob)
        own_light = d[my_ob] if my_ob in d else 0
        self.thresh = 2
        seen = {0: 0, 1: 0, 2: 0, 3: 0}
        if own_light:
            for agent in self.ob.agents:
                light = d[Observation.attribute(agent, Stimulus.Entity.Communication)]
                seen[light] += 1
            if seen[(own_light % 3) + 1] >= self.thresh:
                new_light = (own_light % 3) + 1
            else:
                new_light = own_light

        else:
            new_light = random.randint(1, 3)

        new_light = int(new_light)
        # print("new", self.lights[new_light])
        self.signal(self.config, self.actions, self.lights[new_light])

        return self.actions

    def signal(self, config, actions, light):
        actions[Action.Signal] = {Action.Light: light}


class LightMapAgent(LightAgent, MapAgent):
    def __call__(self, obs):
        LightAgent.__call__(self, obs)
        tile = self.ob.tile(0, 0)

        rock_count_prev = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count_prev = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        self.pickUpItems(self.config, self.actions)

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
