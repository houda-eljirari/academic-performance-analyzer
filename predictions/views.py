# predictions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import Prediction
from students.models import Student


class PredictionSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id_student', read_only=True)

    class Meta:
        model = Prediction
        fields = ['id', 'student_id', 'result', 'probability',
                  'risk_level', 'shap_values', 'predicted_at']


class AllPredictionsView(APIView):
    """GET /api/predictions/ — toutes les prédictions existantes"""

    def get(self, request):
        risk   = request.query_params.get('risk_level')
        result = request.query_params.get('result')

        qs = Prediction.objects.select_related('student').all()

        if risk:
            qs = qs.filter(risk_level=risk)
        if result:
            qs = qs.filter(result=result)

        qs = qs.order_by('-probability')

        data = [{
            'student_id':  p.student.id_student,
            'result':      p.result,
            'probability': round(p.probability, 4),
            'risk_level':  p.risk_level,
            'predicted_at': p.predicted_at,
            'top_features': dict(list(p.shap_values.items())[:5])
                            if isinstance(p.shap_values, dict) else {},
        } for p in qs]

        return Response({
            'count': len(data),
            'predictions': data,
        })


class StudentPredictionDetailView(APIView):
    """GET /api/predictions/student/<id>/ — prédiction détaillée d'un étudiant"""

    def get(self, request, student_id):
        try:
            student    = Student.objects.get(id_student=student_id)
            prediction = Prediction.objects.get(student=student)
        except Student.DoesNotExist:
            return Response({'error': 'Étudiant introuvable.'}, status=404)
        except Prediction.DoesNotExist:
            return Response({'error': 'Aucune prédiction pour cet étudiant. Lancez POST /api/ml/predict/{id}/'}, status=404)

        shap = prediction.shap_values
        positive_features = {k: v for k, v in shap.items() if isinstance(v, float) and v > 0}
        negative_features = {k: v for k, v in shap.items() if isinstance(v, float) and v < 0}

        return Response({
            'student_id':        student_id,
            'result':            prediction.result,
            'probability':       round(prediction.probability, 4),
            'probability_fail':  round(1 - prediction.probability, 4),
            'risk_level':        prediction.risk_level,
            'predicted_at':      prediction.predicted_at,
            'shap_values':       shap,
            'positive_factors':  dict(sorted(positive_features.items(), key=lambda x: x[1], reverse=True)[:5]),
            'negative_factors':  dict(sorted(negative_features.items(), key=lambda x: x[1])[:5]),
        })


class RiskSummaryView(APIView):
    """GET /api/predictions/risk-summary/ — résumé global des niveaux de risque"""

    def get(self, request):
        from django.db.models import Count, Avg

        summary = Prediction.objects.values('risk_level').annotate(
            count=Count('id'),
            avg_probability=Avg('probability'),
        )

        total = Prediction.objects.count()

        data = {
            item['risk_level']: {
                'count':           item['count'],
                'percentage':      round(item['count'] / total * 100, 2) if total else 0,
                'avg_probability': round(item['avg_probability'], 4),
            }
            for item in summary
        }

        return Response({
            'total_predicted': total,
            'summary': data,
        })

from .recommendations import generate_recommendations

class StudentRecommendationsView(APIView):
    """GET /api/predictions/student/<id>/recommendations/ — recommandations personnalisées"""

    def get(self, request, student_id):
        try:
            student    = Student.objects.get(id_student=student_id)
            prediction = Prediction.objects.get(student=student)
        except Student.DoesNotExist:
            return Response({'error': 'Étudiant introuvable.'}, status=404)
        except Prediction.DoesNotExist:
            return Response({
                'error': 'Aucune prédiction disponible. Lancez d\'abord POST /api/ml/predict/{id}/'
            }, status=404)

        recommendations = generate_recommendations(
            shap_values=prediction.shap_values,
            risk_level=prediction.risk_level,
        )

        return Response({
            'student_id':      student_id,
            'risk_level':      prediction.risk_level,
            'result':          prediction.result,
            'probability':     round(prediction.probability, 4),
            'recommendations': recommendations,
            'total':           len(recommendations),
        })