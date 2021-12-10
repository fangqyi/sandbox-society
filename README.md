# Sandbox Society 🤖⛏️🍎

Sandbox Society is an open-source MARL research environment that encourages learning agents to adopt societal formation as collective strategy to master the environment. It is a major extension to [Neural MMO](https://github.com/jsuarez5341/neural-mmo) which provides simulation of massive agents in procedurally generated virtual worlds, where agents forage for food, compete over resources, and struggle to survive. Sandbox Society builds on the current Neural MMO with features that incentivize the emergence of _complex social structures_. The added features include:
-   communication light protocol
-   productive resources (e.g. stick, stone)
-  resource factories (e.g. trees for active resource generation, tree trunk for the inactive, degenerated status)
-   inventory and storage
-   means of production crafted by productive resources (e.g. pickaxe for fast food collection) 
-   exchange system (e.g. barter)

In addition to the listed features, Sandbox Society also provides a new Unity frontend client that supports better visualization and remote rendering. 
## Quickstart:
As Sandbox Society inherits the infrastructure from NeuralMMO, it also officially supports Ubuntu 20.04, Windows 10 + WSL, and MacOS (with unknown problems in Windows 11). The only difference in infrastructure is that our unity client and backend are in the same repository, which  eliminates the original step of moving the client implementation to `neural-mmo/forge/embyr` during setup.
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
 
 Having installed the simulation, we could proceed to generate maps for simulation. Run 
 ```
 python Forge.py generate --config=SmallMaps --TERRAIN_RENDER
# --config=LargeMaps
 ```
To view the simulation of scripted agents, run
```
python Forge.py render --config=SmallMaps
```
For remote rendering, 
```
```
 Please read further technical details at the [documentation of NeuralMMO](https://jsuarez5341.github.io/neural-mmo/build/html/rst/userguide.html). 
  
 ## Dependencies:
> Written with [StackEdit](https://stackedit.io/).
