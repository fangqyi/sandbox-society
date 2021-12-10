from pdb import set_trace as T
import numpy as np

from neural_mmo.forge.blade.item.item import Item, ItemType
from neural_mmo.forge.blade.lib import utils, material
from neural_mmo.forge.blade.lib.utils import staticproperty
from neural_mmo.forge.blade.io.node import Node, NodeType
from neural_mmo.forge.blade.systems import combat
from neural_mmo.forge.blade.io.stimulus import Static

class Fixed:
   pass

#ActionRoot
class Action(Node):
   nodeType = NodeType.SELECTION

   @staticproperty
   def edges():
      return [Move, Attack]

   @staticproperty
   def n():
      return len(Action.arguments)

   def args(stim, entity, config):
      return Static.edges 

   #Called upon module import (see bottom of file)
   #Sets up serialization domain
   def hook():
      idx = 0
      arguments = []
      for action in Action.edges:
         for args in action.edges:
            if not 'edges' in args.__dict__:
               continue
            for arg in args.edges: 
               arguments.append(arg)
               arg.serial = tuple([idx])
               arg.idx = idx 
               idx += 1
      Action.arguments = arguments

class Move(Node):
   priority = 1
   nodeType = NodeType.SELECTION
   def call(env, entity, direction):
      r, c  = entity.pos
      entID = entity.entID
      entity.history.lastPos = (r, c)
      rDelta, cDelta = direction.delta
      rNew, cNew = r+rDelta, c+cDelta
      
      #One agent per cell
      tile = env.map.tiles[rNew, cNew] 
      if tile.occupied and not tile.lava:
         return

      if entity.status.freeze > 0:
         return

      env.dataframe.move(Static.Entity, entID, (r, c), (rNew, cNew))
      entity.base.r.update(rNew)
      entity.base.c.update(cNew)

      env.map.tiles[r, c].delEnt(entID)
      env.map.tiles[rNew, cNew].addEnt(entity)

      if env.map.tiles[rNew, cNew].lava:
         entity.receiveDamage(None, entity.resources.health.val)

   @staticproperty
   def edges():
      return [Direction]

   @staticproperty
   def leaf():
      return True

class Direction(Node):
   argType = Fixed

   @staticproperty
   def edges():
      return [North, South, East, West]

   def args(stim, entity, config):
      return Direction.edges

class North(Node):
   delta = (-1, 0)

class South(Node):
   delta = (1, 0)

class East(Node):
   delta = (0, 1)

class West(Node):
   delta = (0, -1)


class Attack(Node):
   priority = 0
   nodeType = NodeType.SELECTION
   @staticproperty
   def n():
      return 3

   @staticproperty
   def edges():
      return [Style, Target]

   @staticproperty
   def leaf():
      return True

   def inRange(entity, stim, config, N):
      R, C = stim.shape
      R, C = R//2, C//2

      rets = set([entity])
      for r in range(R-N, R+N+1):
         for c in range(C-N, C+N+1):
            for e in stim[r, c].ents.values():
               rets.add(e)

      rets = list(rets)
      return rets

   def l1(pos, cent):
      r, c = pos
      rCent, cCent = cent
      return abs(r - rCent) + abs(c - cCent)

   def call(env, entity, style, targ):
      if entity.isPlayer and not env.config.game_system_enabled('Combat'):
         return 

      #Check if self targeted
      if entity.entID == targ.entID:
         return

      #ADDED: POPULATION IMMUNITY
      #if entity.population == targ.population:
      #   return

      #Check attack range
      rng     = style.attackRange(env.config)
      start   = np.array(entity.base.pos)
      end     = np.array(targ.base.pos)
      dif     = np.max(np.abs(start - end))

      #Can't attack same cell or out of range
      if dif == 0 or dif > rng:
         return 
      
      #Execute attack
      entity.history.attack = {}
      entity.history.attack['target'] = targ.entID
      entity.history.attack['style'] = style.__name__
      targ.attacker = entity
      targ.attackerID.update(entity.entID)

      dmg = combat.attack(entity, targ, style.skill)
      if style.freeze and dmg > 0:
         targ.status.freeze.update(env.config.COMBAT_FREEZE_TIME)

      return dmg

