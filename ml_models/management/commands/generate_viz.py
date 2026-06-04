# ml_models/management/commands/generate_viz.py
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Génère toutes les visualisations ML du modèle AcademiX'

    def handle(self, *args, **kwargs):
        from ml_models.generate_visualizations import generate_all
        generate_all()
        self.stdout.write(
            self.style.SUCCESS('\nVisualisations générées dans ml_models/visualizations/')
        )