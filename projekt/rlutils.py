from pdb import set_trace as T
import numpy as np

import ray.rllib.agents.ppo.ppo as ppo
from ray.rllib.policy.sample_batch import DEFAULT_POLICY_ID

class SanePPOTrainer(ppo.PPOTrainer):
   def __init__(self, env, path, config):
      super().__init__(env=env, config=config)
      self.saveDir = path

   def save(self):
      savedir = super().save(self.saveDir)
      with open('experiment/path.txt', 'w') as f:
         f.write(savedir)
      print('Saved to: {}'.format(savedir))
      return savedir

   def restore(self):
      with open('experiment/path.txt') as f:
         path = f.read()
      print('Loading from: {}'.format(path))
      super().restore(path)

   def policyID(self, idx):
      return 'policy_{}'.format(idx)

   def model(self, policyID):
      return self.get_policy(policyID).model

   def defaultModel(self):
      return self.model(self.policyID(0))

   def train(self):
      epoch = 0
      while True:
          stats = super().train()
          self.save()

          nSteps = stats['info']['num_steps_trained']
          print('Epoch: {}, Samples: {}'.format(epoch, nSteps))
          epoch += 1


   #In rllib.utils.space_utils in next patch
   def unbatch(batches_struct):
       """Converts input from (nested) struct of batches to batch of structs.

       Input: Struct of different batches (each batch has size=3):
           {"a": [1, 2, 3], "b": ([4, 5, 6], [7.0, 8.0, 9.0])}
       Output: Batch (list) of structs (each of these structs representing a
           single action):
           [
               {"a": 1, "b": (4, 7.0)},  <- action 1
               {"a": 2, "b": (5, 8.0)},  <- action 2
               {"a": 3, "b": (6, 9.0)},  <- action 3
           ]

       Args:
           batches_struct (any): The struct of component batches. Each leaf item
               in this struct represents the batch for a single component
               (in case struct is tuple/dict).
               Alternatively, `batches_struct` may also simply be a batch of
               primitives (non tuple/dict).

       Returns:
           List[struct[components]]: The list of rows. Each item
               in the returned list represents a single (maybe complex) struct.
       """
       flat_batches = tree.flatten(batches_struct)

       out = []
       for batch_pos in range(len(flat_batches[0])):
           out.append(
               tree.unflatten_as(
                   batches_struct,
                   [flat_batches[i][batch_pos]
                    for i in range(len(flat_batches))]))
       return out

   #To be integrated into RLlib and thus formatted using
   #their project's conventions
   def compute_actions(self,
                       observations,
                       state=None,
                       prev_action=None,
                       prev_reward=None,
                       info=None,
                       policy_id=DEFAULT_POLICY_ID,
                       full_fetch=False,
                       explore=None):
        """Computes an action for the specified policy on the local Worker.

        Note that you can also access the policy object through
        self.get_policy(policy_id) and call compute_actions() on it directly.

        Arguments:
            observation (obj): observation from the environment.
            state (dict): RNN hidden state, if any. If state is not None,
                then all of compute_single_action(...) is returned
                (computed action, rnn state(s), logits dictionary).
                Otherwise compute_single_action(...)[0] is returned
                (computed action).
            prev_action (obj): previous action value, if any
            prev_reward (int): previous reward, if any
            info (dict): info object, if any
            policy_id (str): Policy to query (only applies to multi-agent).
            full_fetch (bool): Whether to return extra action fetch results.
                This is always set to True if RNN state is specified.
            explore (bool): Whether to pick an exploitation or exploration
                action (default: None -> use self.config["explore"]).

        Returns:
            any: The computed action if full_fetch=False, or
            tuple: The full output of policy.compute_actions() if
                full_fetch=True or we have an RNN-based Policy.
        """
        #Preprocess obs and states
        stateDefined = state is not None
        policy = self.get_policy(policy_id)
        filtered_obs, filtered_state = [], []
        for agent_id, ob in observations.items():
            worker       = self.workers.local_worker()
            preprocessed = worker.preprocessors[
                    policy_id].transform(ob)
            filtered     = worker.filters[policy_id](
                    preprocessed, update=False)
            filtered_obs.append(filtered)
            if state is None:
               continue
            elif agent_id in state:
               filtered_state.append(state[agent_id])
            else:
               filtered_state.append(policy.get_initial_state())

        #Batch obs and states
        obs_batch = np.stack(filtered_obs)
        if state is None:
            state = []
        else:
            state = list(zip(*filtered_state))
            state = [np.stack(s) for s in state]

        # Figure out the current (sample) time step and pass it into Policy.
        self.global_vars["timestep"] += 1

        #Batch compute actions
        actions, states, infos = policy.compute_actions(
            obs_batch,
            state,
            prev_action,
            prev_reward,
            info,
            clip_actions=self.config["clip_actions"],
            explore=explore,
            timestep=self.global_vars["timestep"])

        #Unbatch actions for the environment
        atns, actions = unbatch(actions), {}
        for key, atn in zip(observations, atns):
           actions[key] = atn    

        #Unbatch states into a dict
        unbatched_states = {}
        for idx, agent_id in enumerate(observations):
            unbatched_states[agent_id] = [s[idx] for s in states]

        #Return only actions or full tuple
        if stateDefined or full_fetch:
            return actions, unbatched_states, infos
        else:
            return actions

from ray.rllib.utils import try_import_tree
tree = try_import_tree()
#In rllib.utils.space_utils in next patch
def unbatch(batches_struct):
    """Converts input from (nested) struct of batches to batch of structs.

    Input: Struct of different batches (each batch has size=3):
        {"a": [1, 2, 3], "b": ([4, 5, 6], [7.0, 8.0, 9.0])}
    Output: Batch (list) of structs (each of these structs representing a
        single action):
        [
            {"a": 1, "b": (4, 7.0)},  <- action 1
            {"a": 2, "b": (5, 8.0)},  <- action 2
            {"a": 3, "b": (6, 9.0)},  <- action 3
        ]

    Args:
        batches_struct (any): The struct of component batches. Each leaf item
            in this struct represents the batch for a single component
            (in case struct is tuple/dict).
            Alternatively, `batches_struct` may also simply be a batch of
            primitives (non tuple/dict).

    Returns:
        List[struct[components]]: The list of rows. Each item
            in the returned list represents a single (maybe complex) struct.
    """
    flat_batches = tree.flatten(batches_struct)

    out = []
    for batch_pos in range(len(flat_batches[0])):
        out.append(
            tree.unflatten_as(
                batches_struct,
                [flat_batches[i][batch_pos]
                 for i in range(len(flat_batches))]))
    return out

