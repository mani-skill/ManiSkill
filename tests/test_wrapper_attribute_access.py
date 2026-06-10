"""Test that trajectory replay code correctly accesses BaseEnv attributes
through gymnasium wrappers using .unwrapped.

This addresses GitHub issue #1366: gymnasium >= 1.0 no longer propagates
attribute lookups through the wrapper chain, so env.agent, env.device, and
env.set_state_dict() must be accessed via env.unwrapped.
"""

import ast
import os
import textwrap

import pytest

# ---------------------------------------------------------------------------
# Helpers – lightweight AST inspection
# ---------------------------------------------------------------------------


def _collect_attribute_chains(source: str) -> list[tuple[int, str]]:
    """Return (line_number, dotted_chain) for every attribute access on
    variables named ``env`` or ``ori_env`` in *source*.

    For example, ``env.unwrapped.agent`` produces ``"env.unwrapped.agent"``
    while ``env.step(a)`` produces ``"env.step"``.
    """
    tree = ast.parse(source)
    results: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        # Walk the chain bottom-up to build the dotted string.
        parts: list[str] = []
        cur = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name) and cur.id in ("env", "ori_env"):
            parts.append(cur.id)
            parts.reverse()
            results.append((node.lineno, ".".join(parts)))
    return results


# Attributes that belong to BaseEnv and are NOT available on gymnasium
# wrappers (TimeLimitWrapper, RecordEpisode, etc.) in gymnasium >= 1.0.
_BASE_ENV_ONLY_ATTRS = frozenset(
    {
        "agent",
        "device",
        "set_state_dict",
        "get_state_dict",
        "control_mode",
        "obs_mode",
        "control_freq",
        "backend",
    }
)

# Attributes that are fine to call directly on a wrapper because the wrapper
# itself (or gymnasium.Wrapper) defines them.
_WRAPPER_SAFE_ATTRS = frozenset(
    {
        "step",
        "reset",
        "close",
        "render",
        "render_human",
        "action_space",
        "observation_space",
        "unwrapped",
        "base_env",
        "env",
        # RecordEpisode specific
        "save_trajectory",
        "flush_trajectory",
        "flush_video",
        "_trajectory_buffer",
        "_h5_file",
    }
)


def _find_unsafe_accesses(source: str) -> list[tuple[int, str]]:
    """Return a list of (line, chain) where a BaseEnv-only attribute is
    accessed on ``env`` / ``ori_env`` without going through ``.unwrapped``
    or ``.base_env`` first.
    """
    violations: list[tuple[int, str]] = []
    for lineno, chain in _collect_attribute_chains(source):
        parts = chain.split(".")
        # parts[0] is "env" or "ori_env"
        if len(parts) < 2:
            continue
        first_attr = parts[1]
        if first_attr in _BASE_ENV_ONLY_ATTRS:
            # Direct access like env.agent or ori_env.set_state_dict
            violations.append((lineno, chain))
    return violations


# ---------------------------------------------------------------------------
# The actual tests
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLAY_TRAJECTORY_PATH = os.path.join(
    _REPO_ROOT, "mani_skill", "trajectory", "replay_trajectory.py"
)
CONVERSION_PATH = os.path.join(
    _REPO_ROOT, "mani_skill", "trajectory", "utils", "actions", "conversion.py"
)


def test_replay_trajectory_no_unsafe_wrapper_attribute_access():
    """replay_trajectory.py must not access BaseEnv-only attributes
    directly on wrapped env objects (gymnasium >= 1.0 compatibility)."""
    with open(REPLAY_TRAJECTORY_PATH) as f:
        source = f.read()
    violations = _find_unsafe_accesses(source)
    assert violations == [], (
        "Found direct BaseEnv attribute access through wrapper in "
        f"replay_trajectory.py (needs .unwrapped): {violations}"
    )


