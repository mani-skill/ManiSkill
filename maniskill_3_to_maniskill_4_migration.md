# Migration guide from ManiSkill 3 to ManiSkill 4

A guide for migrating code from ManiSkill 3 to ManiSkill 4, in addition to (strong) recommendations of things to be aware of when upgrading to ManiSkill 4, ranging from changes in default values like sim/control frequencies to TODO

## Things that you **must** change and be aware of

- There is no guarantee any randomness / RNG in maniskill 3 will return the same expected randomness in maniskill 4.

- State in maniskill 4 now includes joint targets and joint target velocities if available. Previously these were not included, which can sometimes lead to differences when setting state and taking `None` actions.

## Strong recommendations

- `SimConfig`, `DefaultMaterialsConfig` configs moved from `mani_skill/utils/structs/types.py` to `mani_skill/sim/base_sim.py`. They are now also frozen dataclasses meaning once created, you generally can't edit it (and shouldn't) unless you know what you are doing.

- The default control and simulation frequencies are now set to 60 and 120, matching a more typical ratio used in timekeeping (e.g. 60s per minute) and more typical values used in robotics for control frequencies. Previously they were 20 and 100, which is still a reasonable choice for many tasks when running simulation RL. Default maniskill tasks and baselines will update to be tuned for the 60 120 control/sim frequencies.

- Default tasks have a new environment ID version of `-v4` (to reflect maniskill v4). They are currently all `-v1`. I am not sure why we chose `-v1`.



## Full list of breaking changes including internal changes and deprecations


### Changes:

- `ManiSkillScene` is no longer a used class. To support multiple simulation backends beyond just SAPIEN, we now have a new general `BaseSim` class that defines all the standard functionalities of a simulator needed by ManiSkill, primarily physics (sub) stepping, rendering, and building objects/scenes with model builder type approaches as done by newton and SAPIEN. These simulator backend classes like `NewtonSim` and `SapienSim` are now located in `mani_skill/sim`, moving `ManiSkillScene` type functionality out of the `mani_skill/envs` folder. The envs folder is now reserved primarily for code working with the gymnasium style / environment class way of building tasks in ManiSkill. Finally we call this a `Sim` instead of `Scene` since the word scene gets thrown around a lot and usually is referring to a "group of assets" or a individual parallel environment, not an actual simulator / engine. So now in ManiSkill, a single "scene" is a single parallel environment in the codebase (e.g. actor builders have a scene_idxs property to dictate which parallel environments the actor is built in).

- `BaseSim` class comes with a `BaseSimConfig` class which defines all the most typically important simulation configurations needed in ManiSkill that spread across backends. If a simulator backend doesn't support one of these configuration attributes (e.g. physics/simulation frequency), we probably will not support that simulator. If the attribute is not used (e.g. perhaps a GPU parallelized simulator has no concept of spacing if designed that way), that backend can simply choose to not parse that attribute. These configs are also more often than not frozen dataclasses now, making it harder to make the mistake of assuming some properties can be changed while a GPU sim is running.

### Deprecations

- `ManiSkillScene`, replaced by `NewtonSim` and `SapienSim`
- `ActorBuilder` functions that add collisions no longer have a `patch_radius` or `min_patch_radius` option. These are physx specific and are only available if you specifically are using SAPIEN/physx backends. `is_trigger` is also no longer an argument, it was never used to begin with.