class Style(Node):
   argType = Fixed
   @staticproperty
   def edges():
      return [Melee, Range, Mage]

   def args(stim, entity, config):
      return Style.edges


class Target(Node):
   argType = None
   #argType = Player 

   @classmethod
   def N(cls, config):
      #return config.WINDOW ** 2
      return config.N_AGENT_OBS

   def args(stim, entity, config):
      #Should pass max range?
      return Attack.inRange(entity, stim, config, None)

class Melee(Node):
   nodeType = NodeType.ACTION
   index = 0
   freeze=False

   def attackRange(config):
      return config.COMBAT_MELEE_REACH

   def skill(entity):
      return entity.skills.melee

class Range(Node):
   nodeType = NodeType.ACTION
   index = 1
   freeze=False

   def attackRange(config):
      return config.COMBAT_RANGE_REACH

   def skill(entity):
      return entity.skills.range

class Mage(Node):
   nodeType = NodeType.ACTION
   index = 2
   freeze=True

   def attackRange(config):
      return config.COMBAT_MAGE_REACH

   def skill(entity):
      return entity.skills.mage

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
Signal is a node that allows entities to set their communication light.
'''
class Signal(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity, light):
      entity.setLight(light)
      entity.history.communication.update(entity.getLightNumeric())

      return light

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
Light is a node that defines the types of lights entities can use.
'''
class Light(Node):
   argType = Fixed

   @staticproperty
   def edges():
      return ["OFF", "PURPLE", "YELLOW", "BLUE"]

   def args(stim, entity, config):
      return Direction.edges

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
TechnologyStatus is a node that allows entities to obtain their technology status for rocks and sticks.
'''
class TechnologyStatus(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity):
      sword_status = entity.getSwordStatus()
      shield_status = entity.getShieldStatus()
      hoe_status = entity.getHoeStatus()
      improved_hoe_status = entity.getImprovedHoeStatus()
      entity.history.sword_status.update(1 if sword_status else 0)
      entity.history.shield_status.update(1 if shield_status else 0)
      entity.history.hoe_status.update(1 if hoe_status else 0)
      entity.history.improved_hoe_status.update(1 if improved_hoe_status else 0)
      return sword_status, shield_status, hoe_status, improved_hoe_status

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
InventoryInsertion is a node that allows entities to insert items into their inventory.
'''
class InventoryInsertion(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity, items):
      entity.inv.insertItems(items)
      for item in items:
         if item.getType() == ItemType.SMALL_ROCK:
            entity.history.small_rocks.increment()
         if item.getType() == ItemType.SMALL_STICK:
            entity.history.small_sticks.increment()
         if item.getType() == ItemType.LARGE_BOULDER:
            entity.history.large_boulders.increment()
         if item.getType() == ItemType.LARGE_BRANCH:
            entity.history.large_branches.increment()
      return True

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
InventoryRemoval is a node that allows entities to remove items from their inventory.
'''
class InventoryRemoval(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity, itemType, numItems):
      entity.inv.removeItems(itemType, numItems)
      if itemType == ItemType.SMALL_ROCK:
         entity.history.small_rocks.decrement(numItems)
      if itemType == ItemType.SMALL_STICK:
         entity.history.small_sticks.decrement(numItems)
      if itemType == ItemType.LARGE_BOULDER:
         entity.history.large_boulders.decrement(numItems)
      if itemType == ItemType.LARGE_BRANCH:
         entity.history.large_branches.decrement(numItems)

      return True

'''
Duke CS390 Fall 2021: AI Sandbox, Lorne Zhang
InventoryItemType is a node that defines the possible types for inventory items.
'''
class InventoryItemType(Node):
   argType = Fixed

   @staticproperty
   def edges():
      return [ItemType.SMALL_STICK, ItemType.SMALL_ROCK, ItemType.LARGE_BOULDER, ItemType.LARGE_BRANCH]

   def args(stim, entity, config):
      return Direction.edges

'''
Duke CS390 Fall 2021: AI Sandbox
Gather is a node that allows entities to gather resources that naturally spawn from their current tile.
'''
class Gather(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity, delta):
      r, c  = entity.pos
      entID = entity.entID
      rDelta, cDelta = delta
      rNew, cNew = r+rDelta, c+cDelta

      tile = env.map.tiles[rNew, cNew]
      if env.map.harvest(rNew, cNew):
         if type(tile.mat) == material.Orerock:
            entity.inv.insertItems([ItemType.SMALL_ROCK])
            entity.history.small_rocks.increment()
         elif type(tile.mat) == material.Forest:
            entity.resources.food.update(entity.resources.food.max)
            entity.inv.insertItems([ItemType.SMALL_STICK])
            entity.history.small_sticks.increment()

'''
Duke CS390 Fall 2021: AI Sandbox
PickUpItem is a node that allows entities to pick up items from their current tile. This includes items that have been dropped.
'''
class PickUpItem(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity):
      r, c  = entity.pos

      tile = env.map.tiles[r, c]
      ssticks, lsticks, sstones, lstones = tile.items

      for i in range(ssticks):
         tile.removeItem(ItemType.SMALL_STICK)
         entity.insertItemsIntoInventory([Item(ItemType.SMALL_STICK)])
         entity.history.small_sticks.increment()

      for i in range(sstones):
         tile.removeItem(ItemType.SMALL_ROCK)
         entity.insertItemsIntoInventory([Item(ItemType.SMALL_ROCK)])
         entity.history.small_rocks.increment()

      shield_status = entity.getShieldStatus()
      hoe_status = entity.getHoeStatus()
      if hoe_status:
         for i in range(lsticks):
            tile.removeItem(ItemType.LARGE_BRANCH)
            entity.insertItemsIntoInventory([Item(ItemType.LARGE_BRANCH)])
            entity.history.large_branches.increment()

      if shield_status:
         for i in range(lstones):
            tile.removeItem(ItemType.LARGE_BOULDER)
            entity.insertItemsIntoInventory([Item(ItemType.LARGE_BOULDER)])
            entity.history.large_boulders.increment()

'''
Duke CS390 Fall 2021: AI Sandbox
DropItem is a node that allows entities to drop inventory items onto their current tile.
'''
class DropItem(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity):
      r, c  = entity.pos

      tile = env.map.tiles[r, c]
      tile.addItem(ItemType.SMALL_STICK)
      ## entity.inv.removeItems(itemType, 1)

'''
Duke CS390 Fall 2021: AI Sandbox
InventoryItem is a node that represents the different types of inventory items an entity can have.
'''
class InventoryItem(Node):
   argType = Fixed

   @staticproperty
   def edges():
      return [Item(ItemType.SMALL_STICK), Item(ItemType.SMALL_ROCK), Item(ItemType.LARGE_BOULDER), Item(ItemType.LARGE_BRANCH)]

   def args(stim, entity, config):
      return Direction.edges


#TODO: Add communication
class Message:
   pass

#TODO: Add trade
class Exchange:
   pass

#TODO: Solve AGI
class BecomeSkynet:
   pass

Action.hook()

class GiveItems(Node):
   priority = 0
   nodeType = NodeType.SELECTION

   @staticproperty
   def n():
      return 0

   @staticproperty
   def edges(self):
      return []

   @staticproperty
   def leaf(self):
      return True

   def call(env, entity, args):
      target, itemType, numItems = args
      numItems = int(numItems)
      entity.inv.removeItems(itemType, numItems)
      entity.inv.insertItems([ItemType]*numItems)
      if itemType == ItemType.SMALL_ROCK:
         entity.history.small_rocks.increment(numItems)
      if itemType == ItemType.SMALL_STICK:
         entity.history.small_sticks.increment(numItems)
      if itemType == ItemType.LARGE_BOULDER:
         entity.history.large_boulders.increment(numItems)
      if itemType == ItemType.LARGE_BRANCH:
         entity.history.large_branches.increment(numItems)
      return True