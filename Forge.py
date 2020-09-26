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
from ray import rllib

from forge.ethyr.torch import utils
from forge.blade.systems import ai

import projekt
from projekt import env, rlutils
from projekt.visualize import visualize
from forge.blade.core import terrain

#Instantiate a new environment
def createEnv(config):
   return projekt.RLLibEnv(config)

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
   ray.init()

   #Instantiate monolithic RLlib Trainer object.
   rllib.models.ModelCatalog.register_custom_model(
         'test_model', projekt.Policy)
   ray.tune.registry.register_env("custom", createEnv)
   policies  = createPolicies(config)
   return rlutils.SanePPOTrainer(
         env="custom", path='experiment', config={
      'num_workers': 2,
      'num_gpus': 1,
      'num_envs_per_worker': 1,
      'train_batch_size': 2000,
      'rollout_fragment_length': 100,
      'sgd_minibatch_size': 128,
      'num_sgd_iter': 1,
      'use_pytorch': True,
      'horizon': np.inf,
      'soft_horizon': False, 
      'no_done_at_end': False,
      'env_config': {
         'config': config
      },
      'multiagent': {
         "policies": policies,
         "policy_mapping_fn": mapPolicy
      },
      'model': {
         'custom_model': 'test_model',
         'custom_options': {'config': config}
      },
   })

def init(config, **kwargs):
   config.override(**kwargs)
   trainer, policy = None, None
   if config.SCRIPTED:
      policy = ai.policy.hostile
   else:
      trainer = loadTrainer(config)
      utils.modelSize(trainer.defaultModel())
      trainer.restore(config.MODEL)

   return trainer, policy

def evaluator(config, **kwargs):
   trainer, policy = init(config, **kwargs)
   return projekt.Evaluator(config,
         trainer=trainer, policy=policy)

class Config(projekt.Config):
   '''Docstring'''
   def train(self, **kwargs):
      trainer, policy = init(self, **kwargs)
      trainer.train()

   def evaluate(self, **kwargs):
      self.RENDER = True
      evaluator(self, **kwargs).test()

   def render(self, **kwargs):
      self.RENDER = True
      evaluator(self, **kwargs).render()

   def generate(self, **kwargs):
      trainer, policy = init(self, **kwargs)
      terrain.MapGenerator(config).generate()

   def visualize(self, **kwargs):
      self.override(**kwargs)
      visualize(self)
      
if __name__ == '__main__':
   #Built config with CLI overrides
   config = Config()
   Fire(config)
