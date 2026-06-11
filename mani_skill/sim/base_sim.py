from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import torch

from mani_skill.sim.builders.actor import ActorBuilder
from mani_skill.sim.builders.articulation import ArticulationBuilder
from mani_skill.utils.structs.pose import Pose


@dataclass(frozen=True)
class DefaultMaterialsConfig:
    # note these frictions are same as unity
    static_friction: float = 0.3
    dynamic_friction: float = 0.3
    restitution: float = 0

    def dict(self):
        return {k: v for k, v in dataclass.asdict(self).items()}


@dataclass(frozen=True)
class BaseSimConfig:
    """
    Base configuration dataclass for the simulation backends.
    """

    spacing: float = 5.0
    """Controls the spacing between parallel environments when simulating on GPU in meters. Increase
    this value if you expect objects in one parallel environment to impact objects within
    this spacing distance."""
    sim_freq: int = 120
    """simulation frequency (Hz)."""
    control_freq: int = 60
    """control frequency (Hz). Every control step (e.g. env.step)
    contains (sim_freq / control_freq) physics steps."""

    default_materials_config: DefaultMaterialsConfig = field(
        default_factory=DefaultMaterialsConfig
    )


class BaseSim(ABC):
    """
    Base class for all simulation backends.

    A simulation backend consists of primarily a physics engine and a renderer. It is possible for
    a simulation backend to only have one or the other as well.
    """

    id: str
    """the id of the simulation backend"""

    device: torch.device
    """the torch device on which the simulation is running"""

    def __init__(self, cfg: BaseSimConfig | None = None):
        self.cfg = cfg or BaseSimConfig()

    ### Code for adding builders to a scene for rendering/physics simulation ###
    def create_actor_builder(self) -> ActorBuilder:
        """
        Creates an ActorBuilder object that can be used to build actors in this scene.
        """
        return ActorBuilder().add_sim(self)

    def create_articulation_builder(self) -> ArticulationBuilder:
        """
        Creates an ArticulationBuilder object that can be used to build articulations in this scene.
        """
        return ArticulationBuilder().add_sim(self)

    ### Code for compiling simulator scene for rendering ###
    @abstractmethod
    def compile_render_scene(self):
        """
        Compiles the simulation scene for rendering.
        """

    ### Rendering code ###
    # TODO (stao): add_camera or call this add_sensor and eventually support other kinds of sensors?
    # feel like cameras need a lot of special treatment in general...
    # (e.g. mounting, batching+tiling, evals etc.)
    @abstractmethod
    def add_camera(self, pose: Pose):
        """
        Adds a camera to the simulation scene.
        """

    ### Code for compiling simulator scene for physical simulation ###
    @abstractmethod
    def compile_physical_scene(self):
        """
        Compiles the simulation scene for physical simulation. Usually necessary to have an explicit
        compilation stage for simulators with GPU parallelization, but some simulators permit
        larger changes to the physical scene at runtime.
        """

    ### Physical simulation code ###
    @abstractmethod
    def physics_step(self):
        """
        Runs a single physics step at `self.cfg.sim_freq` Hz.
        """
