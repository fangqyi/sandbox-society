from pdb import set_trace as T
import numpy as np

from neural_mmo.forge.blade.item.item import Item, ItemType
from neural_mmo.forge.blade.lib import material
from neural_mmo.forge.blade.io.stimulus import Static

from random import randint

class Tile:
   def __init__(self, config, realm, r, c):
      self.config = config
      self.realm  = realm

      self.serialized = 'R{}-C{}'.format(r, c)

      self.dirty = True

      self.r     = Static.Tile.R(realm.dataframe, self.serial, r)
      self.c     = Static.Tile.C(realm.dataframe, self.serial, c)
      self.nEnts = Static.Tile.NEnts(realm.dataframe, self.serial)
      self.index = Static.Tile.Index(realm.dataframe, self.serial, 0)
      self.ssticks = Static.Tile.SStick(realm.dataframe, self.serial, 0)
      self.lsticks = Static.Tile.LStick(realm.dataframe, self.serial, 0)
      self.sstones = Static.Tile.SStone(realm.dataframe, self.serial, 0)
      self.lstones = Static.Tile.LStone(realm.dataframe, self.serial, 0)
      self.items_dict = {ItemType.SMALL_STICK: self.ssticks,
                         ItemType.LARGE_BRANCH: self.lsticks,
                         ItemType.SMALL_ROCK: self.sstones,
                         ItemType.LARGE_BOULDER: self.lstones,
                        }

      realm.dataframe.init(Static.Tile, self.serial, (r, c))

   @property
   def serial(self):
      return self.serialized

   @property
   def repr(self):
      return ((self.r, self.c))

   @property
   def pos(self):
      return self.r.val, self.c.val

   @property
   def habitable(self):
      return self.mat in material.Habitable

   @property
   def vacant(self):
      return len(self.ents) == 0 and self.habitable

   @property
   def occupied(self):
      return not self.vacant

   @property
   def impassible(self):
      return self.mat in material.Impassible

   @property
   def lava(self):
      return self.mat == material.Lava

   @property
   def items(self):
      return self.ssticks.val, self.lsticks.val, self.sstones.val, self.lstones.val

   @property
   def static(self):
      '''No updates needed'''
      assert self.capacity <= self.mat.capacity
      return self.capacity == self.mat.capacity

   def reset(self, mat, config):
      self.state  = mat(config)
      self.mat    = mat(config)

      self.capacity = self.mat.capacity
      self.tex      = mat.tex
      self.ents     = {}
      self.dirty = True

      self.nEnts.update(0)
      self.index.update(self.state.index)

      # for i in range(randint(0,4)):
      #    self.addItem(ItemType.SMALL_STICK)
      # for i in range(randint(0,4)):
      #    self.addItem(ItemType.SMALL_ROCK)
 
   def addEnt(self, ent):
      assert ent.entID not in self.ents
      self.nEnts.update(1)
      self.ents[ent.entID] = ent

   def delEnt(self, entID):
      assert entID in self.ents
      self.nEnts.update(0)
      del self.ents[entID]

   def addItem(self, itm):
      assert itm in self.items_dict
      self.items_dict[itm].increment()
      self.dirty = True

   def removeItem(self, itm):
      assert itm in self.items_dict
      self.items_dict[itm].decrement()
      self.dirty = True

   def step(self):
      if (not self.static and 
            np.random.rand() < self.mat.respawn):
         self.capacity += 1

      if self.static:
         self.state = self.mat
         self.index.update(self.state.index)

   def harvest(self):
      if self.capacity == 0:
         return False
      elif self.capacity <= 1:
         self.state = self.mat.degen(self.config)
         self.index.update(self.state.index)
      self.capacity -= 1
      return True
      return self.mat.dropTable.roll()
