import json
import zipfile

from pathlib import Path

import utils


def create_task_impl(
        work_dir: Path,
        resources_dir: Path,
        network_resources_dir: Path) -> None:
    with open(work_dir / 'task_params.json', 'r') as f:
        params = json.load(f)
    assert len(params['resources']) == 1  # FIXME
    frame_count = len(utils.string_to_frames(params['frames']))
    assert params['subtasks_count'] <= frame_count or params['subtasks_count'] % frame_count == 0  # noqa
    with zipfile.ZipFile(network_resources_dir / '0.zip', 'w') as zipf:
        for resource in params['resources']:
            resource_path = resources_dir / params['resources'][0]
            zipf.write(resource_path, resource)

    with open(work_dir / 'completed_subtasks.json', 'w') as f:
        json.dump([], f)
