from pdb import set_trace as T
import numpy as np

from collections import defaultdict

from forge.blade.io.stimulus import Static
from forge.blade.io.node import DataType

'''
Notes:
1. You need 3d tables for fast row/col range indexing
2. You need a matrix + 2d table representation for entities
3. You need to modify the update() functions to compute absolute
   offsets for discrete variables
4. You need to modify env.getStims and stimulus.Dynamic to accept the new data forms
5. You need to modify RLlib to accept the new data forms
6. You need to modify forge/ethyr/io to accept the new data forms
7. You need to modify the game rules to ensure 1 agent max per tile
'''

class Index:
   def __init__(self, prealloc):
      self.free  = {idx for idx in range(prealloc)}
      self.index = {}

   def full(self):
      return len(self.free) == 0

   def remove(self, key):
      row = self.index[key]
      self.free.add(row)
      return row

   def update(self, key):
      if key in self.index:
         row = self.index[key]
      else:
         row = self.free.pop()
         self.index[key] = row

      return row

   def get(self, key):
      return self.index[key]

   def expand(self, cur, nxt):
      self.free.update({idx for idx in range(cur, nxt)})

class Table:
   def __init__(self, config, obj, prealloc, dtype):
      self.dtype  = dtype
      self.nCols  = 0
      self.cols   = {}
      self.cumsum = 0
      self.discrete = {}
      for (attribute,), attr in obj:
         if dtype not in attr.DATA_TYPES:
            continue

         self.cols[attribute]     = self.nCols
         attr                     = attr(None, None, 0, config=config)
         self.cumsum              += attr.max - attr.min + 1
         self.discrete[attribute] = self.cumsum
         self.nCols += 1


      self.data = self.init(prealloc, self.nCols)

   def init(self, nRows, nCols):
      return np.zeros((nRows, nCols), dtype=self.dtype)

   def update(self, row, attr, val):
      col = self.cols[attr] 
      self.data[row, col] = val

   def expand(self, cur, nxt):
      data = self.init(nxt, self.nCols)

      data[:cur] = self.data

      self.nRows = nxt
      self.data  = data

   def get(self, rows, pad=None):
      data = self.data[rows]

      if pad is not None:
         data = np.pad(data, ((0, pad-len(data)), (0, 0)))

      return data

class Grid:
   def __init__(self, R, C):
      self.data = np.zeros((R, C), dtype=np.int)

   def zero(self, pos):
      r, c           = pos
      self.data[r, c] = 0
    
   def set(self, pos, val):
      r, c            = pos
      self.data[r, c] = val
 
   def move(self, pos, nxt, row):
      self.zero(pos)
      self.set(nxt, row)

   def window(self, rStart, rEnd, cStart, cEnd):
      crop = self.data[rStart:rEnd, cStart:cEnd].ravel()
      return list(filter(lambda x: x != 0, crop))
      
class GridTables:
   def __init__(self, config, obj, pad, prealloc=1000, expansion=2):
      self.grid       = Grid(config.TERRAIN_SIZE, config.TERRAIN_SIZE)
      self.continuous = Table(config, obj, prealloc, np.float32)
      self.discrete   = Table(config, obj, prealloc, np.int32)
      self.index      = Index(prealloc)

      self.nRows      = prealloc
      self.expansion  = expansion
      self.radius     = config.STIM
      self.pad        = pad

   def get(self, pos):
      r, c = pos
      rows = self.grid.window(
            r-self.radius, r+self.radius+1,
            c-self.radius, c+self.radius+1)

      return {'Continuous': self.continuous.get(rows, self.pad),
              'Discrete':   self.discrete.get(rows, self.pad)}

   def update(self, obj, val):
      key, attr = obj.key, obj.attr
      if self.index.full():
         cur        = self.nRows
         self.nRows = cur * self.expansion

         self.index.expand(cur, self.nRows)
         self.continuous.expand(cur, self.nRows)
         self.discrete.expand(cur, self.nRows)

      row = self.index.update(key)
      if DataType.DISCRETE in obj.DATA_TYPES:
         self.discrete.update(row, attr, val)
      if DataType.CONTINUOUS in obj.DATA_TYPES:
         self.continuous.update(row, attr, val)

   def move(self, key, pos, nxt):
      row = self.index.get(key)
      self.grid.move(pos, nxt, row)

   def init(self, key, pos):
      row = self.index.get(key)
      self.grid.set(pos, row)

   def remove(self, key, pos):
      self.index.remove(key)
      self.grid.zero(pos)

class Dataframe:
   def __init__(self, config):
      self.config, self.data = config, defaultdict(dict)
      for (objKey,), obj in Static:
         self.data[objKey] = GridTables(config, obj, pad=obj.N(config))

   def update(self, node, val):
      self.data[node.obj].update(node, val)

   def remove(self, obj, key, pos):
      self.data[obj.__name__].remove(key, pos)

   def init(self, obj, key, pos):
      self.data[obj.__name__].init(key, pos)

   def move(self, obj, key, pos, nxt):
      self.data[obj.__name__].move(key, pos, nxt)

   def get(self, pos):
      stim = {}
      for key, grid2Table in self.data.items():
         stim[key] = grid2Table.get(pos)

      return stim



