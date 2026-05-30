# students/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count
import pandas as pd

from .models import Student, Module, Assessment, VLEActivity
from .serializers import (
    StudentSerializer, StudentDetailSerializer,
    ModuleSerializer, AssessmentSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('module').all()
    serializer_class = StudentSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['final_result', 'gender', 'disability', 'age_band']
    search_fields    = ['id_student', 'region']
    ordering_fields  = ['id_student', 'studied_credits']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StudentDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='at-risk')
    def at_risk(self, request):
        """Retourne les étudiants dont la prédiction indique un risque élevé."""
        from predictions.models import Prediction
        threshold = float(request.query_params.get('threshold', 0.7))
        risky = Prediction.objects.filter(
            probability__gte=threshold
        ).select_related('student').order_by('-probability')

        data = [{
            'student_id':  p.student.id_student,
            'result':      p.result,
            'probability': round(p.probability, 3),
            'risk_level':  p.risk_level,
        } for p in risky]
        return Response({'count': len(data), 'students': data})


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer