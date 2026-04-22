from sqlalchemy.orm import Session

from app.db.models.code_task import CodeTask


class CodeRuntimeService:
    def create_code_task_if_absent(self, db_session: Session, workflow_run, node_run, agent, task_goal: str) -> CodeTask | None:
        existing = db_session.query(CodeTask).filter(
            CodeTask.workflow_run_id == workflow_run.id,
            CodeTask.node_run_id == node_run.id,
        ).first()
        if existing:
            return existing

        task = CodeTask(
            workflow_run_id=workflow_run.id,
            node_run_id=node_run.id,
            agent_id=agent.id,
            task_goal=task_goal,
            status="running",
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task
