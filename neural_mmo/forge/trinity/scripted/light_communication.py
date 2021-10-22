import numpy as np

from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.blade.io.action import static as Action

from neural_mmo.forge.trinity.scripted import io, utils


def signal(config, actions, light):
    # actions[Action.Signal] = {Action.Light: light}
    actions["comm"] = light