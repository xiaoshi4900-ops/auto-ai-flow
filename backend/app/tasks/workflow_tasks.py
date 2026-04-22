from app.tasks.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(bind=True, max_retries=3)
def execute_workflow(self, workflow_run_id: int):
    from app.db.session import SessionLocal
    from app.runtime.workflow_executor import WorkflowExecutor

    db = SessionLocal()
    try:
        executor = WorkflowExecutor(db)
        result = executor.execute(workflow_run_id)
        logger.info(f"Workflow execution completed: {result}")
        return result
    except Exception as e:
        logger.exception(f"Workflow execution failed for run {workflow_run_id}")
        raise self.retry(exc=e, countdown=10)
    finally:
        db.close()
