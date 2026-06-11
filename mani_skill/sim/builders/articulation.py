from mani_skill.utils.structs.pose import Pose
from mani_skill.sim.builders.base_builder import BaseBuilder


class ArticulationBuilder(BaseBuilder):
    """A general articulation builder for building articulated objects in a simulation."""

    initial_pose: Pose | None = None
    """The initial pose of the articulation's root link when it gets built and spawned into the simulation."""

    scene_idxs: list[int] | None = None
    """The list of scene indices to build this articulation in. If None, the articulation will be built in all scenes"""

    def set_scene_idxs(self, scene_idxs: list[int]):
        self.scene_idxs = scene_idxs
        return self
