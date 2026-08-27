"""Pawan Video Studio API: planning, QC, rendering and platform profiles."""
from __future__ import annotations
import json, os
from pathlib import Path
from fastapi import BackgroundTasks, Request
from pydantic import BaseModel, Field
from app.controllers.v1.base import new_router
from app.utils import utils
from studio.engine import CAMERA_STYLES, render
from studio.director import MasterDirector
from studio.qc import QualityGate
from studio.platforms import all_profiles, profile

router = new_router()

class StudioPlanRequest(BaseModel):
    brief: dict = Field(...)
    seed: int = 42

class StudioRenderRequest(BaseModel):
    manifest: dict = Field(...)
    output_name: str = "studio-final.mp4"
    self_revise: bool = True


def _render_job(task_id: str, manifest: dict, output: str) -> None:
    task_dir = utils.storage_dir(os.path.join("studio", task_id), create=True)
    status_path = os.path.join(task_dir, "status.json")
    try:
        Path(status_path).write_text(json.dumps({"state":"processing","output":output}, indent=2), encoding="utf-8")
        report = QualityGate().check(manifest)
        if not report["ok"]:
            Path(status_path).write_text(json.dumps({"state":"failed","stage":"quality_gate","quality":report}, indent=2), encoding="utf-8")
            return
        render(manifest, output)
        Path(status_path).write_text(json.dumps({"state":"complete","output":output,"quality":report}, indent=2), encoding="utf-8")
    except Exception as exc:
        Path(status_path).write_text(json.dumps({"state":"failed","error":str(exc)}, indent=2), encoding="utf-8")

@router.get("/studio/cameras")
def list_cameras(request: Request):
    return utils.get_response(200, {"cameras": list(CAMERA_STYLES)})

@router.get("/studio/platforms")
def list_platforms(request: Request):
    return utils.get_response(200, {"profiles": all_profiles()})

@router.get("/studio/platforms/{name}")
def get_platform(request: Request, name: str):
    try: return utils.get_response(200, profile(name))
    except ValueError as exc: return utils.get_response(404, message=str(exc))

@router.post("/studio/plan")
def plan_studio(request: Request, body: StudioPlanRequest):
    manifest = MasterDirector(seed=body.seed).plan(body.brief)
    manifest["quality"] = QualityGate().check(manifest)
    return utils.get_response(200, manifest)

@router.post("/studio/render")
def render_studio(request: Request, body: StudioRenderRequest, background_tasks: BackgroundTasks):
    manifest = QualityGate().revise(body.manifest) if body.self_revise else body.manifest
    task_id = utils.get_uuid(); task_dir = utils.storage_dir(os.path.join("studio", task_id), create=True)
    manifest_path = os.path.join(task_dir, "project.json"); output = os.path.join(task_dir, body.output_name)
    Path(manifest_path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    background_tasks.add_task(_render_job, task_id, manifest, output)
    return utils.get_response(202, {"task_id":task_id,"state":"queued","manifest":manifest_path,"output":output,"quality":manifest.get("quality")})

@router.get("/studio/tasks/{task_id}")
def studio_status(request: Request, task_id: str):
    status_path = os.path.join(utils.storage_dir("studio", create=True), task_id, "status.json")
    if not os.path.exists(status_path): return utils.get_response(404, message="Studio task not found")
    return utils.get_response(200, json.loads(Path(status_path).read_text(encoding="utf-8")))
