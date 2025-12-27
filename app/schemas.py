from pydantic import BaseModel

class PipelineMetrics(BaseModel):
    """
    Pipeline metrics aligned EXACTLY with model training features.
    """
    total_tasks: int
    is_production: int
    failed_tasks: int
    stage_count: int
    task_failure_rate: float
    project_age_days: int
    days_since_last_push: int
    stars_to_forks_ratio: float
    build_tool_count: int
    uses_legacy_build: int
    uses_multiple_ides: int
    uses_ci_and_submodules: int
    avg_file_churn: float
    new_file_ratio: float
    dependency_error_rate: float
    compiler_error_rate: float


class RiskResponse(BaseModel):
    risk_score: float
    decision: str
