# analytics/urls.py
from django.urls import path
from .views import (
    GlobalStatsView,
    ResultDistributionView,
    ModuleStatsView,
    VLEActivityStatsView,
    AssessmentStatsView,
    StudentProfileView,
)

urlpatterns = [
    path('stats/',                          GlobalStatsView.as_view(),        name='global-stats'),
    path('distribution/',                   ResultDistributionView.as_view(), name='distribution'),
    path('by-module/',                      ModuleStatsView.as_view(),        name='module-stats'),
    path('vle-activity/',                   VLEActivityStatsView.as_view(),   name='vle-stats'),
    path('assessments/',                    AssessmentStatsView.as_view(),    name='assessment-stats'),
    path('students/<int:student_id>/profile/', StudentProfileView.as_view(), name='student-profile'),
]