def test_conversion_no_unsafe_wrapper_attribute_access():
    """conversion.py must not access BaseEnv-only attributes directly on
    wrapped env objects (gymnasium >= 1.0 compatibility)."""
    with open(CONVERSION_PATH) as f:
        source = f.read()
    violations = _find_unsafe_accesses(source)
    assert violations == [], (
        "Found direct BaseEnv attribute access through wrapper in "
        f"conversion.py (needs .unwrapped): {violations}"
    )


def test_unwrapped_is_used_for_agent_access():
    """conversion.py should use env.unwrapped.agent, not env.agent."""
    with open(CONVERSION_PATH) as f:
        source = f.read()
    chains = _collect_attribute_chains(source)
    agent_accesses = [(ln, c) for ln, c in chains if "agent" in c.split(".")]
    for lineno, chain in agent_accesses:
        parts = chain.split(".")
        agent_idx = parts.index("agent")
        assert (
            agent_idx >= 2 and parts[agent_idx - 1] == "unwrapped"
        ), f"Line {lineno}: '{chain}' accesses .agent without .unwrapped"


def test_unwrapped_is_used_for_device_access():
    """conversion.py should use env.unwrapped.device, not env.device."""
    with open(CONVERSION_PATH) as f:
        source = f.read()
    chains = _collect_attribute_chains(source)
    device_accesses = [
        (ln, c) for ln, c in chains if c.split(".")[-1] == "device" or ".device" in c
    ]
    for lineno, chain in device_accesses:
        parts = chain.split(".")
        if "device" in parts:
            device_idx = parts.index("device")
            assert (
                device_idx >= 2 and parts[device_idx - 1] == "unwrapped"
            ), f"Line {lineno}: '{chain}' accesses .device without .unwrapped"


def test_unwrapped_is_used_for_set_state_dict():
    """replay_trajectory.py should use ori_env.unwrapped.set_state_dict,
    not ori_env.set_state_dict."""
    with open(REPLAY_TRAJECTORY_PATH) as f:
        source = f.read()
    chains = _collect_attribute_chains(source)
    state_dict_accesses = [(ln, c) for ln, c in chains if "set_state_dict" in c]
    for lineno, chain in state_dict_accesses:
        parts = chain.split(".")
        ssd_idx = parts.index("set_state_dict")
        # Must be accessed via .unwrapped or .base_env
        assert ssd_idx >= 2 and parts[ssd_idx - 1] in ("unwrapped", "base_env"), (
            f"Line {lineno}: '{chain}' accesses .set_state_dict without "
            ".unwrapped or .base_env"
        )


class TestMockWrapperAttributeAccess:
    """Simulate the gymnasium >= 1.0 behavior where wrappers do NOT
    forward attribute lookups to the base environment."""

    def test_timelimit_wrapper_blocks_attribute_access(self):
        """Verify that our mock correctly blocks direct attribute access,
        mimicking gymnasium >= 1.0 behavior."""

        class FakeBaseEnv:
            agent = "fake_agent"
            device = "cpu"

            def set_state_dict(self, d):
                pass

        class FakeTimeLimitWrapper:
            """Mimics gymnasium >= 1.0 wrapper: does NOT propagate attrs."""

            def __init__(self, env):
                self._env = env

            @property
            def unwrapped(self):
                return self._env

            def step(self, action):
                pass

            def reset(self, **kwargs):
                pass

        base = FakeBaseEnv()
        wrapped = FakeTimeLimitWrapper(base)

        # Direct access should fail (like gymnasium >= 1.0)
        with pytest.raises(AttributeError):
            _ = wrapped.agent
        with pytest.raises(AttributeError):
            _ = wrapped.device
        with pytest.raises(AttributeError):
            wrapped.set_state_dict({})

        # .unwrapped access should work
        assert wrapped.unwrapped.agent == "fake_agent"
        assert wrapped.unwrapped.device == "cpu"
        wrapped.unwrapped.set_state_dict({})  # should not raise
