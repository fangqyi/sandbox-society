from pdb import set_trace as T
import numpy as np
import torch

from torch import nn

from forge.blade.lib.enums import Neon
from forge.blade.lib import enums
from forge.ethyr import torch as torchlib
from forge.ethyr.torch import policy, newpolicy
from forge.blade import entity

from forge.ethyr.torch.netgen.stim import Env

class ANN(nn.Module):
   def __init__(self, config):
      super().__init__()
      self.net = newpolicy.Net(config)
      self.config = config

   def forward(self, env, ent):
      atns, outs, val = self.net(env, ent)
      return atns, outs, val

   #Messy hooks for visualizers
   def visDeps(self):
      from forge.blade.core import realm
      from forge.blade.core.tile import Tile
      colorInd = int(12*np.random.rand())
      color    = Neon.color12()[colorInd]
      color    = (colorInd, color)
      ent = realm.Desciple(-1, self.config, color).server
      targ = realm.Desciple(-1, self.config, color).server

      sz = 15
      tiles = np.zeros((sz, sz), dtype=object)
      for r in range(sz):
         for c in range(sz):
            tiles[r, c] = Tile(enums.Grass, r, c, 1, None)

      targ.pos = (7, 7)
      tiles[7, 7].addEnt(0, targ)
      posList, vals = [], []
      for r in range(sz):
         for c in range(sz):
            ent.pos  = (r, c)
            tiles[r, c].addEnt(1, ent)
            s = torchlib.Stim(ent, tiles, self.config)
            conv, flat, ents = s.conv, s.flat, s.ents
            val  = self.valNet(conv, s.flat, s.ents)
            vals.append(float(val))
            tiles[r, c].delEnt(1)
            posList.append((r, c))
      vals = list(zip(posList, vals))
      return vals

   def visVals(self, food='max', water='max'):
      from forge.blade.core import realm
      posList, vals = [], []
      R, C = self.world.shape
      for r in range(self.config.BORDER, R-self.config.BORDER):
          for c in range(self.config.BORDER, C-self.config.BORDER):
            colorInd = int(12*np.random.rand())
            color    = Neon.color12()[colorInd]
            color    = (colorInd, color)
            ent = entity.Player(-1, color, self.config)
            ent._pos = (r, c)

            if food != 'max':
               ent._food = food
            if water != 'max':
               ent._water = water
            posList.append(ent.pos)

            self.world.env.tiles[r, c].addEnt(ent.entID, ent)
            stim = self.world.env.stim(ent.pos, self.config.STIM)
            s = torchlib.Stim(ent, stim, self.config)
            val = self.valNet(s.conv, s.flat, s.ents).detach()
            self.world.env.tiles[r, c].delEnt(ent.entID)
            vals.append(float(val))

      vals = list(zip(posList, vals))
      return vals
