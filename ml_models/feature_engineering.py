# ml_models/feature_engineering.py
import pandas as pd
import numpy as np
from django.db.models import Avg, Sum, Count
from students.models import Student, Assessment, VLEActivity


def extract_features_from_db():
    from django.db.models import Avg, Sum, Count, Max, Min, StdDev
    from students.models import Student, Assessment, VLEActivity

    students = Student.objects.exclude(
        final_result__isnull=True
    ).exclude(final_result='').select_related('module')

    records = []

    for s in students:
        assessments = Assessment.objects.filter(student=s)
        vle         = VLEActivity.objects.filter(student=s)

        # ── Features Assessment ──────────────────────────
        agg_a = assessments.aggregate(
            avg_score=Avg('score'),
            max_score=Max('score'),
            min_score=Min('score'),
            count=Count('id'),
        )
        avg_score      = agg_a['avg_score'] or 0
        max_score      = agg_a['max_score'] or 0
        min_score      = agg_a['min_score'] or 0
        nb_assessments = agg_a['count'] or 0
        nb_tma         = assessments.filter(assessment_type='TMA').count()
        nb_cma         = assessments.filter(assessment_type='CMA').count()
        nb_exam        = assessments.filter(assessment_type='Exam').count()

        # Score pondéré par le poids
        weighted_score = 0
        total_weight   = 0
        for a in assessments:
            if a.score is not None and a.weight:
                weighted_score += a.score * a.weight
                total_weight   += a.weight
        weighted_avg = (weighted_score / total_weight) if total_weight > 0 else 0

        # Taux de soumission (assessments soumis vs total)
        submitted = assessments.filter(
            date_submitted__isnull=False
        ).count()
        submission_rate = (submitted / nb_assessments) if nb_assessments > 0 else 0

        # ── Features VLE ─────────────────────────────────
        agg_v = vle.aggregate(
            total_clicks=Sum('sum_click'),
            nb_types=Count('activity_type', distinct=True),
            nb_days=Count('date', distinct=True),
        )
        total_clicks  = agg_v['total_clicks'] or 0
        nb_vle_types  = agg_v['nb_types'] or 0
        nb_vle_days   = agg_v['nb_days'] or 0

        # Clics par jour actif
        clicks_per_day = (total_clicks / nb_vle_days) if nb_vle_days > 0 else 0

        # Engagement sur les quiz et forums
        quiz_clicks  = vle.filter(activity_type='quiz').aggregate(
            v=Sum('sum_click'))['v'] or 0
        forum_clicks = vle.filter(activity_type='forumng').aggregate(
            v=Sum('sum_click'))['v'] or 0

        records.append({
            'id_student':        s.id_student,
            # Démographiques
            'gender':            1 if s.gender == 'M' else 0,
            'disability':        1 if s.disability == 'Y' else 0,
            'num_prev_attempts': s.num_of_prev_attempts,
            'studied_credits':   s.studied_credits,
            'age_band':          s.age_band,
            'highest_education': s.highest_education,
            'imd_band':          s.imd_band or 'Unknown',
            # Assessment
            'avg_score':         round(avg_score, 2),
            'max_score':         round(float(max_score), 2),
            'min_score':         round(float(min_score), 2),
            'weighted_avg':      round(weighted_avg, 2),
            'nb_assessments':    nb_assessments,
            'nb_tma':            nb_tma,
            'nb_cma':            nb_cma,
            'nb_exam':           nb_exam,
            'submission_rate':   round(submission_rate, 3),
            # VLE
            'total_clicks':      total_clicks,
            'nb_vle_types':      nb_vle_types,
            'nb_vle_days':       nb_vle_days,
            'clicks_per_day':    round(clicks_per_day, 2),
            'quiz_clicks':       quiz_clicks,
            'forum_clicks':      forum_clicks,
            # Cible
            'final_result':      s.final_result,
        })

    return pd.DataFrame(records)

def preprocess(df, label_encoders=None, fit=True):
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
                lambda x, le=le: int(le.transform([x])[0])
                if x in le.classes_ else -1
            )

    if 'final_result' in df.columns:
        df['label'] = df['final_result'].apply(
            lambda r: 1 if r in ['Pass', 'Distinction'] else 0
        )

    # 23 features maintenant
    feature_cols = [
        'gender', 'disability', 'num_prev_attempts', 'studied_credits',
        'age_band', 'highest_education', 'imd_band',
        'avg_score', 'max_score', 'min_score', 'weighted_avg',
        'nb_assessments', 'nb_tma', 'nb_cma', 'nb_exam',
        'submission_rate',
        'total_clicks', 'nb_vle_types', 'nb_vle_days',
        'clicks_per_day', 'quiz_clicks', 'forum_clicks',
    ]

    # Garder seulement les colonnes existantes
    feature_cols = [f for f in feature_cols if f in df.columns]

    X = df[feature_cols].fillna(0)
    y = df['label'] if 'label' in df.columns else None

    return X, y, label_encoders, feature_cols

