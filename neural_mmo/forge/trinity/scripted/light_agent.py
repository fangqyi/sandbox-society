from neural_mmo.forge.trinity.scripted.baselines import Scripted, Combat, Meander
from neural_mmo.forge.trinity.scripted.io import Observation
from neural_mmo.forge.trinity.scripted.map_agent import MapAgent
import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils

import random

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
Scripted Agent for light communication. Implements rock paper scissors.
'''
class LightAgent(Meander):
    name = "Light_"

    lights = [0, 0x6e3caf, 0x57380f, 0x00525a] # Possible lights.
    thresh = 2 # Threshold for changing lights.

    def __call__(self, obs):
        super().__call__(obs)

        d = {v: i for i, v in enumerate(self.lights)}
        my_ob = Observation.attribute(self.ob.agent, Stimulus.Entity.Communication) # obtain observations.
        # print("My ob:", my_ob)
        own_light = d[my_ob] if my_ob in d else 0 # check own light
        self.thresh = 2
        seen = {0: 0, 1: 0, 2: 0, 3: 0} # dictionary of seen lights
        if own_light:
            for agent in self.ob.agents: # iterate through agents
                light = d[Observation.attribute(agent, Stimulus.Entity.Communication)] # obtain light of agent
                seen[light] += 1 # add to dictionary of seen lights
            if seen[(own_light % 3) + 1] >= self.thresh: # check if the count of the light that beats own light is greater than threshold
                new_light = (own_light % 3) + 1 # set new light
            else:
                new_light = own_light # keep old light

        else:
            new_light = random.randint(1, 3) # no light so set it to random

        new_light = int(new_light)
        # print("new", self.lights[new_light])
        self.signal(self.config, self.actions, self.lights[new_light]) # signal the new light

        return self.actions

    # Method to signal light
    def signal(self, config, actions, light):
        actions[Action.Signal] = {Action.Light: light}

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
Scripted Agent for light communication based on map iteraction.
'''
class LightMapAgent(LightAgent, MapAgent):
    def __call__(self, obs):
        LightAgent.__call__(self, obs)
        tile = self.ob.tile(0, 0) # obtain tile

        # get counts of rocks and sticks within inventory for previous time step
        rock_count_prev = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count_prev = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        # pick up items from tile
        self.pickUpItems(self.config, self.actions)

        # get counts of rocks and sticks within inventory for current time step
        rock_count_curr = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallRocks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBoulders)
        stick_count_curr = Observation.attribute(self.ob.agent, Stimulus.Entity.SmallSticks) + Observation.attribute(
            self.ob.agent, Stimulus.Entity.LargeBranches)

        # check if rocks or sticks have been collected
        rock_collected = rock_count_prev < rock_count_curr
        stick_collected = stick_count_prev < stick_count_curr

        # update the light based on what has been collected
        if rock_collected and stick_collected: # both rocks and sticks: purple
            self.signal(self.config, self.actions, 0x6a0dad)
        elif rock_collected: # only rocks: red
            self.signal(self.config, self.actions, 0xff0000)
        elif stick_collected: # only sticks: blue
            self.signal(self.config, self.actions, 0x0000ff)

        return self.actions
