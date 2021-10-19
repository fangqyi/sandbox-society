from neural_mmo.forge.trinity.scripted.baselines import Scripted
from neural_mmo.forge.trinity.scripted import light_communication


class LightAgent(Scripted):

    def signal_blue(self):
        light_communication.signal(self.config, self.actions, "BLUE")

    def signal_purple(self):
        light_communication.signal(self.config, self.actions, "PURPLE")

    def signal_yellow(self):
        light_communication.signal(self.config, self.actions, "YELLOW")