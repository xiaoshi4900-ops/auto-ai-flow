from app.tasks.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task
def cleanup_old_runs(days: int = 30):
    logger.info(f"Cleaning up runs older than {days} days")
