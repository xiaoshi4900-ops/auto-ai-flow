from app.tasks.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task
def on_workflow_success(sender=None, result=None, **kwargs):
    logger.info(f"Workflow succeeded: {result}")


@celery_app.task
def on_workflow_failure(sender=None, exc=None, **kwargs):
    logger.error(f"Workflow failed: {exc}")
