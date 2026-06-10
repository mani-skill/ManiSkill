# Community Projects

ManiSkill alone only provides the framework for working with robot learning and simulation. We are excited to see all the different algorithms, benchmarks, and tools the community has built on ManiSkill to make new advancements at the frontier of robotics. We hand-picked a number of notable projects that are well made and recommend those interested in diving deep into different areas of robotics/embodied AI to check out these projects.


## Sim-to-Real Transfer

- [Squint: Fast Visual Reinforcement Learning for Sim-to-Real Robotics](https://aalmuzairee.github.io/squint/) - Fast (< 10 minutes) sim-to-real transfer of skills for the low-cost SO101 robot arm.
- [HandelBot: Real-World Piano Playing via Fast Adaptation of Dexterous Robot Policies](https://amberxie88.github.io/handelbot/) - Sim-to-real transfer of piano skills.
- [DexDrummer: In-Hand, Contact-Rich, and Long-Horizon Dexterous Robot Drumming](https://dexdrummer.github.io/) - Sim-to-real transfer of drumming skills.

## Simulation Evaluations for Real-World policies

- [GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation](https://github.com/luccachiang/GSWorld) - Gaussian splatting added to custom ManiSkill environments for evaluation of real-world robotics foundation models and sim-to-real transfer.
- [Evaluating Real-World Robot Manipulation Policies in Simulation](https://simpler-env.github.io/) - One of the first widely used evaluation benchmarks for robotics foundation models.
- [What Can RL Bring to VLA Generalization? An Empirical Study](https://rlvla.github.io/) - Systematic study of RL finetuning for VLA foundation models.
- [RoboTwin](https://robotwin-platform.github.io/) - A scalable simulation data generator and benchmark targeting bimanual manipulation, testing robotics foundation models and imitation learning algorithms.
- [Molmospaces](https://github.com/allenai/molmospaces) - A large scale benchmark of tasks for robotics evaluation in apartment scenes.

## Benchmarks/Datasets
(note: some benchmarks may overlap with real world policy evaluation projects)

**Robotics Benchmarks/Datasets**
- [MIKASA-Robo-VLA](https://mikasarobo.github.io/) - A memory-intensive robotic manipulation benchmark for Vision-Language-Action research.
- [RoboFactory: Exploring Embodied Agent Collaboration with Compositional Constraints](https://iranqin.github.io/robofactory/) - Benchmark on multi-agent manipulation as well as data collection framework.
- [Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation](https://jianglongye.com/dex1b/) - Large dataset of dextrous manipulation for grasping and articulation in simulation generated via generative models.

**Other**
- [VAGEN: Reinforcing World Model Reasoning for Multi-Turn VLM Agents](https://vagen-ai.github.io/)
- [Do Vision-Language Models Have Internal World Models? Towards an Atomic Evaluation](https://wm-abench.maitrix.org/)

## Algorithms/Models

- [TD-MPC2 / Newt](https://www.nicklashansen.com/NewtWM/) - Training massively multitask world models for continuous control problems.
- [FlashSAC](https://holiday-robot.github.io/FlashSAC/) - Improved version of the SAC RL algorithm to adapt to the high throughput regime of GPU parallelized simulators.
- [A0: An Affordance-Aware Hierarchical Model for General Robotic Manipulation](https://a-embodied.github.io/A0/) - Affordance based hiearchical model for robot manipulation trained on a variety of data sources including simulation data.
- [RLinf](https://github.com/RLinf/RLinf) - RL infrastructure for robotics foundation models.

## Teleoperation

- [ImVR: Immersive VR Teleoperation System for General Purpose Manipulation](https://github.com/liuyulinn/imvr) - Local connection/ALVR based teleoperation.
- [Maniskill Quest Teleop](https://github.com/fracapuano/maniskill-quest-teleop) - WebXR based teleoperation.