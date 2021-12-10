# Maintenance Documentation

## Installation
Sandbox Society inherits the infrastructure from NeuralMMO, it also officially supports Ubuntu 20.04, Windows 10 + WSL, and MacOS (with screen death problems in Windows 11). The only difference in infrastructure is that our unity client and backend are in the same repository, which  eliminates the original step of moving the client implementation to ``neural-mmo/forge/embyr`` during setup.
For a quickstart,
```
conda create --name neural_mmo_env
conda activate neural_mmo_env
git clone https://coursework.cs.duke.edu/compsci390_2021fall/project_Playground.git
cd neural-mmo && bash scripts/setup.sh # --CORE_ONLY to omit RLlib requirements
```
Then, follow these additional required steps:  
- Edit projekt/config.py as per the instructions therein to match your hardware specs
- Create a file wandb_api_key in the repo root and paste in your WanDB API key. This new integration is now so important to logging and evaluation that we are requiring it by default. Do not commit this file.

For more technical details and troubleshooting questions, please read the [installation documentation](https://jsuarez5341.github.io/neural-mmo/build/html/rst/userguide.html#installation) of NeuralMMO.

## Running
To run the simulation, first generate maps:

```
python3 Forge.py generate --config=Social
```

Then run the Unity client. For Windows, this will mean running `neural_mmo/forge/embyr/UnityClient/sandbox_society.exe`. **The current frontend is not yet built for Mac/Linux.** As a workaround, the project can be opened in the Unity Editor and run there, on all systems.

Then render the backend:

```
python3 Forge.py render --config=Social
```

## Configurations
  address ways to update or change key non-programming components of the app, such as database information, data files, resource links, phone numbers, server addresses, etc.

Many of the configurable parameters can be set in `projekt/config.py`. Simply create a new class sublcassing from `core.Config` or one of the existing config classes, and set the desired parameters appropriately. This config can then be called from the command line in the generate and render commands above, as `--config=[new_config_name]`. A comprensive list of parameters can be found in `neural_mmo/forge/blade/core/config.py`.

To run with a different scripted agent, change the AGENT and EVAL_AGENTS lists to be lists of the classes of the desired scripted agents. These scripted agents can be found in `neural_mmo/forge/trinity/scripted` as subclasses of the `baselines.Scripted` class. To make a new type of agent, create a new subclass of Scripted, and define the desired behavior in the `__call__` method.

## Libraries and Tools 
```
ray==1.5.2  ### Apache License 2.0
cloudpickle==1.2.2   ### non-standard license https://github.com/cloudpipe/cloudpickle/blob/master/LICENSE
setproctitle==1.1.10  ### BSD License
redis==3.5.3   ### MIT License
dm-tree==0.1.5   ### Apache License 2.0
tensorflow==2.4.1  ### Apache License 2.0
aioredis==1.3.1   ### MIT License
fire==0.4.0   ### Apache License 2.0
autobahn==19.3.3   ### MIT License
Twisted==19.2.0   ### non-standard license https://github.com/twisted/twisted/blob/trunk/LICENSE
gym==0.17.2   ### MIT License
vec-noise==1.1.4   ### MIT License
bokeh==2.2.3   ### BSD 3-Clause "New" or "Revised" License
imageio==2.8.0  ### BSD 2-Clause "Simplified" License
sphinx-rtd-theme==0.5.1  ### MIT License
tqdm==4.61.1  ### MIT License
matplotlib==3.1.3  ### BSD License
numpy==1.21.1   ### BSD license
trueskill==0.4.5   ### BSD License
wandb==0.10.32   ### MIT License
neural-mmo==1.5.2  ### MIT License
```


