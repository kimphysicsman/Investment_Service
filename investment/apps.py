from django.apps import AppConfig
import os

class InvestmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investment'

    def ready(self):
        from investment.scheduler import updater
        if os.environ.get('RUN_MAIN'):
            updater.start()