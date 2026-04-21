# User Guide

![teaser](./teaser.jpg)
<p style="text-align: center; font-size: 0.8rem; color: #999;margin-top: -1rem;">Sample of environments/robots rendered with ray-tracing. Scene datasets sourced from AI2THOR and ReplicaCAD</p>

[![Downloads](https://static.pepy.tech/badge/mani_skill)](https://pepy.tech/project/mani_skill)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/haosulab/ManiSkill/blob/main/examples/tutorials/1_quickstart.ipynb)
[![PyPI version](https://badge.fury.io/py/mani-skill.svg)](https://badge.fury.io/py/mani-skill)
[![Docs status](https://img.shields.io/badge/docs-passing-brightgreen.svg)](https://maniskill.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/996566046414753822?logo=discord)](https://discord.gg/x8yUZe5AdN)

ManiSkill is an open-source framework for robot simulation and training powered by [SAPIEN](https://sapien.ucsd.edu/), with a strong focus on manipulation skills. Among its features include:
- GPU parallelized visual data collection system. On the high end you can collect RGBD + Segmentation data at 30,000+ FPS on a 4090 GPU
- GPU parallelized simulation, enabling high throughput state-based synthetic data collection in simulation
- GPU parallelized heterogeneous simulation, where every parallel environment has a completely different scene/set of objects
- Example tasks cover a wide range of different robot embodiments (humanoids, mobile manipulators, single-arm robots) as well as a wide range of different tasks (table-top, drawing/cleaning, dexterous manipulation)
- Flexible and simple task building API that abstracts away much of the complex GPU memory management code via an object oriented design
- Real2sim environments for scalably evaluating real-world policies 100x faster via GPU simulation.
- Sim2real examples for deploying policies trained in simulation to the real world
- Many tuned robot learning baselines in Reinforcement Learning (e.g. PPO, SAC, [TD-MPC2](https://github.com/nicklashansen/tdmpc2)), Imitation Learning (e.g. Behavior Cloning, [Diffusion Policy](https://github.com/real-stanford/diffusion_policy)), and large Vision Language Action (VLA) models (e.g. [Octo](https://github.com/octo-models/octo), [RDT-1B](https://github.com/thu-ml/RoboticsDiffusionTransformer), [RT-x](https://robotics-transformer-x.github.io/))

For more details we encourage you to take a look at our [paper](https://arxiv.org/abs/2410.00425), published at [RSS 2025](https://roboticsconference.org/).

Please refer to our [documentation](https://maniskill.readthedocs.io/en/latest/user_guide) to learn more information from tutorials on building tasks to sim2real to running baselines. If you find any bugs or have any feature requests please post them to our [GitHub issues](https://github.com/haosulab/ManiSkill/issues/) or discuss about them on [GitHub discussions](https://github.com/haosulab/ManiSkill/discussions/). We also have a [Discord Server](https://discord.gg/x8yUZe5AdN) through which we make announcements and discuss about ManiSkill.

Users looking for the original ManiSkill2 can find the commit for that codebase at the [v0.5.3 tag](https://github.com/haosulab/ManiSkill/tree/v0.5.3)


```{toctree}
:caption: Get started

getting_started/installation
getting_started/quickstart
getting_started/docker
```

```{toctree}
:maxdepth: 3
:caption: Resources

demos/index
tutorials/index
concepts/index
datasets/index
data_collection/index
reinforcement_learning/index
learning_from_demos/index
vision_language_action_models/index
wrappers/index
```

```{toctree}
:maxdepth: 2
:caption: Additional Resources

additional_resources/performance_benchmarking
additional_resources/citation
```