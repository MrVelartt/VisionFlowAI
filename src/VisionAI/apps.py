# VisionAI/apps.py
from django.apps import AppConfig

class VisionAiConfig(AppConfig):
    name = 'VisionAI'

    def ready(self):
        # Importar el módulo signals para que se registre el receptor
        import VisionAI.signals
