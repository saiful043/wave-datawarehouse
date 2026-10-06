# apps/etl_engine/apps.py
from django.apps import AppConfig

class EtlEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.etl_engine'