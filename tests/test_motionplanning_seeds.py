import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import numpy as np
import pytest


@pytest.fixture
def run_motionplanning(monkeypatch, tmp_path):
    """Run the real dispatch and retry loops with a deterministic solver and recorder."""

    def run(robot, workers, trajectories, failed_seeds):
        attempts = []

        class Recorder:
            def __init__(self, env, *, output_dir, trajectory_name, **kwargs):
                self.path = Path(output_dir, f"{trajectory_name}.h5")
                self._h5_file = SimpleNamespace(filename=str(self.path))
                self.seeds = []

            def flush_trajectory(self, save=True):
                if save:
                    self.seeds.append(self.seed)

            def close(self):
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.touch()
                self.path.with_suffix(".json").write_text(json.dumps(self.seeds))

        def solve(recorder, seed, debug, vis):
            attempts.append(seed)
            if len(attempts) > 2 * trajectories:
                pytest.fail("The generator exceeded the expected number of attempts")
            recorder.seed = seed
            if seed in failed_seeds:
                return -1
            return [{"success": np.array(True), "elapsed_steps": np.array(1)}]

        def merge(output, inputs):
            seeds = []
            for source in inputs:
                seeds.extend(json.loads(Path(source).with_suffix(".json").read_text()))
            Path(output).with_suffix(".json").write_text(json.dumps(seeds))

        def stub_module(name, **attrs):
            module = ModuleType(name)
            vars(module).update(attrs)
            monkeypatch.setitem(sys.modules, name, module)

        def get_solution(name):
            if name.startswith("solve"):
                return solve
            raise AttributeError(name)

        class InProcessPool:
            def __init__(self, processes):
                pass

            def starmap(self, fn, arguments):
                return [fn(*args) for args in arguments]

            def close(self):
                pass

        stub_module("mani_skill.utils.wrappers.record", RecordEpisode=Recorder)
        stub_module("mani_skill.trajectory.merge_trajectory", merge_trajectories=merge)
        planning_module = f"mani_skill.examples.motionplanning.{robot}"
        stub_module(f"{planning_module}.solutions", __getattr__=get_solution)

        root = Path(__file__).resolve().parents[1]
        path = root / "mani_skill" / "examples" / "motionplanning" / robot / "run.py"
        spec = importlib.util.spec_from_file_location(f"test_{robot}_runner", path)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        monkeypatch.setattr(runner.gym, "make", lambda *args, **kwargs: object())
        monkeypatch.setattr(runner.mp, "Pool", InProcessPool)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                str(path),
                "--record-dir",
                str(tmp_path),
                "--traj-name",
                "seed-test",
                "--num-traj",
                str(trajectories),
                "--num-procs",
                str(workers),
                "--only-count-success",
            ],
        )
        runner.main(runner.parse_args())
        (recording,) = tmp_path.glob("*/motionplanning/*.json")
        return attempts, json.loads(recording.read_text())

    return run


@pytest.mark.parametrize("robot", ["panda", "so100", "xarm6"])
@pytest.mark.parametrize("workers", [2, 3])
def test_parallel_motionplanning_records_unique_seeds_after_retry(
    run_motionplanning, robot, workers
):
    count = workers * 2
    attempts, recorded = run_motionplanning(robot, workers, count, failed_seeds={0})

    assert len(recorded) == count
    assert len(set(attempts)) == len(attempts), attempts
    assert 0 not in recorded
    assert len(set(recorded)) == len(recorded), recorded


@pytest.mark.parametrize("robot, start_seed", [("panda", 0), ("so100", 9), ("xarm6", 0)])
def test_single_worker_motionplanning_retries_with_consecutive_seeds(
    run_motionplanning, robot, start_seed
):
    attempts, recorded = run_motionplanning(
        robot, workers=1, trajectories=2, failed_seeds={start_seed}
    )

    assert attempts == [start_seed, start_seed + 1, start_seed + 2]
    assert recorded == [start_seed + 1, start_seed + 2]


@pytest.mark.parametrize("robot", ["panda", "so100", "xarm6"])
def test_parallel_motionplanning_retries_keep_worker_seed_streams_disjoint(
    run_motionplanning, robot
):
    attempts, recorded = run_motionplanning(
        robot, workers=2, trajectories=4, failed_seeds={0}
    )

    assert attempts == [0, 2, 4, 1, 3]
    assert recorded == [2, 4, 1, 3]
