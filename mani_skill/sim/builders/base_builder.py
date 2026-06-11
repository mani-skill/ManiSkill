from mani_skill.sim.base_sim import BaseSim
from abc import ABC


class BaseBuilder(ABC):
    """Base builder class for constructing objects in a simulation."""

    _sims: dict[str, BaseSim] = {}
    """dictionary of sim backends that will be tracking this builder. There can be multiple sims
    that track this builder in order to support using different sim backends for physics and rendering."""

    def add_sim(self, sim: BaseSim):
        self._sims[sim.id] = sim
        return self

    def remove_sim(self, sim: BaseSim):
        self._sims.pop(sim.id)
        return self