def extract_features_for_student(student_id, label_encoders, feature_cols):
    """
    Extrait les features d'un seul étudiant pour la prédiction.
    """
    from django.db.models import Avg, Sum, Count, Max, Min
    from students.models import Student, Assessment, VLEActivity

    try:
        s = Student.objects.get(id_student=student_id)
    except Student.DoesNotExist:
        return None, f"Étudiant {student_id} introuvable"

    assessments = Assessment.objects.filter(student=s)
    vle         = VLEActivity.objects.filter(student=s)

    # ── Features Assessment ──────────────────────────────
    agg_a = assessments.aggregate(
        avg_score=Avg('score'),
        max_score=Max('score'),
        min_score=Min('score'),
        count=Count('id'),
    )
    avg_score      = agg_a['avg_score'] or 0
    max_score      = agg_a['max_score'] or 0
    min_score      = agg_a['min_score'] or 0
    nb_assessments = agg_a['count'] or 0
    nb_tma         = assessments.filter(assessment_type='TMA').count()
    nb_cma         = assessments.filter(assessment_type='CMA').count()
    nb_exam        = assessments.filter(assessment_type='Exam').count()

    # Score pondéré
    weighted_score = 0
    total_weight   = 0
    for a in assessments:
        if a.score is not None and a.weight:
            weighted_score += a.score * a.weight
            total_weight   += a.weight
    weighted_avg = (weighted_score / total_weight) if total_weight > 0 else 0

    # Taux de soumission
    submitted       = assessments.filter(date_submitted__isnull=False).count()
    submission_rate = (submitted / nb_assessments) if nb_assessments > 0 else 0

    # ── Features VLE ─────────────────────────────────────
    agg_v = vle.aggregate(
        total_clicks=Sum('sum_click'),
        nb_types=Count('activity_type', distinct=True),
        nb_days=Count('date', distinct=True),
    )
    total_clicks  = agg_v['total_clicks'] or 0
    nb_vle_types  = agg_v['nb_types'] or 0
    nb_vle_days   = agg_v['nb_days'] or 0
    clicks_per_day = (total_clicks / nb_vle_days) if nb_vle_days > 0 else 0

    quiz_clicks  = vle.filter(activity_type='quiz').aggregate(
        v=Sum('sum_click'))['v'] or 0
    forum_clicks = vle.filter(activity_type='forumng').aggregate(
        v=Sum('sum_click'))['v'] or 0

    # ── Encodage catégoriel ───────────────────────────────
    def encode_cat(col, val):
        le = label_encoders.get(col)
        if le is None:
            return 0
        val = str(val)
        return int(le.transform([val])[0]) if val in le.classes_ else -1

    record = {
        'gender':            1 if s.gender == 'M' else 0,
        'disability':        1 if s.disability == 'Y' else 0,
        'num_prev_attempts': s.num_of_prev_attempts,
        'studied_credits':   s.studied_credits,
        'age_band':          encode_cat('age_band', s.age_band),
        'highest_education': encode_cat('highest_education', s.highest_education),
        'imd_band':          encode_cat('imd_band', s.imd_band or 'Unknown'),
        'avg_score':         round(avg_score, 2),
        'max_score':         round(float(max_score), 2),
        'min_score':         round(float(min_score), 2),
        'weighted_avg':      round(weighted_avg, 2),
        'nb_assessments':    nb_assessments,
        'nb_tma':            nb_tma,
        'nb_cma':            nb_cma,
        'nb_exam':           nb_exam,
        'submission_rate':   round(submission_rate, 3),
        'total_clicks':      total_clicks,
        'nb_vle_types':      nb_vle_types,
        'nb_vle_days':       nb_vle_days,
        'clicks_per_day':    round(clicks_per_day, 2),
        'quiz_clicks':       quiz_clicks,
        'forum_clicks':      forum_clicks,
    }

    import pandas as pd
    # Utiliser exactement les features du modèle sauvegardé
    df_row = pd.DataFrame([record])

    # Ajouter les colonnes manquantes avec 0
    for col in feature_cols:
        if col not in df_row.columns:
            df_row[col] = 0

    df_row = df_row[feature_cols].fillna(0)
    return df_row, None
