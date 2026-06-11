from mani_skill.utils.structs.pose import Pose
from mani_skill.sim.base_sim import BaseSim


class ActorBuilder:
    # TODO (stao): can this re-use for soft body? need to check newton api
    """A general actor builder for building rigid body objects (actors) in a simulation"""

    initial_pose: Pose | None = (
        None  # NOTE (stao): most sims have a concept of a initial pose
    )
    """The initial pose of the actor when it gets built and spawned into the simulation"""

    scene_idxs: list[int] | None = None
    """The list of scene indices to build this actor in. If None, the actor will be built in all scenes"""

    _sims: dict[str, BaseSim] = {}
    """dictionary of sim backends that will be tracking this actor builder. There can be multiple sims
    that track this actor builder in order to support using different sim backends for physics and rendering."""

    def __init__(self):
        pass

    def add_sim(self, sim: BaseSim):
        self._sims[sim.id] = sim
        return self

    def remove_sim(self, sim: BaseSim):
        self._sims.pop(sim.id)
        return self

    def set_scene_idxs(self, scene_idxs: list[int]):
        self.scene_idxs = scene_idxs
        return self
