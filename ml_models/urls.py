# ml_models/urls.py
from django.urls import path
from .views import TrainModelView, PredictStudentView, ModelInfoView, BulkPredictView

urlpatterns = [
    path('train/',                        TrainModelView.as_view(),   name='train-model'),
    path('info/',                         ModelInfoView.as_view(),    name='model-info'),
    path('predict/<int:student_id>/',     PredictStudentView.as_view(), name='predict-student'),
    path('predict-all/',                  BulkPredictView.as_view(),  name='bulk-predict'),
]