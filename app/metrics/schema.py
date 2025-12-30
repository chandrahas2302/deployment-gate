from pydantic import BaseModel

class PipelineContext(BaseModel):
    repo: str              # owner/repo
    sha: str
    run_id: str
    branch: str

