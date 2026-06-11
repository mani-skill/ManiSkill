from mani_skill.sim.base_sim import BaseSim, BaseSimConfig
from dataclasses import dataclass, field
import numpy as np


@dataclass
class GPUMemoryConfig:
    """A gpu memory configuration dataclass that neatly holds all parameters that configure physx GPU memory for simulation"""

    temp_buffer_capacity: int = 2**24
    """Increase this if you get 'PxgPinnedHostLinearMemoryAllocator: overflowing initial allocation size, increase capacity to at least %.' """
    max_rigid_contact_count: int = 2**19
    """Increase this if you get 'Contact buffer overflow detected'"""
    max_rigid_patch_count: int = (
        2**18
    )  # 81920 is SAPIEN default but most tasks work with 2**18
    """Increase this if you get 'Patch buffer overflow detected'"""
    heap_capacity: int = 2**26
    found_lost_pairs_capacity: int = (
        2**25
    )  # 262144 is SAPIEN default but most tasks work with 2**25
    found_lost_aggregate_pairs_capacity: int = 2**10
    total_aggregate_pairs_capacity: int = 2**10
    collision_stack_size: int = 64 * 64 * 1024  # this is the same default as SAPIEN
    """Increase this if you get 'Collision stack overflow detected'"""

    def dict(self):
        return {k: v for k, v in dataclass.asdict(self).items()}


@dataclass
class SceneConfig:
    gravity: np.ndarray | list[float] = field(
        default_factory=lambda: np.array([0, 0, -9.81])
    )
    bounce_threshold: float = 2.0
    sleep_threshold: float = 0.005
    contact_offset: float = 0.02
    rest_offset: float = 0
    solver_position_iterations: int = 15
    solver_velocity_iterations: int = 1
    enable_pcm: bool = True
    enable_tgs: bool = True
    enable_ccd: bool = False
    enable_enhanced_determinism: bool = False
    enable_friction_every_iteration: bool = True
    cpu_workers: int = 0

    def dict(self):
        return {k: v for k, v in dataclass.asdict(self).items()}

    # cpu_workers=min(os.cpu_count(), 4)
    # NOTE (fxiang): PCM is enabled for GPU sim regardless.
    # NOTE (fxiang): smaller contact_offset is faster as less contacts are considered, but some contacts may be missed if distance changes too fast
    # NOTE (fxiang): solver iterations 15 is recommended to balance speed and accuracy. If stable grasps are necessary >= 20 is preferred.
    # NOTE (fxiang): can try using more cpu_workers as it may also make it faster if there are a lot of collisions, collision filtering is on CPU
    # NOTE (fxiang): enable_enhanced_determinism is for CPU probably. If there are 10 far apart sub scenes, this being True makes it so they do not impact each other at all


@dataclass(frozen=True)
class SapienSimConfig(BaseSimConfig):
    gpu_memory_config: GPUMemoryConfig = field(default_factory=GPUMemoryConfig)
    scene_config: SceneConfig = field(default_factory=SceneConfig)


class SapienSim(BaseSim):
    pass
