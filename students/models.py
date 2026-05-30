# students/models.py
from django.db import models


class Module(models.Model):
    code_module = models.CharField(max_length=10)
    code_presentation = models.CharField(max_length=10)
    module_presentation_length = models.IntegerField(default=0)

    class Meta:
        unique_together = ('code_module', 'code_presentation')

    def __str__(self):
        return f"{self.code_module} - {self.code_presentation}"


class Student(models.Model):
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('Distinction', 'Distinction'),
        ('Withdrawn', 'Withdrawn'),
    ]

    id_student       = models.IntegerField(unique=True)
    gender           = models.CharField(max_length=1)
    region           = models.CharField(max_length=100)
    highest_education = models.CharField(max_length=100)
    imd_band         = models.CharField(max_length=20, blank=True, null=True)
    age_band         = models.CharField(max_length=20)
    num_of_prev_attempts = models.IntegerField(default=0)
    studied_credits  = models.IntegerField(default=0)
    disability       = models.CharField(max_length=1, default='N')
    final_result     = models.CharField(max_length=20, choices=RESULT_CHOICES, blank=True, null=True)
    module           = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f"Student {self.id_student}"


class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ('TMA', 'Tutor Marked Assessment'),
        ('CMA', 'Computer Marked Assessment'),
        ('Exam', 'Exam'),
    ]

    id_assessment    = models.IntegerField(unique=True)
    student          = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assessments')
    module           = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessments')
    assessment_type  = models.CharField(max_length=10, choices=ASSESSMENT_TYPES)
    date_submitted   = models.IntegerField(null=True, blank=True)
    score            = models.FloatField(null=True, blank=True)
    weight           = models.FloatField(default=0)
    is_banked        = models.BooleanField(default=False)

    def __str__(self):
        return f"Assessment {self.id_assessment} — Student {self.student.id_student}"


class VLEActivity(models.Model):
    student          = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='vle_activities')
    module           = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='vle_activities')
    id_site          = models.IntegerField()
    activity_type    = models.CharField(max_length=50)
    date             = models.IntegerField()
    sum_click        = models.IntegerField(default=0)

    def __str__(self):
        return f"VLE {self.activity_type} — Student {self.student.id_student}"