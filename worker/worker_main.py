import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.tasks.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()
