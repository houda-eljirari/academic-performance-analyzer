# ml_models/management/commands/train_model.py
from django.core.management.base import BaseCommand
from ml_models.train import train_and_save
import json


class Command(BaseCommand):
    help = 'Entraîne le modèle ML Random Forest sur les données OULAD importées'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n Démarrage de l\'entraînement...\n'))

        metrics = train_and_save()

        if 'error' in metrics:
            self.stdout.write(self.style.ERROR(f"\n Erreur : {metrics['error']}"))
            return

        self.stdout.write(self.style.SUCCESS('\n Modèle entraîné avec succès !\n'))
        self.stdout.write(f"  Accuracy  : {metrics['accuracy']}")
        self.stdout.write(f"  F1 Score  : {metrics['f1_score']}")
        self.stdout.write(f"  Precision : {metrics['precision']}")
        self.stdout.write(f"  Recall    : {metrics['recall']}")
        self.stdout.write(f"  CV F1     : {metrics['cv_mean_f1']} ± {metrics['cv_std']}")
        self.stdout.write(f"\n  Top features :")
        for feat, imp in list(metrics['feature_importance'].items())[:5]:
            bar = '█' * int(imp * 40)
            self.stdout.write(f"    {feat:<25} {bar} {imp}")