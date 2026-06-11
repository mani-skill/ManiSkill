from mani_skill.utils.structs.pose import Pose
from mani_skill.sim.builders.base_builder import BaseBuilder


class ActorBuilder(BaseBuilder):
    # TODO (stao): can this re-use for soft body? need to check newton api
    """A general actor builder for building rigid body objects (actors) in a simulation."""

    name: str | None = None
    """The name of the actor once built."""

    # NOTE (stao): most sims have a concept of a initial pose
    initial_pose: Pose | None = None
    """The initial pose of the actor when it gets built and spawned into the simulation."""

    scene_idxs: list[int] | None = None
    """The list of scene indices to build this actor in. If None, the actor will be built in all scenes."""

    def set_scene_idxs(self, scene_idxs: list[int]):
        self.scene_idxs = scene_idxs
        return self
