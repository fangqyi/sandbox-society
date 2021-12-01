from pdb import set_trace as T
import numpy as np
from itertools import chain

from neural_mmo.forge.blade import core
from neural_mmo.forge.blade.lib import material

from random import randint

import os

numsent = 0

class Map:
   '''Map object representing a list of tiles
   
   Also tracks a sparse list of tile updates
   '''
   def __init__(self, config, realm):
      self.config = config

      sz          = config.TERRAIN_SIZE
      self.tiles  = np.zeros((sz, sz), dtype=object)

      for r in range(sz):
         for c in range(sz):
            self.tiles[r, c] = core.Tile(config, realm, r, c)

   @property
   def packet(self):
       '''Packet of degenerate resource states'''
       missingResources = []
       for e in self.updateList:
           missingResources.append((e.r.val, e.c.val, e.index.val))
       return missingResources

   @property
   def repr(self):
      '''Flat matrix of tile material indices'''
      return [[t.mat.index for t in row] for row in self.tiles]

   @property
   def items(self):
      global numsent
      numsent += 1
      item_types = self.tiles[0,0].items_dict.keys()
      ret = {itm:[] for itm in item_types}
      if numsent < 100:
         for itm in item_types:
            temp = []
            for row in self.tiles:
               for t in row:
                  if t.mat == material.Grass and t.dirty:
                     temp.append((t.r.val, t.c.val, t.items_dict[itm].val))
            ret[itm] = [i for i in temp]

      # ret = {itm:[(t.r.val, t.c.val, t.items_dict[itm].val+2) for t in chain(*self.tiles) if t.mat.index == material.Grass] for itm in item_types}
      # for t in chain(*self.tiles):
      #    t.dirty = False
      return ret
   
   def reset(self, realm, idx):
      '''Reuse the current tile objects to load a new map'''
      self.updateList = set()

      materials = {mat.index: mat for mat in material.All}
      fPath  = os.path.join(self.config.PATH_MAPS,
            self.config.PATH_MAP_SUFFIX.format(idx))
      for r, row in enumerate(np.load(fPath)):
         for c, idx in enumerate(row):
            mat  = materials[idx]
            tile = self.tiles[r, c]
            tile.reset(mat, self.config)


   def step(self):
      '''Evaluate updatable tiles'''
      for e in self.updateList.copy():
         if e.static:
            self.updateList.remove(e)
         e.step()
      # for t in chain(*self.tiles):
      #    t.dirty = False

   def harvest(self, r, c):
      '''Called by actions that harvest a resource tile'''
      self.updateList.add(self.tiles[r, c])
      return self.tiles[r, c].harvest()
