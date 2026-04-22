from sqlalchemy.orm import Session

from app.db.models.run import RunArtifact
from app.schemas.execution import RunResponse


class ArtifactService:
    def __init__(self, db: Session):
        self.db = db

    def list_by_run(self, run_id: int) -> list[RunArtifact]:
        return self.db.query(RunArtifact).filter(RunArtifact.workflow_run_id == run_id).all()

    def create(self, workflow_run_id: int, node_key: str, artifact_type: str, name: str, content: dict | None = None) -> RunArtifact:
        artifact = RunArtifact(workflow_run_id=workflow_run_id, node_key=node_key, artifact_type=artifact_type, name=name, content=content)
        self.db.add(artifact)
        self.db.commit()
        self.db.refresh(artifact)
        return artifact
