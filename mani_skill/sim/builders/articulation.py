from mani_skill.utils.structs.pose import Pose


class ArticulationBuilder:
    """A general articulation builder for building articulated objects in a simulation"""

    initial_pose: Pose | None = None
    """The initial pose of the articulation's root link when it gets built and spawned into the simulation"""

    scene_idxs: list[int] | None = None
    """The list of scene indices to build this actor in. If None, the actor will be built in all scenes"""

    def __init__(self):
        pass
