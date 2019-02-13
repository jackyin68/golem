import json
import os
import shutil
import zipfile
from pathlib import Path

from scripts_verifier import verificator

import utils
from renderingtaskcollector import RenderingTaskCollector


def verify_impl(
        subtask_id: int,
        work_dir: Path,
        resources_dir: Path,
        network_resources_dir: Path,
        results_dir: Path,
        network_results_dir: Path) -> None:
    with open(work_dir / 'task_params.json', 'r') as f:
        task_params = json.load(f)
    with open(work_dir / f'subtask{subtask_id}.json', 'r') as f:
        params = json.load(f)
    subtask_work_dir = work_dir / f'subtask{subtask_id}'
    subtask_work_dir.mkdir(exist_ok=True)
    subtask_results_dir = subtask_work_dir / 'results'
    subtask_results_dir.mkdir(exist_ok=True)
    subtask_output_dir = subtask_work_dir / 'output'
    subtask_output_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(network_results_dir / f'{subtask_id}.zip', 'r') as zipf:  # noqa
        zipf.extractall(subtask_results_dir)

    verdict = verificator.verify(
        list(map(lambda f: subtask_results_dir / f, os.listdir(subtask_results_dir))),  # noqa
        params['borders'],
        resources_dir / params['scene_file'],
        params['resolution'],
        params['samples'],
        params['frames'],
        params['output_format'],
        'verify',
        mounted_paths={
            'OUTPUT_DIR': str(subtask_output_dir),
            'WORK_DIR': str(subtask_work_dir),
        }
    )
    print("Verdict:", verdict)
    if not verdict:
        return

    with open(work_dir / 'completed_subtasks.json', 'r') as f:
        completed_subtasks = json.load(f)
    completed_subtasks.append(subtask_id)
    with open(work_dir / 'completed_subtasks.json', 'w') as f:
        json.dump(completed_subtasks, f)
    completed_subtasks = set(completed_subtasks)

    frame_count = len(utils.string_to_frames(task_params['frames']))
    parts = task_params['subtasks_count'] // frame_count
    if parts <= 1:
        for res, frame_num in enumerate(params['frames']):
            shutil.copy2(
                subtask_results_dir / f'result{res+1:04d}.{params["output_format"]}',  # noqa
                results_dir / f'result{frame_num:04d}.{params["output_format"]}',  # noqa
            )
        return

    frame_id = subtask_id // parts
    subtask_ids = list(range(frame_id * parts, (frame_id + 1) * parts))
    if not all([i in completed_subtasks for i in subtask_ids]):
        return

    collector = RenderingTaskCollector(
        width=params['resolution'][0],
        height=params['resolution'][1],
    )
    for i in subtask_ids[::-1]:
        collector.add_img_file(str(subtask_results_dir / f'result0001.{params["output_format"].lower()}'))  # noqa
    with collector.finalize() as image:
        image.save_with_extension(results_dir / f'result{frame_id+1:04d}', params['output_format'])  # noqa
