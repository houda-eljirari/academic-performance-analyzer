# predictions/urls.py
from django.urls import path
from .views import (
    AllPredictionsView,
    StudentPredictionDetailView,
    RiskSummaryView,
    StudentRecommendationsView,
)

urlpatterns = [
    path('',                                       AllPredictionsView.as_view(),          name='all-predictions'),
    path('student/<int:student_id>/',              StudentPredictionDetailView.as_view(), name='student-prediction'),
    path('risk-summary/',                          RiskSummaryView.as_view(),             name='risk-summary'),
    path('student/<int:student_id>/recommendations/', StudentRecommendationsView.as_view(), name='student-recommendations'),
]