"""Regression tests for #1302: gravity accepts plain lists/tuples in sim config.

A plain list was already accepted (fixed in #1306), but a tuple was still
rejected by the strict dacite parsing in BaseEnv.__init__ with
``UnionMatchError: can not match type "tuple" ...``. These tests pin the
behavior for all three input forms through the exact parsing path BaseEnv
uses (merge user overrides into the default SimConfig dict, then
``dacite.from_dict(..., strict=True)``), plus direct ``SceneConfig``
construction.
"""

import dacite
import numpy as np
import pytest

from mani_skill.utils.common import dict_merge
from mani_skill.utils.structs.types import SceneConfig, SimConfig


def parse_sim_config(user_sim_config: dict) -> SimConfig:
    """Mirror BaseEnv.__init__ (mani_skill/envs/sapien_env.py)."""
    merged = SimConfig().dict()
    dict_merge(merged, user_sim_config)
    return dacite.from_dict(
        data_class=SimConfig, data=merged, config=dacite.Config(strict=True)
    )


@pytest.mark.parametrize(
    "gravity", [[0, 0, -9.81], (0, 0, -9.81), np.array([0, 0, -9.81])]
)
def test_sim_config_gravity_sequence_accepted(gravity):
    cfg = parse_sim_config(dict(scene_config=dict(gravity=gravity)))
    assert isinstance(cfg.scene_config.gravity, np.ndarray)
    np.testing.assert_array_equal(cfg.scene_config.gravity, [0, 0, -9.81])


def test_sim_config_gravity_default_unchanged():
    cfg = parse_sim_config(dict())
    assert isinstance(cfg.scene_config.gravity, np.ndarray)
    np.testing.assert_array_equal(cfg.scene_config.gravity, [0, 0, -9.81])


@pytest.mark.parametrize("gravity", [[0, 0, -9.81], (0, 0, -9.81)])
def test_scene_config_direct_construction_normalizes_gravity(gravity):
    cfg = SceneConfig(gravity=gravity)
    assert isinstance(cfg.gravity, np.ndarray)
    np.testing.assert_array_equal(cfg.gravity, [0, 0, -9.81])


def test_sim_config_object_round_trip_with_tuple_gravity():
    cfg = SimConfig(scene_config=SceneConfig(gravity=(0, 0, -9.81)))
    reparsed = parse_sim_config(cfg.dict())
    assert isinstance(reparsed.scene_config.gravity, np.ndarray)
    np.testing.assert_array_equal(reparsed.scene_config.gravity, [0, 0, -9.81])
