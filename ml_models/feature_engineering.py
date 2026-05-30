# ml_models/feature_engineering.py
import pandas as pd
import numpy as np
from django.db.models import Avg, Sum, Count
from students.models import Student, Assessment, VLEActivity


def extract_features_from_db():
    """
    Extrait et construit le DataFrame de features
    à partir de la base de données pour entraîner le modèle.
    Retourne X (features) et y (labels).
    """
    students = Student.objects.exclude(
        final_result__isnull=True
    ).exclude(final_result='').select_related('module')

    records = []

    for s in students:
        assessments = Assessment.objects.filter(student=s)
        vle         = VLEActivity.objects.filter(student=s)

        avg_score      = assessments.aggregate(v=Avg('score'))['v'] or 0
        max_score      = assessments.order_by('-score').values_list('score', flat=True).first() or 0
        min_score      = assessments.order_by('score').values_list('score', flat=True).first() or 0
        nb_assessments = assessments.count()
        nb_tma         = assessments.filter(assessment_type='TMA').count()
        nb_cma         = assessments.filter(assessment_type='CMA').count()
        total_clicks   = vle.aggregate(v=Sum('sum_click'))['v'] or 0
        nb_vle_types   = vle.values('activity_type').distinct().count()
        nb_vle_days    = vle.values('date').distinct().count()

        records.append({
            'id_student':         s.id_student,
            'gender':             1 if s.gender == 'M' else 0,
            'disability':         1 if s.disability == 'Y' else 0,
            'num_prev_attempts':  s.num_of_prev_attempts,
            'studied_credits':    s.studied_credits,
            'age_band':           s.age_band,
            'highest_education':  s.highest_education,
            'imd_band':           s.imd_band or 'Unknown',
            'avg_score':          round(avg_score, 2),
            'max_score':          round(float(max_score), 2),
            'min_score':          round(float(min_score), 2),
            'nb_assessments':     nb_assessments,
            'nb_tma':             nb_tma,
            'nb_cma':             nb_cma,
            'total_clicks':       total_clicks,
            'nb_vle_types':       nb_vle_types,
            'nb_vle_days':        nb_vle_days,
            'final_result':       s.final_result,
        })

    df = pd.DataFrame(records)
    return df


def preprocess(df, label_encoders=None, fit=True):
    """
    Encode les variables catégorielles et retourne X, y.
    Si fit=True  → construit les encoders (phase entraînement).
    Si fit=False → réutilise les encoders existants (phase prédiction).
    """
    from sklearn.preprocessing import LabelEncoder

    cat_cols = ['age_band', 'highest_education', 'imd_band']

    if fit:
        label_encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
    else:
        for col in cat_cols:
            le = label_encoders[col]
            df[col] = df[col].astype(str).map(
                lambda x: le.transform([x])[0]
                if x in le.classes_ else -1
            )

    # Binariser la cible : Pass/Distinction = 1, Fail/Withdrawn = 0
    if 'final_result' in df.columns:
        df['label'] = df['final_result'].apply(
            lambda r: 1 if r in ['Pass', 'Distinction'] else 0
        )

    feature_cols = [
        'gender', 'disability', 'num_prev_attempts', 'studied_credits',
        'age_band', 'highest_education', 'imd_band',
        'avg_score', 'max_score', 'min_score',
        'nb_assessments', 'nb_tma', 'nb_cma',
        'total_clicks', 'nb_vle_types', 'nb_vle_days',
    ]

    X = df[feature_cols].fillna(0)
    y = df['label'] if 'label' in df.columns else None

    return X, y, label_encoders, feature_cols


def extract_features_for_student(student_id, label_encoders, feature_cols):
    """
    Extrait les features d'un seul étudiant pour la prédiction.
    """
    try:
        s = Student.objects.get(id_student=student_id)
    except Student.DoesNotExist:
        return None, "Étudiant introuvable"

    assessments = Assessment.objects.filter(student=s)
    vle         = VLEActivity.objects.filter(student=s)

    avg_score      = assessments.aggregate(v=Avg('score'))['v'] or 0
    max_score      = assessments.order_by('-score').values_list('score', flat=True).first() or 0
    min_score      = assessments.order_by('score').values_list('score', flat=True).first() or 0
    nb_assessments = assessments.count()
    total_clicks   = vle.aggregate(v=Sum('sum_click'))['v'] or 0
    nb_vle_types   = vle.values('activity_type').distinct().count()
    nb_vle_days    = vle.values('date').distinct().count()

    from sklearn.preprocessing import LabelEncoder
    def encode_cat(col, val):
        le = label_encoders.get(col)
        if le is None:
            return 0
        val = str(val)
        return int(le.transform([val])[0]) if val in le.classes_ else -1

    record = {
        'gender':             1 if s.gender == 'M' else 0,
        'disability':         1 if s.disability == 'Y' else 0,
        'num_prev_attempts':  s.num_of_prev_attempts,
        'studied_credits':    s.studied_credits,
        'age_band':           encode_cat('age_band', s.age_band),
        'highest_education':  encode_cat('highest_education', s.highest_education),
        'imd_band':           encode_cat('imd_band', s.imd_band or 'Unknown'),
        'avg_score':          round(avg_score, 2),
        'max_score':          round(float(max_score), 2),
        'min_score':          round(float(min_score), 2),
        'nb_assessments':     nb_assessments,
        'nb_tma':             assessments.filter(assessment_type='TMA').count(),
        'nb_cma':             assessments.filter(assessment_type='CMA').count(),
        'total_clicks':       total_clicks,
        'nb_vle_types':       nb_vle_types,
        'nb_vle_days':        nb_vle_days,
    }

    df_row = pd.DataFrame([record])[feature_cols].fillna(0)
    return df_row, None