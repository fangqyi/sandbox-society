from neural_mmo.forge.trinity.scripted.baselines import Scripted
from neural_mmo.forge.trinity.scripted import light_communication
import random

class LightAgent(Scripted):

    def __call__(self, obs):
        super().__call__(obs)

        signals = [0, 1, 2]
        choice = random.choice(signals)
        if choice == 0:
            self.signal_blue()
        elif choice == 1:
            self.signal_purple()
        else:
            self.signal_yellow()

        return self.actions

    def signal_blue(self):
        light_communication.signal(self.config, self.actions, "BLUE")

    def signal_purple(self):
        light_communication.signal(self.config, self.actions, "PURPLE")

    def signal_yellow(self):
        light_communication.signal(self.config, self.actions, "YELLOW")