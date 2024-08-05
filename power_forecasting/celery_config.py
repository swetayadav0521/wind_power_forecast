import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "power_forecasting.settings")

app = Celery("power_forecasting")

app.conf.update(
    worker_concurrency=4,  # Number of concurrent worker processes/threads
)

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
