# ml_models/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .train import train_and_save
from .predictor import predict_student, get_model_info


class TrainModelView(APIView):
    """POST /api/ml/train/ — lance l'entraînement du modèle"""

    def post(self, request):
        metrics = train_and_save()
        if 'error' in metrics:
            return Response(metrics, status=400)
        return Response({
            'message': 'Modèle entraîné avec succès',
            'metrics': metrics,
        })


class PredictStudentView(APIView):
    """POST /api/ml/predict/<student_id>/ — prédit le résultat d'un étudiant"""

    def post(self, request, student_id):
        result = predict_student(student_id)
        if 'error' in result:
            return Response(result, status=404)

        from predictions.models import Prediction
        from students.models import Student
        try:
            student = Student.objects.get(id_student=student_id)
            Prediction.objects.update_or_create(
                student=student,
                defaults={
                    'result':      result['result'],
                    'probability': result['probability'],
                    'risk_level':  result['risk_level'],
                    'shap_values': result['shap_values'],
                }
            )
        except Student.DoesNotExist:
            pass

        return Response(result)


class ModelInfoView(APIView):
    """GET /api/ml/info/ — infos sur le modèle chargé"""

    def get(self, request):
        return Response(get_model_info())


class BulkPredictView(APIView):
    """POST /api/ml/predict-all/ — prédit tous les étudiants sans prédiction"""

    def post(self, request):
        from students.models import Student
        from predictions.models import Prediction

        already_predicted = Prediction.objects.values_list(
            'student__id_student', flat=True
        )
        students = Student.objects.exclude(
            id_student__in=already_predicted
        ).values_list('id_student', flat=True)

        results = {'success': 0, 'errors': 0, 'details': []}

        for sid in students:
            res = predict_student(sid)
            if 'error' in res:
                results['errors'] += 1
            else:
                results['success'] += 1
                results['details'].append({
                    'student_id': sid,
                    'result':     res['result'],
                    'risk_level': res['risk_level'],
                })

        return Response(results)