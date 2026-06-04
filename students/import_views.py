# students/import_views.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
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
        created = updated = 0

        for _, row in df.iterrows():
            module, _ = Module.objects.get_or_create(
                code_module=row['code_module'],
                code_presentation=row['code_presentation'],
            )
            _, created_flag = Student.objects.update_or_create(
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
            if created_flag:
                created += 1
            else:
                updated += 1

        return Response({
            'message': 'Import étudiants réussi',
            'created': created,
            'updated': updated,
            'total':   created + updated,
        }, status=201)

class ImportAssessmentsView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Aucun fichier fourni.'}, status=400)

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        df = df.where(pd.notna(df), None)
        df.columns = df.columns.str.strip().str.lower()

        required = ['id_student', 'id_assessment', 'score']
        missing  = [c for c in required if c not in df.columns]
        if missing:
            return Response({'error': f'Colonnes manquantes : {missing}'}, status=400)

        # Charger tous les étudiants en mémoire — 1 seule requête DB
        student_map = {
            s.id_student: s
            for s in Student.objects.select_related('module').all()
        }

        # Construire tous les objets en mémoire
        to_create = []
        skipped   = 0

        for _, row in df.iterrows():
            try:
                sid     = int(row['id_student'])
                student = student_map.get(sid)
                if student is None:
                    skipped += 1
                    continue

                score = float(row['score']) if row.get('score') is not None else None

                to_create.append(Assessment(
                    id_assessment   = int(row['id_assessment']),
                    student         = student,
                    module          = student.module,
                    assessment_type = str(row.get('assessment_type', 'TMA')),
                    date_submitted  = int(row['date_submitted']) if row.get('date_submitted') else None,
                    score           = score,
                    is_banked       = bool(int(row.get('is_banked', 0))),
                    weight          = float(row.get('weight', 0)) if row.get('weight') else 0.0,
                ))

            except Exception:
                skipped += 1
                continue

        # Insertion en lots de 5000 — ignore_conflicts gère les doublons
        BATCH         = 5000
        created_count = 0

        for i in range(0, len(to_create), BATCH):
            batch = to_create[i:i + BATCH]
            Assessment.objects.bulk_create(batch, ignore_conflicts=True)
            created_count += len(batch)

        return Response({
            'message': 'Import assessments terminé',
            'created': created_count,
            'skipped': skipped,
            'total':   created_count,
        }, status=201)
        
class ImportVLEView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Aucun fichier fourni.'}, status=400)
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        df = df.where(pd.notna(df), None)
        created = skipped = 0
        batch = []

        for _, row in df.iterrows():
            try:
                student = Student.objects.filter(
                    id_student=int(row['id_student'])
                ).first()
                if student is None:
                    skipped += 1
                    continue

                batch.append(VLEActivity(
                    student=student,
                    module=student.module,
                    id_site=int(row.get('id_site', 0)),
                    activity_type=str(row.get('activity_type', 'resource')),
                    date=int(row.get('date', 0)),
                    sum_click=int(row.get('sum_click', 0)),
                ))

                if len(batch) >= 2000:
                    VLEActivity.objects.bulk_create(
                        batch, ignore_conflicts=True
                    )
                    created += len(batch)
                    batch = []

            except Exception:
                continue

        if batch:
            VLEActivity.objects.bulk_create(batch, ignore_conflicts=True)
            created += len(batch)

        return Response({
            'message': 'Import VLE terminé',
            'created': created,
            'skipped': skipped,
        }, status=201)