from abc import ABC, abstractmethod
from typing import Any

from mani_skill.sim.base_sim import BaseSim
from mani_skill.sim.builders.base_builder import BaseBuilder
from mani_skill.utils.structs.actor import Actor
from mani_skill.utils.structs.pose import Pose
from mani_skill.utils.structs.types import Vec3


class BaseActorBuilder(BaseBuilder, ABC):
    # TODO (stao): can this re-use for soft body? need to check newton api
    """Base actor builder for building rigid body objects (actors) in a simulation.
    Actor builders for each simulator backend should inherit from this class."""

    # NOTE (stao): most sims have a concept of a initial pose
    initial_pose: Pose | None = None
    """The initial pose of the actor when it gets built and spawned into the simulation."""

    scene_idxs: list[int] | None = None
    """The list of scene indices to build this actor in. If None, the actor will be
    built in all scenes."""

    def set_scene_idxs(self, scene_idxs: list[int]):
        self.scene_idxs = scene_idxs
        return self

    @abstractmethod
    def build(self, name: str) -> Actor:
        """
        Build the actor.

        Arguments:
            name: The name of the actor.

        Returns:
            The built actor.
        """

    ### Standard primitive building functions, based on Sapien's original ActorBuilder ###
    def add_box_collision(
        self,
        pose: Pose,
        half_size: Vec3 = (1.0, 1.0, 1.0),
        material: Any | None = None,
        density: float = 1000.0,
    ):
        raise NotImplementedError("")

    def add_box_visual(
        self,
        pose: Pose,
        half_size: Vec3 = (1.0, 1.0, 1.0),
        material: Any | Vec3 | None = None,
    ):
        raise NotImplementedError("")


class ActorBuilder(BaseActorBuilder):
    """Actor builder for building rigid body objects (actors) in a simulation. This
    is simulator independent and can be used to build actors across different simulators
    simultaneously to support e.g. rendering in one simulator and running physics in another."""

    _sims: dict[str, BaseSim] = {}
    """dictionary of simulators that will be tracking this builder. There can be multiple simulators
    that track this builder in order to support using different simulators for physics and
    rendering."""

    def add_sim(self, sim: BaseSim):
        self._sims[sim.id] = sim
        return self

    def remove_sim(self, sim: BaseSim):
        self._sims.pop(sim.id)
        return self
