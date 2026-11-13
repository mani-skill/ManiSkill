import numpy as np
import pytest
import gymnasium as gym
from gymnasium import spaces

from mani_skill.utils import gym_utils


def _act_rgbd_space():
    """The observation space of the ACT rgbd evaluation envs (issue #992):
    state is float32, rgb is uint8 and depth is float16."""
    return spaces.Dict(
        {
            "state": spaces.Box(-np.inf, np.inf, shape=(8,), dtype=np.float32),
            "rgb": spaces.Box(0, 255, shape=(1, 3, 32, 32), dtype=np.uint8),
            "depth": spaces.Box(
                -np.inf, np.inf, shape=(1, 1, 32, 32), dtype=np.float16
            ),
        }
    )


class _DummyRGBDEnv(gym.Env):
    """Minimal env with the ACT rgbd observation space (no simulation)."""

    def __init__(self):
        self.observation_space = _act_rgbd_space()
        self.action_space = spaces.Box(-1, 1, shape=(4,), dtype=np.float32)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        return self.observation_space.sample(), {}

    def step(self, action):
        return self.observation_space.sample(), 0.0, False, False, {}


def _gym_supports_float16_shared_memory():
    """gymnasium >= 1.4 allocates a uint8 buffer for dtypes without an
    ``array`` typecode (e.g. float16); earlier versions raise TypeError."""
    parts = gym.__version__.split(".")
    try:
        major, minor = int(parts[0]), int(parts[1])
    except (IndexError, ValueError):
        return False
    return (major, minor) >= (1, 4)


def test_make_async_vector_env_with_float16_obs():
    """Regression test for #992: constructing an AsyncVectorEnv must not
    raise ``TypeError: this type has no size`` for observation spaces
    containing float16 (e.g. the ACT rgbd depth images)."""
    env = gym_utils.make_async_vector_env(
        [lambda: _DummyRGBDEnv(), lambda: _DummyRGBDEnv()]
    )
    obs, _ = env.reset(seed=0)
    assert obs["depth"].dtype == np.float16
    obs, _, _, _, _ = env.step(
        [env.single_action_space.sample() for _ in range(env.num_envs)]
    )
    assert obs["depth"].dtype == np.float16
    env.close()


@pytest.mark.skipif(
    _gym_supports_float16_shared_memory(),
    reason="gymnasium >= 1.4 supports float16 in shared memory",
)
def test_plain_async_vector_env_raises_for_float16_obs():
    """Documents the upstream limitation that make_async_vector_env works
    around: gymnasium < 1.4 cannot place float16 observations in shared
    memory, so the plain constructor raises ``TypeError``."""
    with pytest.raises(TypeError, match="has no size"):
        gym.vector.AsyncVectorEnv(
            [lambda: _DummyRGBDEnv(), lambda: _DummyRGBDEnv()],
            context="forkserver",
        )
