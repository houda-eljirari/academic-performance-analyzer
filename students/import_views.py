# students/import_views.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Student, Module, Assessment, VLEActivity


class ImportStudentsView(APIView):
    parser_classes = [MultiPartParser]

    @transaction.atomic
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Aucun fichier fourni.'}, status=400)

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response({'error': f'Fichier invalide : {str(e)}'}, status=400)

        required_cols = ['id_student', 'gender', 'region', 'age_band',
                         'num_of_prev_attempts', 'studied_credits',
                         'disability', 'final_result',
                         'code_module', 'code_presentation']

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            return Response({'error': f'Colonnes manquantes : {missing}'}, status=400)

        df = df.where(pd.notna(df), None)
        created_count = 0
        updated_count = 0

        for _, row in df.iterrows():
            module, _ = Module.objects.get_or_create(
                code_module=row['code_module'],
                code_presentation=row['code_presentation'],
            )
            student, created = Student.objects.update_or_create(
                id_student=int(row['id_student']),
                defaults={
                    'gender':               row.get('gender', ''),
                    'region':               row.get('region', ''),
                    'highest_education':    row.get('highest_education', ''),
                    'imd_band':             row.get('imd_band'),
                    'age_band':             row.get('age_band', ''),
                    'num_of_prev_attempts': int(row.get('num_of_prev_attempts', 0)),
                    'studied_credits':      int(row.get('studied_credits', 0)),
                    'disability':           row.get('disability', 'N'),
                    'final_result':         row.get('final_result'),
                    'module':               module,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        return Response({
            'message': 'Import réussi',
            'created': created_count,
            'updated': updated_count,
            'total':   created_count + updated_count,
        }, status=201)