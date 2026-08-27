"""Pawan Video Studio API.

This endpoint is intentionally project-agnostic. The client submits a Studio
manifest; the server renders it with the reusable studio engine. Brand assets,
scene order, camera motion and subtitle styling therefore live in the project
manifest rather than in Python code.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import BackgroundTasks, Request
from pydantic import BaseModel, Field

from app.controllers.v1.base import new_router
from app.utils import utils
from studio.engine import CAMERA_STYLES, render

router = new_router()


class StudioRenderRequest(BaseModel):
    manifest: dict = Field(..., description="Pawan Video Studio project manifest")
    output_name: str = Field("studio-final.mp4", description="Output filename")



def _render_job(task_id: str, manifest: dict, output: str) -> None:
    task_dir = utils.storage_dir(os.path.join("studio", task_id), create=True)
    status_path = os.path.join(task_dir, "status.json")
    try:
        Path(status_path).write_text(
            json.dumps({"state": "processing", "output": output}, indent=2),
            encoding="utf-8",
        )
        render(manifest, output)
        Path(status_path).write_text(
            json.dumps({"state": "complete", "output": output}, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        Path(status_path).write_text(
            json.dumps({"state": "failed", "error": str(exc)}, indent=2),
            encoding="utf-8",
        )


@router.get("/studio/cameras", summary="List Studio camera moves")
def list_cameras(request: Request):
    return utils.get_response(200, {"cameras": list(CAMERA_STYLES)})


@router.post("/studio/render", summary="Render a Pawan Video Studio project")
def render_studio(
    request: Request,
    body: StudioRenderRequest,
    background_tasks: BackgroundTasks,
):
    task_id = utils.get_uuid()
    task_dir = utils.storage_dir(os.path.join("studio", task_id), create=True)
    manifest_path = os.path.join(task_dir, "project.json")
    output = os.path.join(task_dir, body.output_name)
    Path(manifest_path).write_text(
        json.dumps(body.manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    background_tasks.add_task(_render_job, task_id, body.manifest, output)
    return utils.get_response(
        202,
        {
            "task_id": task_id,
            "state": "queued",
            "manifest": manifest_path,
            "output": output,
        },
    )


@router.get("/studio/tasks/{task_id}", summary="Get Studio render status")
def studio_status(request: Request, task_id: str):
    status_path = os.path.join(utils.storage_dir("studio", create=True), task_id, "status.json")
    if not os.path.exists(status_path):
        return utils.get_response(404, message="Studio task not found")
    data = json.loads(Path(status_path).read_text(encoding="utf-8"))
    return utils.get_response(200, data)
