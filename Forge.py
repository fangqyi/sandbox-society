'''Main file for the neural-mmo/projekt demo

/projeckt will give you a basic sense of the training
loop, infrastructure, and IO modules for handling input 
and output spaces. From there, you can either use the 
prebuilt IO networks in PyTorch to start training your 
own models immediately or hack on the environment'''

#My favorite debugging macro
from pdb import set_trace as T

from fire import Fire
import sys
import time

import numpy as np
import torch

import ray
from typing import Dict
from ray import rllib
from ray.rllib.env import BaseEnv
from ray.rllib.policy import Policy
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.evaluation import MultiAgentEpisode, RolloutWorker
from ray.rllib.agents.callbacks import DefaultCallbacks

from forge.ethyr.torch import utils
from forge.blade.systems import ai

import projekt
from projekt import env, rlutils
from projekt.visualize import visualize
from forge.blade.core import terrain

class LogCallbacks(DefaultCallbacks):
   STEP_KEYS    = 'rllib_compat env_step realm_step env_stim stim_process'.split()
   EPISODE_KEYS = ['env_reset']
   
   def init(self, episode):
      for key in LogCallbacks.STEP_KEYS + LogCallbacks.EPISODE_KEYS: 
         episode.hist_data[key] = []

   def on_episode_start(self, *, worker: RolloutWorker, base_env: BaseEnv,
         policies: Dict[str, Policy],
         episode: MultiAgentEpisode, **kwargs):
      self.init(episode)

   def on_episode_step(self, *, worker: RolloutWorker, base_env: BaseEnv,
         episode: MultiAgentEpisode, **kwargs):

      env = base_env.envs[0]
      for key in LogCallbacks.STEP_KEYS:
         if not hasattr(env, key):
            continue
         episode.hist_data[key].append(getattr(env, key))

   def on_episode_end(self, *, worker: RolloutWorker, base_env: BaseEnv,
         policies: Dict[str, Policy], episode: MultiAgentEpisode, **kwargs):
      env = base_env.envs[0]
      for key in LogCallbacks.EPISODE_KEYS:
         if not hasattr(env, key):
            continue
         episode.hist_data[key].append(getattr(env, key))

#Map agentID to policyID -- requires config global
def mapPolicy(agentID):
   return 'policy_{}'.format(agentID % config.NPOLICIES)

#Generate RLlib policies
def createPolicies(config):
   obs      = projekt.env.observationSpace(config)
   atns     = projekt.env.actionSpace(config)
   policies = {}

   for i in range(config.NPOLICIES):
      params = {
            "agent_id": i,
            "obs_space_dict": obs,
            "act_space_dict": atns}
      key           = mapPolicy(i)
      policies[key] = (None, obs, atns, params)

   return policies

def loadTrainer(config):
   #Setup ray
   torch.set_num_threads(1)
   #ray.init(local_mode=True)
   ray.init()

   #Instantiate monolithic RLlib Trainer object.
   rllib.models.ModelCatalog.register_custom_model(
         'test_model', projekt.Policy)

   policies  = createPolicies(config)
   ray.tune.registry.register_env("custom",
         lambda config: projekt.RLLibEnv(config))

   return rlutils.SanePPOTrainer(
         env="custom", path='experiment', config={
      'num_workers': 4,
      'num_gpus_per_worker': 0,
      'num_gpus': 1,
      'num_envs_per_worker': 1,
      'train_batch_size': 4000,
      'rollout_fragment_length': 100,
      'sgd_minibatch_size': 128,
      'num_sgd_iter': 1,
      'framework': 'torch',
      'horizon': np.inf,
      'soft_horizon': False, 
      '_use_trajectory_view_api': False,
      'no_done_at_end': False,
      'callbacks': LogCallbacks,
      'env_config': {
         'config': config
      },
      'multiagent': {
         "policies": policies,
         "policy_mapping_fn": mapPolicy
      },
      'model': {
         'custom_model': 'test_model',
         'custom_model_config': {'config': config}
      },
   })

def loadModel(config):
   trainer = None
   policy  = None

   if config.SCRIPTED_DP:
      policy = ai.policy.baselineDP
   elif config.SCRIPTED_BFS:
      policy = ai.policy.baselineBFS
   else:
      trainer = loadTrainer(config)

   utils.modelSize(trainer.defaultModel())
   trainer.restore(config.MODEL)

   evaluator = projekt.Evaluator(config,
      trainer=trainer, policy=policy)

   return trainer, policy, evaluator

class Anvil():
   '''Docstring'''
   def __init__(self, **kwargs):
      #TODO: obliterate this
      global config

      if 'config' in kwargs:
         config = kwargs.pop('config')
         config = getattr(projekt.config, config)()
      else:
         config = projekt.config.SmallMap()
      config.override(**kwargs)
      self.config = config

   def train(self, **kwargs):
      trainer, _, _ = loadModel(self.config)
      trainer.train()

   def evaluate(self, **kwargs):
      self.config.EVALUATE = True
      _, _, evaluator      = loadModel(self.config)
      evaluator.test()

   def render(self, **kwargs):
      self.config.EVALUATE = True
      _, _, evaluator      = loadModel(self.config)
      evaluator.render()

   def generate(self, **kwargs):
      terrain.MapGenerator(self.config).generate()

   def visualize(self, **kwargs):
      visualize(self.config)
      
if __name__ == '__main__':
   #Build config with CLI overrides
   Fire(Anvil)
