"""Preflight cost/resource governance. Estimates are intentionally provider-neutral."""
from dataclasses import dataclass

@dataclass
class ResourceEstimate:
    gpu_minutes: float = 0.0
    api_cost: float = 0.0
    storage_mb: float = 0.0
    render_minutes: float = 0.0

class BudgetGuard:
    def __init__(self, max_api_cost: float | None=None, max_gpu_minutes: float | None=None):
        self.max_api_cost=max_api_cost; self.max_gpu_minutes=max_gpu_minutes
    def check(self, estimate: ResourceEstimate) -> dict:
        failures=[]
        if self.max_api_cost is not None and estimate.api_cost > self.max_api_cost: failures.append("api_cost")
        if self.max_gpu_minutes is not None and estimate.gpu_minutes > self.max_gpu_minutes: failures.append("gpu_minutes")
        return {"ok": not failures, "failures": failures, "estimate": estimate.__dict__}
