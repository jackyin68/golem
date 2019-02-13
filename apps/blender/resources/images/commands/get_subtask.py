import json
import math
import os

from pathlib import Path

import utils


def get_subtask_impl(
        subtask_id: int,
        work_dir: Path,
        resources_dir: Path,
        network_resources_dir: Path):
    with open(work_dir / 'task_params.json', 'r') as f:
        params = json.load(f)
    assert 0 <= subtask_id < params['subtasks_count']

    all_frames = utils.string_to_frames(params['frames'])

    scene_file = os.path.basename(params['resources'][0])  # noqa FIXME find correct scene file

    frames, parts = _choose_frames(
        all_frames,
        subtask_id,
        params['subtasks_count'],
    )
    min_y = (subtask_id % parts) / parts
    max_y = (subtask_id % parts + 1) / parts

    extra_data = {
        "scene_file": scene_file,
        "resolution": params['resolution'],
        "use_compositing": False,
        "samples": 0,
        "frames": frames,
        "output_format": params['format'],
        "borders": [0.0, min_y, 1.0, max_y],

        "resources": [0],
    }

    with open(work_dir / 'subtask{}.json'.format(subtask_id), 'w') as f:
        json.dump(extra_data, f)


def _choose_frames(frames, start_task, total_tasks):
    if total_tasks <= len(frames):
        subtasks_frames = int(math.ceil(len(frames) / total_tasks))
        start_frame = (start_task - 1) * subtasks_frames
        end_frame = min(start_task * subtasks_frames, len(frames))
        return frames[start_frame:end_frame], 1
    else:
        parts = max(1, int(total_tasks / len(frames)))
        return [frames[int((start_task - 1) / parts)]], parts
