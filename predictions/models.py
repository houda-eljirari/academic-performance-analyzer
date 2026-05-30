# predictions/models.py
from django.db import models
from students.models import Student


class Prediction(models.Model):
    RISK_CHOICES = [
        ('LOW',    'Faible'),
        ('MEDIUM', 'Moyen'),
        ('HIGH',   'Élevé'),
    ]

    student      = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='prediction')
    result       = models.CharField(max_length=20)
    probability  = models.FloatField()
    risk_level   = models.CharField(max_length=10, choices=RISK_CHOICES)
    shap_values  = models.JSONField(default=dict)
    predicted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prediction({self.student.id_student}) → {self.result} [{self.risk_level}]"