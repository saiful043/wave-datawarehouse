import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# namespace='CELERY' দেওয়ার কারণে settings.py-এর CELERY_ প্রিফিক্স যুক্ত সব কনফিগারেশন রিড করবে
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()