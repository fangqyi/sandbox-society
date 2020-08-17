from pdb import set_trace as T
import numpy as np
import time

from collections import defaultdict

import projekt
from projekt.overlay import OverlayRegistry

from forge.blade.systems import ai
from forge.blade.core.env import Env
from forge.blade.io.action import static as Action

class Evaluator:
   '''Test-time evaluation with communication to
   the Unity3D client. Makes use of batched GPU inference'''
   def __init__(self, config, trainer=None, policy=None):
      assert (trainer is None) ^ (policy is None)
      self.trainer = trainer
      self.policy  = policy
      self.config  = config
      self.done    = {}
      self.infos   = {}

      #Logging
      self.lifetimes = []
 
      if trainer:
         self.model    = self.trainer.get_policy('policy_0').model
         self.env      = projekt.RLLibEnv({'config': config})
         self.obs      = self.env.reset(idx=0)

         self.registry = OverlayRegistry(self.env, self.model, trainer, config)
         self.state    = {}
      else:
         self.env      = Env(config)
         self.obs      = self.env.reset()
         self.registry = OverlayRegistry(self.env, None, None, config)

   def render(self):
      '''Rendering launches a Twisted WebSocket server with a fixed
      tick rate. This is a blocking call; the server will handle 
      environment execution using the provided tick function.'''
      from forge.trinity.twistedserver import Application
      Application(self.env, self.tick)

   def test(self):
      t = 0
      while True:
         self.tick(None, None)
         print('Tick: ', t)
         t += 1
         if len(self.lifetimes) > 10:
            break

      perf = np.mean(self.lifetimes)
      print('Performance: ', perf)

   def tick(self, pos, cmd):
      '''Compute actions and overlays for a single timestep
      Args:
          pos: Camera position (r, c) from the server)
          cmd: Console command from the server
      '''
      #Remove dead agents
      for agentID in self.done:
         if self.done[agentID]:
            del self.obs[agentID]
           
      #Compute batch of actions
      if self.trainer:
         actions, self.state, _ = self.trainer.compute_actions(
               self.obs, state=self.state, policy_id='policy_0')
         self.registry.step(self.obs, pos, cmd,
               update='counts values attention wilderness'.split())
      else:
         realm, actions = self.env.realm, {}
         for agentID in self.obs:
            agent              = realm.players[agentID]
            agent.skills.style = Action.Range
            actions[agentID]   = ai.policy.baseline(realm, agent)

         self.registry.step(self.obs, pos, cmd, update=
               'counts wilderness'.split())

      #Step the environment
      self.obs, rewards, self.done, self.infos = self.env.step(actions)

      #Log performance
      for entID, e in self.infos.items():
         self.lifetimes.append(e)
