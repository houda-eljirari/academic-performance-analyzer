# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum, Q, FloatField
from django.db.models.functions import Cast
import pandas as pd

from students.models import Student, Assessment, VLEActivity, Module


class GlobalStatsView(APIView):
    """GET /api/analytics/stats/ — statistiques globales"""

    def get(self, request):
        total = Student.objects.count()
        if total == 0:
            return Response({'error': 'Aucune donnée disponible.'})

        results = Student.objects.values('final_result').annotate(
            count=Count('id')
        )
        result_dist = {r['final_result']: r['count'] for r in results}

        avg_credits = Student.objects.aggregate(
            avg=Avg('studied_credits')
        )['avg'] or 0

        avg_attempts = Student.objects.aggregate(
            avg=Avg('num_of_prev_attempts')
        )['avg'] or 0

        disabled_count = Student.objects.filter(disability='Y').count()

        return Response({
            'total_students':       total,
            'result_distribution':  result_dist,
            'pass_rate':            round((result_dist.get('Pass', 0) + result_dist.get('Distinction', 0)) / total * 100, 2),
            'fail_rate':            round(result_dist.get('Fail', 0) / total * 100, 2),
            'withdrawn_rate':       round(result_dist.get('Withdrawn', 0) / total * 100, 2),
            'avg_studied_credits':  round(avg_credits, 2),
            'avg_prev_attempts':    round(avg_attempts, 2),
            'disabled_students':    disabled_count,
        })


class ResultDistributionView(APIView):
    """GET /api/analytics/distribution/ — distribution par tranche d'âge, genre, région"""

    def get(self, request):
        by_age = list(
            Student.objects.values('age_band')
            .annotate(count=Count('id'))
            .order_by('age_band')
        )

        by_gender = list(
            Student.objects.values('gender')
            .annotate(count=Count('id'))
        )

        by_region = list(
            Student.objects.values('region')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        by_education = list(
            Student.objects.values('highest_education')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            'by_age_band':   by_age,
            'by_gender':     by_gender,
            'by_region':     by_region,
            'by_education':  by_education,
        })


class ModuleStatsView(APIView):
    """GET /api/analytics/by-module/ — stats par module"""

    def get(self, request):
        modules = Module.objects.annotate(
            total_students=Count('students'),
            pass_count=Count(
                'students',
                filter=Q(students__final_result__in=['Pass', 'Distinction'])
            ),
            fail_count=Count(
                'students',
                filter=Q(students__final_result='Fail')
            ),
            withdrawn_count=Count(
                'students',
                filter=Q(students__final_result='Withdrawn')
            ),
            avg_score=Avg('assessments__score'),
        )

        data = []
        for m in modules:
            total = m.total_students or 1
            data.append({
                'code_module':        m.code_module,
                'code_presentation':  m.code_presentation,
                'total_students':     m.total_students,
                'pass_rate':          round(m.pass_count / total * 100, 2),
                'fail_rate':          round(m.fail_count / total * 100, 2),
                'withdrawn_rate':     round(m.withdrawn_count / total * 100, 2),
                'avg_score':          round(m.avg_score or 0, 2),
            })

        return Response({'modules': data})


class VLEActivityStatsView(APIView):
    """GET /api/analytics/vle-activity/ — engagement VLE global et par type"""

    def get(self, request):
        by_type = list(
            VLEActivity.objects.values('activity_type')
            .annotate(
                total_clicks=Sum('sum_click'),
                count=Count('id'),
            )
            .order_by('-total_clicks')
        )

        by_week = list(
            VLEActivity.objects.values('date')
            .annotate(total_clicks=Sum('sum_click'))
            .order_by('date')[:52]
        )

        top_students = list(
            VLEActivity.objects.values('student__id_student')
            .annotate(total_clicks=Sum('sum_click'))
            .order_by('-total_clicks')[:10]
        )

        return Response({
            'by_activity_type': by_type,
            'weekly_clicks':    by_week,
            'top_students':     top_students,
        })


class AssessmentStatsView(APIView):
    """GET /api/analytics/assessments/ — stats des évaluations"""

    def get(self, request):
        by_type = list(
            Assessment.objects.values('assessment_type')
            .annotate(
                count=Count('id'),
                avg_score=Avg('score'),
            )
        )

        score_ranges = {
            '0-20':   Assessment.objects.filter(score__gte=0,  score__lt=20).count(),
            '20-40':  Assessment.objects.filter(score__gte=20, score__lt=40).count(),
            '40-60':  Assessment.objects.filter(score__gte=40, score__lt=60).count(),
            '60-80':  Assessment.objects.filter(score__gte=60, score__lt=80).count(),
            '80-100': Assessment.objects.filter(score__gte=80, score__lte=100).count(),
        }

        global_avg = Assessment.objects.aggregate(
            avg=Avg('score')
        )['avg'] or 0

        return Response({
            'by_type':      by_type,
            'score_ranges': score_ranges,
            'global_avg':   round(global_avg, 2),
        })


class StudentProfileView(APIView):
    """GET /api/analytics/students/<id>/profile/ — profil analytique complet"""

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id_student=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Étudiant introuvable.'}, status=404)

        assessments = Assessment.objects.filter(student=student)
        vle         = VLEActivity.objects.filter(student=student)

        avg_score     = assessments.aggregate(avg=Avg('score'))['avg'] or 0
        total_clicks  = vle.aggregate(total=Sum('sum_click'))['total'] or 0
        nb_assessments = assessments.count()

        assessments_by_type = list(
            assessments.values('assessment_type')
            .annotate(avg_score=Avg('score'), count=Count('id'))
        )

        weekly_activity = list(
            vle.values('date')
            .annotate(clicks=Sum('sum_click'))
            .order_by('date')
        )

        activity_by_type = list(
            vle.values('activity_type')
            .annotate(total_clicks=Sum('sum_click'))
            .order_by('-total_clicks')
        )

        engagement_score = min(100, round(total_clicks / 100, 1))

        return Response({
            'student': {
                'id_student':        student.id_student,
                'gender':            student.gender,
                'region':            student.region,
                'age_band':          student.age_band,
                'disability':        student.disability,
                'studied_credits':   student.studied_credits,
                'prev_attempts':     student.num_of_prev_attempts,
                'final_result':      student.final_result,
                'module':            str(student.module),
            },
            'performance': {
                'avg_score':         round(avg_score, 2),
                'nb_assessments':    nb_assessments,
                'total_vle_clicks':  total_clicks,
                'engagement_score':  engagement_score,
                'assessments_by_type': assessments_by_type,
            },
            'activity': {
                'weekly_clicks':     weekly_activity,
                'by_activity_type':  activity_by_type,
            },
        })
        