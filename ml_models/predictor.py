# ml_models/predictor.py
import joblib
import numpy as np
from django.conf import settings

MODELS_DIR = settings.ML_MODELS_DIR

_model          = None
_label_encoders = None
_feature_cols   = None


def load_model():
    """Charge le modèle en mémoire (singleton — chargé une seule fois)."""
    global _model, _label_encoders, _feature_cols

    model_path   = MODELS_DIR / 'random_forest.pkl'
    encoder_path = MODELS_DIR / 'label_encoders.pkl'
    cols_path    = MODELS_DIR / 'feature_cols.pkl'

    if not model_path.exists():
        raise FileNotFoundError(
            "Modèle introuvable. Lancez : python manage.py train_model"
        )

    _model          = joblib.load(model_path)
    _label_encoders = joblib.load(encoder_path)
    _feature_cols   = joblib.load(cols_path)

    return _model, _label_encoders, _feature_cols


def predict_student(student_id):
    """
    Prédit le résultat d'un étudiant.
    Retourne un dict avec result, probability, risk_level, shap_values.
    """
    global _model, _label_encoders, _feature_cols

    if _model is None:
        load_model()

    from .feature_engineering import extract_features_for_student
    X_row, error = extract_features_for_student(
        student_id, _label_encoders, _feature_cols
    )

    if error:
        return {'error': error}

    # Prédiction
    proba     = float(_model.predict_proba(X_row)[0][1])
    result    = 'Pass' if proba >= 0.5 else 'Fail'

    if proba >= 0.75:
        risk_level = 'LOW'
    elif proba >= 0.5:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'HIGH'

    # SHAP — explicabilité
    shap_values = compute_shap(X_row)

    return {
        'student_id':  student_id,
        'result':      result,
        'probability': round(proba, 4),
        'risk_level':  risk_level,
        'shap_values': shap_values,
    }


def compute_shap(X_row):
    """
    Calcule les valeurs SHAP pour une ligne de features.
    Retourne un dict trié par importance décroissante.
    """
    try:
        import shap
        explainer   = shap.TreeExplainer(_model)
        shap_vals   = explainer.shap_values(X_row)

        # shap_values retourne [class0, class1] pour RandomForest
        if isinstance(shap_vals, list):
            vals = shap_vals[1][0]
        else:
            vals = shap_vals[0]

        shap_dict = {
            col: round(float(v), 4)
            for col, v in zip(_feature_cols, vals)
        }

        # Trier par valeur absolue décroissante (features les plus impactantes)
        shap_dict = dict(sorted(
            shap_dict.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        ))

        return shap_dict

    except Exception as e:
        return {'error': f'SHAP non disponible : {str(e)}'}


def get_model_info():
    """Retourne les infos du modèle chargé."""
    global _model, _feature_cols

    if _model is None:
        try:
            load_model()
        except FileNotFoundError:
            return {'status': 'not_trained'}

    return {
        'status':          'loaded',
        'algorithm':       type(_model).__name__,
        'n_features':      len(_feature_cols),
        'feature_names':   _feature_cols,
        'n_estimators':    getattr(_model, 'n_estimators', None),
        'max_depth':       getattr(_model, 'max_depth', None),
    }